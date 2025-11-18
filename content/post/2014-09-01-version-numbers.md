---
title: "Version numbers"
date: 2014-09-01T00:00:00Z
---

If there are two only things guaranteed to cause all out war between developers, my vote is that those two things are:

Code formatting conventions

Version number conventions

The first is resolved trivially (just shoot anyone suggesting the use of TABs). Until recently most people thought the second was resolved by semver… at least until the developer of one of the more commonly used JavaScript libraries threw the cat amongst the pigeons.

The real issue here is that we are trying to cram far too much into a list of number like things (that we call a “version number” - note it’s not a plural). On top of that we have marketing types putting additional demands on these poor abused version numbers.

Let’s start with some example schemes:

Every time you change something increment the number by 1.

This scheme is dead simple to implement if your source repository is Subversion, as the version number is simply the revision number.

Things get a bit harder if you use a DVCS like Git. You can certainly count commits from the root commit, but you have to worry about squashed commits and history rewriting, so you end up with a canonical repository configured to not allow rewriting of history and the version number is determined by that repository

For something like Software as a Service, there is a lot to be said with this model, as there is only ever one version in production, and that distribution model tends to follow upgrade only processes.

Once you have to maintain more than one version (i.e. if you need to fix things in older versions… or if there is an emergency fix needed in production while you await the next big release to make it through testing) then that single version number becomes a liability. You need to have some tracking database to know that version 17 was actually a fixed release of version 10.

We need some way to track those fixes...

Well there’s an infinite supply of numbers, so let’s change the scheme

Every time you release from the mainline, increment the number by 10. If releasing an update to an old release, increment the number by 1.

Well that buys us some room, but if we ever have more than 9 fixes we’ll be in trouble.

Notice now that we have switched from being able to determine the version number from a rule. The version number has now become subjective.

We can refine the scheme to give us some more room, e.g. by switching to decimal numbers.

Every time you release from the mainline, increment the number by 1. If releasing an update to an old release, increment the number by 0.1

If we consistently expect more than 9 updates to old releases then use an increment to 0.01. We can even be lazy about changing the increment and switch to 0.01 once we are at a .9 release

So far we have been able to keep some invariants:

Our version numbers are actual numbers.

Newer things have bigger numbers than older things

And if we are strict with policy, we can tell some more information from the version numbers. So for example if we say “only changes that  backport bug fixes from trunk” are allowed in older releases then you know that upgrading point releases should be safe.

At this point we now leave the realm of the actual numbers.

Semver and OSGi are amongst this class of schemes.

Version numbers are [major].[minor].[patch]

If you make a release that breaks backwards compatibility, increase the major number and reset the remaining numbers to 0.If you make a release that adds a feature but remains backwards compatible, increase the minor number and reset the patch number to 0.If you make a release that just fixes bugs, increase the patch number by 1.

There are usually additional side rules to nail the scheme down somewhat, but the principle is the same. If you write something that depends on 5.0.0 you should be “safe” with any 5.?.? release. We are now relying on even more subjective criteria, namely the question of when we break backwards compatible behaviour.

We can fool ourselves with tooling into the belief that there are automated checks of backwards compatibility, but that just captures changes to method signatures. It does not capture the documentation change that says you now need to call the ‘start’ method before using the ‘forward’ method.

So yes, tooling can help us catch those cases where we should have updated the major version and forgot to.

Tooling can be more helpful with catching backwards compatible changes (i.e. new methods in an API) but even then there can be backwards compatible enhancements that are missed by tooling (‘You no-longer have to call the ‘start’ method before using the ‘forward’ method as an un-started widget will be started implicitly on the first call to ‘forward’” would be an example)

By all means put tooling in place to help you catch those cases where you forgot to change the version number, but do not assume that the tooling absolves you from thinking about the version number.

When a project is developing rapidly it can be very easy to make mistakes in identifying and categorizing breaking changes, even semver recognises this by having an opt-out of the 0.x.x version numbers… basically under semver as long as you are in a 0.x.x version number anything goes.

Now layer on top the fact that semver does not distinguish the scope of the breaking change.

You can have a breaking change where you fixed one method in a small corner of the API to require a previously optional parameter. That requires a major version bump.

You can have a breaking change where you refactor the API splitting it from one class into two classes in a different namespace. That requires a major version bump.

So when I see a major version bump I don’t know which of those has happened.

There are really only two ways to fix that:

Add another segment (splitting the major into "really major" and "sort of major”)

Dual purpose the minor segment.

So we are either at 4 segments or we loose the ability to differentiate changes that break backwards compatibility from those that are just adding functionality.

Another thing to consider is that there is a difference in respect of version numbers for providers and consumers. So a change in an API almost always affects the provider of the API but with careful design it is often possible to ensure that the change is backwards compatible for consumers. OSGi is smart enough to make this distinction, semver however ignores this.

So what we have is a situation where we want to expose information in a single “version number” but the information is contextual.

Finally I present the AT&T history version number scheme (inherited by Avaya and Alcatel-Lucent):

Version numbers are of the format [major].[minor].[service pack].[update].[patch].[build] (or depending on who you ask it can be [major].[minor].[service pack + update].[patch].[build])

Increase the major version when you want to start cutting off support, the contract being to support the current and one back (or two back again depending on who you ask)

Increase the minor version for a new release

Increate the service pack for each service pack release. Updates to the service pack can also be released and should yield the equivalent, so Service Pack 2 Update 0 should be the same as Service Pack 1 Update 1 or Service Pack 0 Update 2. This distinction only makes sense when considering that the releases may be tied to physical hardware.

Each patch that gets released gets its own unique number.

You can build a patch multiple times before it actually gets released

This scheme presents a totally different contract from the semver/OSGi scheme and is more focused on support and maintenance contract.

What is the ideal?

Well we all need a bikeshed to paint. My suggestion:

The first segment should indicate what branches are being maintained. A project should indicate how many branches it is going to maintain and support, this could be:

just the current branch;

the current and one back;

the current and two back; etc.

Increment this version when you want to drop support for a previous branch. A good time to do this is when you make major API refactorings. What support for the non-current branch means is determined by the project. It may be that older branches can get new features or it may be that only security fixes will be made to older branches. It could even be a mixture.

The second segment should be incremented when there are breaking changes.

The third segment should be incremented when there are new features and those new features do not break consumers.

The forth segment should be incremented for bug fixes.

An optional fifth segment to be used as a qualifier such as alpha, beta, rc, etc.

This is not perfect, you still may want a separate version number for producers. But by adding the support contract to the version number you allow people to know when they should get concerned about running an older version. You also stop the rampant version number inflation that semver can lead to that seems to annoy some people… on the other hand we are now up to 4 version segments.

If there is serious interest in this scheme I may dream up a name and publish a spec!

Thoughts?