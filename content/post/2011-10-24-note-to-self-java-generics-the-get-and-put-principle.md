---
title: "Note to self: Java Generics - The Get and Put principle"
date: 2011-10-24T00:00:00Z
---

With Java Generics, it can be useful to insert wildcards wherever possible, but how do you decide *which* wildcard is correct? When do you use `? super T`, `? extends T` and when should you not use a wildcard at all.

> **The Get and Put principle:** Use an `extends` wildcard when you only *get* values from the structure. Use a `super` wildcard when you only *put* values into the structure. Don't use a wildcard when you both *get* and *put* values from/into the structure.

The best example of this principle is the following copy method signature:

```java
public static <T> void copy(
        Collection<? super T> destination,
        Collection<? extends T> source);
```

The method gets values out of the `source`, so `source` uses `extends`, and it puts values into the `destination`, so that is declared with the `super` wildcard.