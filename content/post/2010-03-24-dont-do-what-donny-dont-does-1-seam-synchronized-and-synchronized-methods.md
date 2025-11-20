---
title: "Don't Do What Donny Don't Does #1 - Seam @Synchronized and  synchronized methods"
date: 2010-03-24T00:00:00Z
---

I am starting a series of things you should not do:

![](/images/post/2010-03-24-donny-dont.jpeg)

Seam has this handy annotation: [`@Synchronized`](http://www.google.com/url?sa=t&source=web&ct=res&cd=1&ved=0CAgQFjAA&url=http%3A%2F%2Fdocs.jboss.org%2Fseam%2F1.1GA%2Fapi%2Forg%2Fjboss%2Fseam%2Fannotations%2FSynchronized.html&ei=0-upS5uqJYvyNP3V_eQB&usg=AFQjCNG8cnfD4zCN-VH28nWD_W1eoRMqxA&sig2=Yxc0t-IQgA5yST-uA40img) which ensures that only a single thread may access the methods/fields of the component at the same time.

Often times it is easy to forget that SESSION scoped Seam components are automatically `@Synchronized`

Java has this (formerly) handy modifier [`synchronized`](http://java.sun.com/docs/books/tutorial/essential/concurrency/locksync.html) which when applied to a method, ensures that the object's implicit lock is held whenever the method is invoked.

Hilarity will ensue if you have an `@Synchronized` component with `synchronized` methods (which you should not have to apply because the component is `@Synchronized`), e.g.

```java
@Name("donny")
@Scope(ScopeType.SESSION)
public class DonnyDont {
    public synchronized String dont() {
        // some stuff
    }
}
```