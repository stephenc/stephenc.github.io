---
title: "Do you want to become a Maven Committer?"
date: 2012-07-11T00:00:00Z
tags: ["Maven"]
---

> *Hamlet:* ... for there is nothing either good or bad, but thinking makes it so.
>
> --- Hamlet Act 2, scene 2, 239–251, William Shakespeare

The [Apache Software Foundation](http://www.apache.org/) is a meritocracy. By this we mean that you gain status based on the merit of your work and actions. In fact the status that you gain is a recognition of the merit of your work and actions.

[Maven](http://maven.apache.org/) is an Apache project, that means that we have to follow the Apache rules and way. One of those rules is that we cannot hand out commit access to anyone who asks for it.

To gain commit access you must establish your merit by submitting patches that get picked up by existing committers.

After you have contributed enough patches to establish merit, the project management committee decides whether you can be trusted with commit access.

> [!QUESTION]
>
> *Is this a good way to manage commit access?*
>
> There was a reason for the Hamlet quote that I opened this post with.
>
> Other communities can do things differently, for example the [Jenkins](http://jenkins-ci.org/) project which I am also involved with gives out commit access to anyone who cares to ask for it... but commit access to core requires completing some paperwork, and access to infrastructure requires that you establish your merit.
> 
> Which is better? It all depends on who is asking and what they mean by better.
> 
> The reality is that "It is what it is"

TL;DR To become a Maven committer write good patches and get them applied.

What makes a good patch?

A good patch is a patch that applies cleanly and includes tests that cover both the positive and negative case and has documentation where relevant.

For example, if you were implementing a patch to fix [MNG-4612](http://jira.codehaus.org/browse/MNG-4612) you would first need to write a test case that is failing when trying to encrypt

```
{DESede}y+qq...==
```

and a second test case that is passing when trying to encrypt

```
password
```

This is in order to be sure that you have written an effective test case that can pass for good data. Then you implement the fix and all the tests should pass. You then take a Subversion compatible[^1] diff of the source code and attach that to the issue in question.

To understand how your patch gets evaluated, here is how I apply patches:

1. I look at the actual diff, if there is a whole lot of formatting changes irrelevant to the issue being fixed => **Patch is no good, ask on JIRA for a clean patch**

2. I look at the list of files in the diff, if there are no tests => **Patch is no good, ask on JIRA for test cases**

3. I look at the issue and if the issue requires documentation be updated and there is no documentation changes in the patch => **Patch is no good, ask on JIRA for documentation changes in the patch**

4. I take a clean checkout of the source that the patch applies to and try to apply the patch... if it does not apply clean => **Patch is no good, ask on JIRA for an updated patch**

5. I revert the src/main and run the tests. If the tests all pass, then there are no test cases to catch the bug => **Patch is no good, ask on JIRA for proper tests**

6. I revert src and run the tests. If any tests fail, then there is something wrong with the existing code => **If I have time I might try and fix the issue, otherwise I just move on**

7. I apply the patch a second time and run the tests. If the tests all pass => **Patch is good, I commit the patch and mark the JIRA as resolved.**

So there you have it, my guide to writing good patches... now the next step is getting your patches noticed...

## How to get your patches noticed

The simplest way to get your patches noticed is to submit them to the JIRA issue that they fix.

Remember that the Maven project is run by volunteers in their spare time, so very often we may not notice your patch for a few days.

If you are certain that your patch is a good patch, and a week has passed with no comments on JIRA, then you should send one and only one email to the dev@maven.apache.org mailing list to see if your patch can get noticed.

> [!NOTE]
>
> You need to be fairly confident that your patch is a good patch, because if you keep on pestering the Maven developers looking to have non-good patches applied, your merit will become negative and people will be less inclined to help you get your patches applied... also this is why you should send one and only one email about your patch on any specific JIRA issue.

## Stephen, Arnaud & Barrie's school for potential Maven committers

To help people who are interested in becoming Maven committers fulfill their goals, myself, Arnaud Heritier and Barrie Treloar (along with any other current Maven committers who decide to help) will be running an assignment based class to help people become committers.

To register for the class you need to complete the following steps:

1. Read the Apache Individual Contributor License Agreement. When you graduate from the class you will be required to sign this in order to become a committer.

2. Subscribe to the dev@maven.apache.org mailing list.

3. Send an email to the list with the Subject line: 
    ```
    [Committer School] I would like to become a committer
    ```
    and the Message body:
    ```
    I am interested in the following areas:
      _______, _______ and ______

    If anyone knows any issues that I could take a look at I would be very much appreciated

    Thanks
    ```

Once you have registered your class assignments are basically to find JIRA issues that you want to fix. The issues can be in any part of Maven, but it is best to start with the areas you have the most interest in. Once you have found a JIRA issue that you are interested in fixing, the process will work a little something like this:

1. Make sure that nobody else is working on the issue and that the issue is one that should be fixed by sending an email to the list with a Subject line something like:
    ```
    [Committer School] Should I fix MNG-4612?
    ```
    The Message body should be something like:
    ```
    I have had a look at MNG-4612 and I think this is a real issue because...

    I think I can fix it like so....

    Is that the correct way to go about fixing it and is it a real issue at all

    Thanks
    ```

2. Wait a couple of days. Arnaud, Barrie and I will do our best to respond quickly to all such emails, but please keep in mind that we are doing this in our spare time.

3. If you get the all clear, develop your patch and upload it to the JIRA, after it is uploaded, send an email to the list with a subject line something like:
    ```
    [Committer School] Patch for review: MNG-4612
    ```
    The Message body should be something like:
    ```
    I have tested that this is a good patch and I would appreciate if a committer could review and apply

    Thanks
    ```

Keep in mind that the Committer School is just a way for us to identify people who are committed to developing patches with a view to eventually becoming committers.

When we have enough evidence that we think we can get you accepted as a committer we will nominate you and hopefully your nomination will be accepted.

Personally, if I see somebody averaging a good patch a week for 2-3 months[^2] and being active helping out on the users@maven.apache.org and dev@maven.apache.org mailing lists then I think I could make a strong case for such a person being given commit access.

So if you think you have the right stuff and want to become a Maven committer... class enrollment is open!

[^1]: The Maven project may well move to GIT at some point in the future but for now we are using Subversion

[^2]: Or a good patch a month for a year