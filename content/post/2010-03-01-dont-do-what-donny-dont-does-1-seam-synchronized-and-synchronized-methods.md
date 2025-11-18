---
title: "Don't Do What Donny Don't Does #1 - Seam @Synchronized and  synchronized methods"
date: 2010-03-01T00:00:00Z
---

I am starting a series of things you should not do:

Seam has this handy annotation: @Synchronized which ensures that only a single thread may access the methods/fields of the component at the same time.

Often times it is easy to forget that SESSION scoped Seam components are automatically @Synchronized

Java has this (formerly) handy modifier synchronized which when applied to a method, ensures that the object's implicit lock is held whenever the method is invoked.

Hilarity will ensue if you have an @Synchronized component with synchronized methods (which you should not have to apply because the component is @Synchronized), e.g.

@Name("donny")

@Scope(ScopeType.SESSION)

public class DonnyDont {

public synchronized String dont() {

// some stuff

}

}