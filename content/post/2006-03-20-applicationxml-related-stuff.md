---
title: "application.xml related stuff"
date: 2006-03-20T01:00:00Z
---

I have been going nuts trying to trace problems with deployment ofenterprise applications and resource injection.  
I think the issue is around the `application.xml` file in a `.ear`! Without an `application.xml` file, everything is fine and dandy.  As soon as you add an `application.xml` file, things start breaking... it seems that when you have defined an `application.xml` file only those modules that are defined in the `application.xml` file are loaded.  Without an `application.xml` file, all the `.jar` files are scanned for `@Stateless` and `@Statefull` annotations and the modules are inferred.  It would help if there was some notification that maybe your `application.xml` file was incomplete, or else some way of restoring the scanning behaviour if you want it.  Now to go digging through the spec to see if I'm just stupidly missing something or if I need to file a bug report.