---
title: "The Cross-Build Injection Attack Fallacy"
date: 2012-10-01T00:00:00Z
tags: ["Maven", "Jenkins"]
---

This is a repost of my post on the CloudBees Developers blog

TL;DR Source control injection attacks are a bigger worry than build tool injection attacks, and if you cannot trust your local filesystem, then you cannot trust anything.

A few exchanges on twitter have prompted me to write a fuller blog post on the subject of Cross-Build Injection (XBI) Attacks.

The idea of XBI is that you trick the developer and replace parts of their code with your code, thereby getting your code to be trusted by the developer.

I do not object to the theory of XBI. But let's get real for a minute. Ultimately all the XBI attacks rely on a compromised local file system.

I am not saying that you cannot apply these attacks to remote systems and then have those affect developers with un-compromised local file systems.

I am saying that when you fix any remote vectors, you still end up victim of the local file system integrity.

Take for example this attack vector using Maven as an example victim build tool. How does the attack work? Well it replaces a good artifact in the Maven local repository with a bad version… and bad things happen.

For this attack to work for real you need to have your local file system compromised. Is that attack specific to Maven? Nope. You can get your $ANT_HOME/lib folder contents compromised just as easily (i.e. if your local file system cannot be trusted to hold your local repository, it cannot be trusted to hold your build tool) Same too applies to Gradle, Make, MSBuild, etc.

How do we prevent the attack? Well for quite some time the central repository has only been publishing artifacts with GPG signatures. So we could verify the GPG signature before each and every build… but those signatures are stored on the file system too, so we cannot trust them… and our GPG checking code is stored on the filesystem also… so we cannot trust that! Never mind that such checks would slow every build down - increasing the risk of the developer being knocked out of “the zone”.

The reality of “the zone” is often lost on people. Working memory is only able to retain information for a couple of seconds at a time and therefore any interruptions can be fatal to problem solving processes. Software development is one continuous problem solving process after another. If you add 5 seconds to every build, then that is 5 seconds of temptation for the developer to check their email / reddit / stackoverflow / etc. And then they will have to rebuild the context of the problem they were solving. In some cases, this can correspond to up to 45-50 minutes of zero productivity for the developer (I cannot find the link, but I have personal experiences that confirm this).

Good developers that recognise this problem will therefore seek to reduce build time to the minimum… therefore turning off any GPG or other integrity checks, etc. If you ask them why, they will probably respond with something like:

Well if I cannot trust the local filesystem, sure I cannot trust the SCM or the signature checks to even run in the first place. I'm reclaiming those 5 seconds on every build and being more productive.

What is the solution? Simple. Don't do the checks until you are making the release build! Better yet do the release builds from a continuous integration server such as Jenkins. You can lock that down, have it do the checks for you, and have it sign the resultant artifacts… but just be sure that you trust its filesystem and your source control system too!