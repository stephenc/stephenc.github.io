---
title: "JUnit testing strategies for EJB3 entities and beans"
date: 2006-04-07T00:00:00Z
---

Here are my initial thoughts (which I posted as a forum comment elsewhere)  

Layer 0. Test the entity beans are deployable (You'll need some of the framework from Layer 4 for this). Basically, you need to know that all your annotations work. Things to watch out for are multiple `@Id` fields in one class or `@EmbeddedID` or `@IdClass` in conjunction with `@ManyToOne`, `@ManyToMany`, `@OneToMany`, `@OneToOne` and fun with `@JoinTable`, `@JoinColumn` and `@JoinColumns`. Once you know how these are supposed to work with the specification, it's not too bad to write it correctly each time. But there are some gotchas that will break things later on.  

Layer 1. Do the functions in the classes that don't depend on annotations work as expected. Typically, this is just going to be the getters and setters in your entity classes. Of course JUnit best practice says we don't bother testing functions that look like:

```java
  public T getX() { 
  	return this.x; 
  }  

  // or  

  public void setX(T x) { 
  	this.x = x; 
  }
```

as there is nothing that can go wrong with them. So in that case, your level 1 tests will just be initial values specified from constructors and verifying that the non-get/set pairs work, and that the getters you have tagged `@Transient` work (because you've likely put some logic in them)  

Layer 2. Test the session bean methods that don't require injection to work.  

Layer 3. Test the session bean methods that require injection (Mock Objects). Simulate the injection for yourself, injecting Mock Objects for the entity manager. Then you can confirm that the correct methods are being called in the correct sequences, etc. 

[Note this may require some skill in designing the mock. I'm working on developing my own entitymanager mock, and if it looks useful I'll release it to the world.]

Layer 4. Test the session bean methods that require injection (Real entity manager) (See Layer 0) For this you will need an out of container persistence implementation. Currently Hibernate and Glassfish provide beta versions. You will need a different `persistence.xml` file that lists all the entities. You will have to use reflection to inject the entity manager(s) that you create from an entity manager factory unless you provide a constructor that takes an `EntityManager` as a parameter. You may need to use reflection to call any `@PostConstruct` method if you made it private.  

Layer 5. Navigate the relationships in the objects returned from Layer 4 using a database that has been loaded with test data.  I am currently using Layers 0, 1, 2 & 4 to test my session beans and entity beans.  

Has anyone else any other ideas?