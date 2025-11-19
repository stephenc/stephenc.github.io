---
title: "Java Serialization and locks"
date: 2011-08-15T00:00:00Z
---

Java has a couple of “nice” features, specifically:

* Built-in locks

* Baked in support for object serialization

Now I don't want to get into a war about how both of these are flawed (there was a reason that I put “nice” in quotes) but here is a quick note on how to make the two play nice (more as a reference to myself... but if others find this useful, well and good).

## General principal

In essence, in each case you implement the `readObject` and `writeObject` methods per the [Java Object Serialization Specification](http://download.oracle.com/javase/1.3/docs/guide/serialization/spec).

## Using object's intrinsic lock

In this case you can just make the `readObject` and `writeObject` methods `synchronized`:

```java
private synchronized void readObject(ObjectInputStream stream)
        throws ClassNotFoundException, IOException {
    stream.defaultReadObject();
}

private synchronized void writeObject(ObjectOutputStream stream) 
        throws IOException {
    stream.defaultWriteObject();
}
```

## Using Java 5 style locks

In this case you just wrap the functionality inside a `try`...`finally` block

```java
private void readObject(ObjectInputStream stream)
        throws ClassNotFoundException, IOException {
    lock.lock();
    try {
        stream.defaultReadObject();
    } finally {
        lock.unlock();
    }
}

private void writeObject(ObjectOutputStream stream) 
        throws IOException {
    lock.lock();
    try {
        stream.defaultWriteObject();
    } finally {
        lock.unlock();
    }
}
```

## Using multiple locks

If your object uses multiple locks to guard the different fields, there are really two techniques you can use:

* Get all the locks in one go, ensuring that you always get multiple locks in the same sequence (high-risk)

* Stop relying on `stream.default____Object()` and get/set each field manually in code as that allows you to hold one lock at a time (may write a partially modified object)

## Gotchas

Watch out for the fields you are writing being mutable and modified by other threads while you are writing them to the stream. Reads from a stream are less of an issue as the object should not be given to another thread until fully read back in.