---
title: "JPA Entity exerciser"
date: 2007-07-20T00:00:00Z
tags: ["Java", "JavaEE"]
---

Working on this to add to EasyGloss.

There are a number of rules that JPA entities must obey:

* `equals` and `hashCode` must only be based on the persistent fields that are `@Id` annotated.
* annotations must be applied to either fields or getters, no mix & match (although future versions of the spec may provide for such)
* In general, getters and setters should be simple methods (i.e. no complex processing)

I want to have a JPA Entity excerciser that will check these rules for you (and can be included in your unit tests)