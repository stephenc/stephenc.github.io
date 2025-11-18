---
title: "Jenkins' Maven job type considered evil"
date: 2013-11-01T00:00:00Z
---

There are two ways to build a Maven project with Jenkins*

Use a free-style project with a Maven build step

Use a Maven-style project

The first way runs the build as Maven intended. The second way adds a whole lot of hooks and can even modify the build in ways that Maven did not intend.

The first way requires that you configure stuff yourself. The second way tries to “guess” what you want and auto-configure it.

The first way is initially less user friendly, i.e. you have more UI to click through to get the full set of reports. The second way is initially more user friendly… but when things go wrong… well sorry out of luck.

If something goes wrong with the first way, worst case you add a shell build step above the Maven build step that just runs SET, trigger a build, login to the build slave, switch to the user the build is running as, apply the environment your SET build step output and then run the Maven command that the build’s console log captured. That will give you an exact reproduction of the Maven build and you can debug why your build is not working.

When something goes wrong with the second way, well good luck. By all means try to do the same as you would for a free-style project, but at the end of the day, there is no way you can replicate the injected hooks that Jenkins puts into your Maven build. You can get an approximate reproduction, and hey, that may just be enough to let you figure out what is wrong and fix your build… but there are cases where you cannot.

Hence why, since 2007, I have been saying that the Maven job type is considered evil…

It has very attractive because is easy to configure (so users use it) and gives nice per-module reports

When it blows up, and it will blow up, it blows up big

-Stephen

* well actually three ways§ if you include the literate job type

§ (Update 2017-08-01) well actually four ways if you include pipeline and the withMaven helper