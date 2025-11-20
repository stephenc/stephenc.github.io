---
title: "Backwards compatibility"
date: 2011-05-27T00:00:00Z
tags: ["Jenkins", "CloudBees"]
---

This is a tail about Jenkins (née Hudson) and Kohsuke's policy of maintaining backwards compatibility...

Back in 2006 I started working for my previous employer, just a month or two after Peter Reilly started. Initially we were working on the same team. This was a team who's CI system was a nightly cron job that emailed off a list of failing tests to everyone... obviously Peter and I had many a WTF over that old system... so I convinced our boss that we should put some effort into setting up a proper CI system... Initially this was CruiseControl (as he thought Hudson at version 1.64 was too new and unheard of... go with the old reliable)... but after a couple of pains with the CruiseControl system (monolithic xml config file), we convinced him to switch to Hudson... (I don't think we ever looked back!)

What we really liked was that Kohsuke had put in place a plugin framework, so I started writing plugins, and shortly afterwards convinced Peter that it was "cool" (even if he did have to use Maven to build the plugins - Peter is on the Apache ANT PMC).

One of the earlier plugins that Peter wrote during his spare time was his "Simple Cobertura plugin" which allowed you to get the Cobertura coverage results on the build page[^1]. Peter created his plugin against Hudson 1.129. By this stage Peter and I had moved onto separate projects, eventually Peter left the company, but the team he was working on still had the .hpi for his "Simple Cobertura plugin". As they moved to newer and newer Hudson builds, the plugin kept on working (no recompile needed). I had my own plugins which were built for an earlier version of Hudson (my closed source SilkTest plugin, my original closed source AccuRev plugin [not to be confused with the open source one I subsequently developed and handed on to others to maintain]) which also were still working (with no recompile) in newer versions of Hudson

Recently, I met up with Peter, and he told me the sad news.... his plugin is now broken... it no longer works in the latest version of Jenkins... this was strange news to me, as before I left my previous employer to join [CloudBees](http://www.cloudbees.com/) I'd upgraded our CI servers to the latest and one of those was using Peter's "Simple Cobertura plugin" which did not seem broken...

After looking at Peter's code I finally found the problem... he was using the old javadoc annotation to mark the constructor as one for data binding, with one simple change:

```diff
6,7d5
> import org.kohsuke.stapler.DataBoundConstructor;
>
22a21
<      * @stapler-constructor
24d22
>     @DataBoundConstructor
```

His plugin was back in action... Now I was puzzled, as I couldn't understand how I'd upgraded this old old plugin from Hudson 1.129 and got it running on Jenkins 1.397 without recompiling...

Well I found out the answer, the version Peter had left in behind, didn't use the data bound constructor at all... it was doing

```java
public Publisher newInstance(StaplerRequest req) throws FormException {
    return new C2Publisher(req.getParameter("c2_coverReportDir"));
}
```

While the code Peter had was doing

```java
public C2Publisher newInstance(StaplerRequest req, JSONObject obj) 
        throws FormException {
    return req.bindParameters(C2Publisher.class, "c2_");
}
```

If you change it back to the old way, and you have enough Maven-foo to build against that old a version of Jenkins (née Hudson) you can end up with a plugin that works on both Hudson 1.129 and Jenkins 1.413...

I am fairly sure that if I had a SilkTest license and a copy of the SilkTest plugin that I wrote against Hudson 1.96, it would also still run unmodified on Jenkins 1.413.

How many projects can maintain **that** level of backwards compatibility.

[^1]: Peter wanted to have the coverage results on the main page, and at the time Kohsuke did not want to allow plugins to add columns to the main page... I came up with the compromise of adding a column which would be just one icon wide and have a tooltip to which plugins could contribute information... and that was the birth of the weather (health) icons[^2]

[^2]: At the time Peter thought it would be cool if he could generate his own weather icon on the fly so that if you had high code coverage that would be a full umbrella while poor code coverage would be a tattered umbrella with no fabric and only the frame remaining... this is actually part of the API, so the technology to implement this has been there since 1.115... just nobody has done it... yet!