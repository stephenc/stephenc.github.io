---
title: "When a Kubernetes Operator Makes Sense"
date: 2025-11-18T12:00:00Z
tags: ["kubernetes", "operator-pattern", "vault", "devops", "platform-engineering"]
categories: ["Infrastructure", "Kubernetes"]
series: ["Advanced Kubernetes Patterns"]
images: ["/images/post/2025-11-18-when-a-kubernetes-operator-makes-sense.png"]
---

# When a Kubernetes Operator Makes Sense

![Simplifying a tangled mess with a Kubernetes Operator](/images/post/2025-11-18-when-a-kubernetes-operator-makes-sense.png)

## Beyond YAML: Real-World Lessons from Managing Complex Infrastructure

There are plenty of ways to deploy applications onto Kubernetes:

* raw `kubectl apply`
* Kustomize overlays
* Helm charts
* sidecars and init containers
* and, at the far end of the spectrum, fully-fledged operators

Most teams start at the simple end and stay there. And they should, most applications don’t need anything more complicated than a Deployment, a few ConfigMaps, and a `kubectl apply -k`.

But over the last few years building and operating platforms for distributed systems, secrets management, and internal PaaS primitives, I’ve learned a consistent pattern:

> **If you find yourself orchestrating multi-step lifecycle logic with scripts, sidecars, or tribal knowledge, you’re already halfway to writing an operator — whether you mean to or not.**

In this post, I outline when an operator genuinely makes sense, using one of the clearest real-world cases I’ve worked with: **running and operating Vault** inside Kubernetes.

## The Limits of YAML, Sidecars, and Good Intentions

Kubernetes gives you powerful declarative primitives, but those primitives assume your application behaves like a stateless, idempotent component. In practice, many systems don’t.

Teams often try to bridge the gap with tools like:

* init containers
* sidecar containers
* Helm hooks
* bash scripts baked into container entrypoints

These techniques work when the lifecycle is simple: “run this once, then start the app.”
But they fall apart completely when the application behaves like a **state machine** rather than a simple process.

Vault is the poster child for this.

## Case Study: Vault’s Lifecycle Doesn’t Fit the Pod Lifecycle

Vault is incredibly powerful — but it has distinct operational states:

* uninitialised
* initialised but sealed
* unsealed
* leader
* follower
* resealed on restart
* expiring leases
* privileged configuration requiring root-level access

None of that behaviour maps cleanly onto a `Deployment` or `StatefulSet`. And for a while, the SRE team supporting our Vault deployments tried to glue the lifecycle together using init scripts and sidecars.

It was unreliable. And unavoidably so. While the SRE team heros could keep our SaaS instance working, the problems really started to surface when the product was deployed in dedicated VPC instances for bigger customers.

1. **Initialisation isn’t idempotent**

    `vault operator init` must run *exactly once*, on one node, and only when the cluster is uninitialised.
    If a script guesses wrong, it bricks the cluster.

    Operators excel here because they can read application state, maintain a shared control loop, and encode an idempotent workflow.


2. **Pods don’t share memory — but Vault has shared state**

    Sidecars run **once per pod**, but Vault’s state is **cluster-wide**.
    Coordinating initialisation, unseal operations, and failover across replicas cannot be expressed through pod-local logic.

    An operator, running as a single control plane component, can coordinate safely.

3. **Multi-step workflows don’t belong in bash**

    A simplified lifecycle of a Vault cluster:

    1. Detect initialisation state
    2. Initialise (once) if required
    3. Store unseal keys safely
    4. Unseal nodes one by one
    5. Detect restarts
    6. Re-unseal automatically
    7. Reconcile mounts, roles, and policies
    8. Rotate secrets
    9. Maintain downstream K8s access tokens
    10. Back up and restore data selectively

    Trying to express this via init scripts and pod startup timing is brittle and unsafe.

4. **Failures are domain-specific, not pod-specific**

    “Sealed” is not “crashed.”
    Vault failures require domain-aware remediation, not generic liveness probes.

    Operators can interpret domain faults and take domain-correct actions.

> [!EXAMPLE]
> *A Real-World Example of Why Scripts Fail: The “Replica Index Hack”*
> 
> One of the clearest signs the approach had gone too far was a clever — and unintentionally hilarious — hack I encountered.
> 
> To prevent every pod from attempting initialisation, the team leaned on this logic:
> 
> * Vault pods in a StatefulSet get predictable names: `vault-0`, `vault-1`, …
> * Helm passes `replicaCount` into the container.
> * The init script would:
> 
>   * Parse its own index
>   * Compare it to `replicaCount - 1`
>   * If it was the “last” pod, assume the others were up
>   * Attempt initialisation
>   * Have all other pods skip
> 
> In other words:
> 
> > **“Use pod index order and hope Kubernetes starts pods in sequence.”**
> 
> Of course:
> 
> * Kubernetes makes *no guarantee* about pod startup order
> * Restarted pods break assumptions
> * A “last” pod can start *first* after rescheduling
> * Node drains or autoscaling resets the whole hack
> 
> This was an accidental reinvention of a distributed coordination protocol using naming conventions and timing.
> 
> And it failed exactly when you’d expect it to.

This was the moment it became clear: we needed a **real controller**.

## Evaluating Open-Source Vault Operators

Before building anything, we evaluated the existing ecosystem:

* HashiCorp Vault Secrets Operator

    Great for syncing secrets *downstream* into Kubernetes Secrets.
    **Not designed for managing Vault itself**, nor for initialisation/unseal logic.

* KubeVault (AppsCode)

    A more complete lifecycle solution, but opinionated and not compatible with our custom bootstrap requirements, existing tooling, and security model.

* Others

    Similar limitations — focused on secret consumption, not cluster lifecycle, privileged config, or platform integration.

**None addressed our core needs:**

* lifecycle orchestration
* custom initialisation
* controlled privileged operations
* direct app authentication
* integration with our existing IAM and KMS architecture
* some other needs related to our VPC and SaaS deployment models

This wasn’t a case of reinventing the wheel, the wheel we needed didn’t exist.

That’s when the operator became the obvious path forward.

## How I Secured Root Credentials: AWS Secrets Manager + IRSA

One major design requirement was that **no human** and **no pod except the operator** should ever see:

* Vault initialisation seeds
* unseal keys
* the root token

I solved this with a combination of AWS Secrets Manager and IAM Roles for Service Accounts (IRSA):

* *Storage*

    * The operator stored the seeds and unseal keys in **AWS Secrets Manager** during initialisation.
    * Kubernetes never held these secrets at rest.

* *Access Control*

    * The operator ran under a dedicated Kubernetes ServiceAccount.
    * That ServiceAccount was mapped to a locked-down IAM role using IRSA.
    * That IAM role had the *only* permissions to access the specific secrets in Secrets Manager.

* *Operational Flow*

    1. A platform/team user creates a CRD (e.g., `VaultBackup`, `VaultConfigChange`, `VaultUnseal`).
    2. Kubernetes RBAC determines who can create which CRDs.
    3. The operator watches the CRD and:

       * Assumes its IAM role
       * Fetches the required seeds/keys from AWS Secrets Manager
       * Performs the privileged operation
       * Discards the credentials
    4. The operator updates the CRD `status` for audit and visibility.

This pattern gave us:

* Zero exposure of root keys
* Full AWS audit logs
* Zero trust of pods
* Simple RBAC for safe delegation
* Compliance-friendly credential handling

## When You Know It’s Operator Time

Here’s the checklist I now rely on:

- [x] Initialisation requires conditional or multi-step logic

- [x] The system has meaningful runtime states

- [x] You must reconcile external state with Kubernetes

- [x] You need domain-aware healing, not restarts

- [x] Privileged operations need safe delegation

- [x] Teams are writing bash scripts to automate lifecycle logic

Any one of these can justify an operator.
All of them together make it unavoidable.

## Final Thoughts

Most systems don’t need operators.
But the ones that do… *really* do.

When applications have rich state models, privileged operations, or complex orchestration sequences, Kubernetes’ built-in controllers aren’t enough. Operators allow you to encode operational knowledge where it belongs: in code, with guardrails, observability, and repeatability.

For us, Vault was one of those systems.
And moving from fragile init scripts and hacks to a robust operator architecture turned it into a reliable, secure platform service.

If you find yourself debugging the same lifecycle script for the tenth time, or relying on pod index order as a coordination mechanism, that’s your signal:
**you’re EITHER fighting the platform _OR_ it’s time to extend it.**

## Where to Start?

If this article resonates with you, it might be time to explore the ecosystem. Look into frameworks that simplify the development process:

- [Kubebuilder](https://book.kubebuilder.io/): The standard for building operators with Go.

- [Operator SDK](https://sdk.operatorframework.io/): Provides more scaffolding and support for different languages, including Ansible and Helm.

Start by modeling one small, painful piece of your application's lifecycle as a Custom Resource Definition (CRD). You don't have to build the entire controller at once.
