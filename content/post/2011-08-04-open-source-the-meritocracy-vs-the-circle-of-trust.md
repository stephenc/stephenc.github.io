---
title: "Open Source: the Meritocracy vs the Circle of Trust"
date: 2011-08-04T00:00:00Z
---

There has been this idea running around the back of my head for a while, and it's only now that it is starting to crystalize into something that I can express.

When we look at Open Source projects, we see that there is a hierarchy of involvement. There are different levels at which you can be involved, and at each higher level, there will be less and less individuals. For now I am going to divide involvement up like this:

* Interested: this group of individuals know that the project exists, and might even be following what it is doing, but have not been able to actually use the project at all yet (for whatever reason)

* Consumers: these are the people who actually use the project. They may not even be following the project, e.g. a lot of people consume log4j or ANT without following the mailing lists, seeing what features are on the roadmap, or even filing issues.

* Contributors: if you are filing issues, submitting patches, etc, but you do not have commit access to the project, then you are a Contributor.

* Committers: you have commit access to the project

* Management: you get to have a say in some of the following: whether the new release of a project can be released; the architecture/direction of the project going forward; who has commit access; etc.

Different Open Source projects but different barriers at different points. For example:

* Contributor road-blocks:

    * You may have to create an account to file issues. [Technical]

    * You may have to sign a CLA and fax it off before you can commit any patches. [Legal]

    * You may have to get a notarized signed CLA sent via snail-mail before you can commit any patches. [Legal]

    * You may have to get your employer to sign-off on you contributing patches. [Legal]

* Committer road-blocks:

    * You may have to be invited to become a committer.

    * You may have to establish merit before you can be invited to become a committer.

    * You may have to sign a CLA and fax it off before you can get commit access. [Legal]

    * You may have to get a notarized signed CLA sent via snail-mail before you can get commit access. [Legal]

    * You may have to get your employer to sign-off on you committing code to the project. [Legal]

* Management road-blocks:

    * You may have to be invited to become management.

    * You may have to establish merit before you can be invited to become management.

> [!NOTE]
> I'm not going to even try and pretend that the above is a complete list of road-blocks

Different people view success of Open Source projects differently. Some measures of success include: the number of consumers;  the number of active contributors; the number of committers; the number of releases; the number of downloads; the number of issues raised and closed; the activity of mailing lists.

None of these are correct, and much like psychologists hypothesize a (in reality) unmeasurable [“g factor”](http://en.wikipedia.org/wiki/G_factor_(psychometrics)) as a true measure of intelligence against which all real measures (such as IQ) are only partial measures. We could hypothesize an unmeasurable “s factor” which is the true measure of the success of an Open Source project.

But I don't want to go down such an academic road today. Instead lets look at the dependency tree in the measures of success that we know of...

* Number of downloads depends on number of consumers: as a consumer has to download your project at least once... it is not a perfect dependency, because you could download each release of the project once and every time decide it is a load of rubbish and never actually consume it... and a consumer may have just downloaded version 1.0 once and stayed on that version for ever more, but in general, if you have a large number of consumers, you will have a large number of downloads and the opposite does not necessarily follow.

* Activity of mailing lists depends on the number of active contributors: when you have a lot of active contributors, the mailing lists will be active... however the mailing lists can be active without any active contributors.

* Number of issues raised depends on the number of active contributors: for similar reasons to the previous.

* Number of issues closed depends on the number of committers: because you need commit access to close most issues (appart from the "not a bug" type of issues)

So a lot of the measures of success can be raised by increasing the number of consumers, active contributors, and committers. However, just because we have a large number of consumers/active contributors/committers does not imply that we have a successful project, it just says that projects that have a large number of consumers/active contributors/committers have a greater likelihood of being successful projects.

So how do we increase that number, and thereby increase the probability that our Open Source project is a “success”?

Well, if you are picking an project to use, i.e. deciding to become a consumer, one of the things you will look at is how active the community is (i.e. number of active contributors and number of committers). It's not the only thing you will look at, but assuming you have two projects which have the feature-set you need, and they are comparable in usability, etc. When you come to make the decision, the social beast in you will pick the larger active community (who wants to pick the dead project). The active community also act as evangelists out selling the project to potential consumers. So one way to grow the number of consumers is to grow the active community.

* Number of consumers (partially) depends on the number of active contributors

If we have lots of active contributors and very few committers, very soon there will be a glut of patches that don't get applied, and the active contributors will wonder off to another project where there contributions can be consumed. So for each project, there is probably some upper limit to the number of active contributors that depends on the number of committers. That limit depends on things like the complexity of the project, the code base, the toolchain used by the project, the project management processes, etc. So I don't think there is any hard and fast rule like you can have X active contributors for every Y committers on any open source project.

But what I do think we can say is:

* Number of active contributors is limited by the number of committers.

So at this point you might feel that my chain of logic looks a little like this:

![](/images/post/2011-08-04-jenga-tower.jpg)

But I should point out that what I am trying to say is really that:

> Having a lot of committers
> 
> indicates that a project is more likely to be successful, 
> 
> but it cannot guarantee that success.

Hopefully your back thinking I have a solid argument again.

So how do we get a lot of committers? Well the answer is easy, remove as many road-blocks to becoming a committer.

Some of the road-blocks are technical. So you have to create an account to file issues... well we can switch to a issue tracking tool that uses OpenID or oAuth and now you can use an account you already have to file those issues... or perhaps you can just provide your email address and fill in a captcha... etc. None of these completely remove the technical road-block, but they can make it easier for the consumer to graduate to active contributor.

Some of the road-blocks are legal. So you need a CLA signed with the blood of an Armur leopard before you can submit a patch. These are harder to work around, but not always impossible e.g. perhaps small patches (less than some size metric) don't need the CLA.

After all these road-blocks, we start to hit what I like to call the “merit wall”. And this is the problem that I see. In essence you need to establish that you have the merit to work on the project. You need to establish a chain of consistent patches (which get picked up by the existing committers) of good quality before you are invited to become a committer.

That to me is a crazy way to gate commit access.

Just because your submitted patches were all stellar quality, that could just be the result of the areas being patched having good test coverage, so you were forced to get the code right. It could be that the nature of bundling up your changes as a patch forced you to think more about the changes. You could become sloppy as a coder, etc.

There are many reasons why “past performance is not a guarantee of future returns”. Some people think the solution to this is to have merit expire, e.g. if you have not worked on the project recently, then you loose the right to work on the project. All that happens then is that people start doing busy work on the project just before their merit is due to expire, and such busy work is, by its very nature, not the work that drives a project forward.

In my view, the only merit to contribute to a project is the code you are contributing right now. Not the code you contributed yesterday, last month, or last year. Not the code you might contribute tomorrow, next month, or next year. But the code you are contributing right now. You don't have merit, but your code might.

> Merit is the wrong thing to use as a gate for commit access.

Because what is giving commit access really about? It is about saying that we trust you to commit changes to the project. If you commit code which has no merit, we (or you) can use the SCM to back out those changes. The merit of your previous submissions is a very poor measure of our trust in you using the SCM. In fact because for a lot of projects, generating patches actually is about not using the SCM at all (Git pull requests changes that) it is exactly the wrong thing to use to establish trust.

Once we realize that commit access is about trust and not merit, then we can really start to build a community, and increase the likelihood of our project being a success:

* You don't start with zero trust.

* One big abuse of trust, and you have lost all your trust and you have to work a lot harder to earn what you had back again.

* You have to be given scope in order to earn more trust.

* Trust does not expire easily.

So what I am arguing is that if somebody shows up knocking at the door of your project looking to contribute, at some point you have to trust them enough to open the door and let them in. It's fine if you have a few hurdles that they have to jump, but remember that at the end of the day you are trying to decided if you trust them enough to let them make changes to the code, or to put it another way, if you trust them to make good judgements on the merit of any changes they want to commit.

> Your merit as a committer is not the merit of the code changes you have committed, but all the code changes you did not commit because those changes had no merit.

A good committer is somebody who does not make changes that are bad. The ideal committer only makes commits that improve the project. Joe might be the ideal committer for your project even though he has never submitted a patch because Joe knows when a patch is improving the project and when it is not, but because Joe has never submitted a patch, he has earned no merit in your projects eyes, so he will never become a committer.

Commit access is about letting somebody inside the circle of trust. The easier you make that process, the more vibrant your community, and the more successful your project. Put a merit wall in place and you are alienating your potential community (never mind that it is the wrong barrier in the first place)

Look at the [Jenkins](http://jenkins-ci.org/) project. If you want commit access, you just ask for it. How is that for initial trust. The result is a very successful project, oh and the sky has not fallen. Everyone that has been trusted so far has respected the trust they have been shown.

Look at most projects hosted on github. Pull requests have effectively removed a large chunk of the need for commit access, and because you can see the person's skills with the SCM, they can earn trust to be let loose on the canonical source directly.

![](/images/post/2011-08-04-circle-of-trust.jpg)

*A merit wall can leave you feeling like this*

So my message to all open source projects that use merit based on previous patches as a measure of the worth of a potential committer, please look again at your policy. Are you sure you are looking for the right qualities to drive your project to bigger successes?