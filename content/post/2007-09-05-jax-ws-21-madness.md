---
title: "JAX-WS 2.1 madness"
date: 2007-09-05T00:00:00Z
tags: ["Java", "JavaEE"]
---

I am sick of the fun  that is getting JAX-WS 2.1 to work on JVM 1.6.   

Oh, copy these four  jars into the endorsed directory and then you can use JAX-WS 2.1... oh but  sometimes it won't work for some unknown reason and then it will work  again.   

How you are supposed  to explain this to end users, I don't know.   

So next you need a  platform specific installer to put those jars into the correct location, or a  platform specific start script to tell the JVM about my alternate endorsed lib  folder... or do I write a self-extracting jar file that exctracts the libs and  forks a second JVM... no that won't work for people wanting to use my  library..   

We went through all  this pain with SAX and DOM.  Did Sun learn  nothing?