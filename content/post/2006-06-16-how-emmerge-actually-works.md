---
title: "How em.merge actually works"
date: 2006-06-16T00:00:00Z
---

Let's have a look at some `em.merge` related fun.

From discussions on a number of forums, here is my explanation for what goes on when you call `em.merge`.

We will use the following classes as an example:

```java
@Entity
public class Parent {
    // ...
    private List<Child> children;
    // ...    
    public List<Child> getChildren() { return this.children; }
    public void setChildren(List<Child> children) { this.children = children; }
    // ...
}

@Entity
public class Child {
    // ...    
    private Parent parent;    
    // ...    
    public Parent getParent() { return this.parent; }    
    public void setParent(Parent parent) { this.parent = parent; }    
    // ...
}

```

To aid in understanding, we will assume that our client has a `UserTransaction ut` (this is to allow us to force entity instances to become detached. Entity instances can becomedetached without using a `UserTransaction`, however, we want to show what happens to the entities;

So our client goes something like:

```java
Parent parent = null;  
// ...  
ut.begin();  
parent = em.find(Parent.class, aParentId);  
// ...
```

At this point the client has a reference to a managed instance. We can illustrate this like so:

[image lost - ed]

Now at some point we have to commit the transaction and the transaction ends.

```java
// ...  
ut.commit();  
// ...
```

So now parent still points to an instance of the class `Parent` that still holds the data as before, however, the instances have lost their connection to the entity manager (as the connection depended on the transaction.)

We can illustrate this like so:

[image lost - ed]

Later on, we want to synchronise the parent object back to the database, so we call `em.merge`:  

```java
// ...  
ut.begin();  
Parent managedParent = em.merge(parent);  
// ...
```

Now, the transaction is still active, so the instances pointed to by `managedParent` are still managed instances, i.e. changes made to fields will be reflected back into the database.

The instances pointed to by parent are still detached instances, i.e. changes made to fields do not get persisted back to the database. `em.merge` has done two things for us:  

1. Fetched new managed instances of the objects we already have  
2. Synchronised all the changes in the instances we have back to the managed instances (and therefore back to the database)

We can illustrate this like so:

[image lost - ed]

Once we commit or otherwise end the transaction, we will now have two sets of detached instances.

Some people want to not have references to our old detached instance lying around... so they will typically reuse the parent instance variable like so:

```java
// ...  
ut.begin()  
parent = em.merge(parent);  
// ...
```

This is OK, provided that there are no other references to the detached entities lying around.

If you had done something like  

```java
// ...  
Child child = parent.getChildren().get(0);  
ut.begin();  
parent = em.merge(parent);  
ut.commit();  
// ...
```

Then you are in a dangerous situation as child points to a different detatched instance of the same persisted entity!!!

[image lost - ed]

The moral of the story is that when you call `em.merge`, you need to know what instances you are merging and what you will do with the detatched instances after you have finished merging