---
title: "hashCode() pitfalls with HashSet and HashMap"
date: 2007-02-26T00:00:00Z
---

I have been reading a book on C# recently, and it got me thinking about Java's `hashCode()` in a little bit more detail than I had before.

Consider the following Java class.


```java
public class Person {  
	private String firstName;  
	private String surname;  

	public Person(String firstName, String surname) {    
		this.firstName = firstName;    
		this.surname = surname;  
	}  

	public boolean equals(Object other) {
		/* proper equals checking firstName and surname */  
	}  

	public int hashCode() {
		int code = surname.hashCode();
		code = 31 * code + firstName.hashCode();    
		return code; 
	}  

	public String getFirstName() { /* getter */ }  
	public void setFirstName(String firstName) { /* setter */ } 
	public String getSurname() { /* getter */ } 
	public void setSurname(String surname) { /* setter */ }
}

```
What is wrong with the above? Ignore that the hash code may not be well designed given that names are usually A-Z only and the prime factor may not be the most efficient algorithm for calculating hash codes for our data set.

OK, so I have cheated... the problem is the setters that I glossed over.

Our hash code is not calculated on the basis of immutable values.Let's try using it with a `HashSet`...

```java
Person joe = new Person("Joe", "Bloggs");
Set people = new HashSet();
people.add(joe);

assert people.contains(joe); // this works
assert people.contains(new Person("Joe", "Bloggs")); // this works

joe.setSurname("Smith");

assert !people.contains(new Person("Joe", "Bloggs")); // this works
assert people.contains(new Person("Joe", "Smith")); // this fails!!!
assert people.contains(joe); // this fails!!!

boolean found = false;
for (Person person: people) {  
	if (person == joe) {    
		found = true;    
		break;  
	}
}
assert found; // this works!!!
```

So what is going on?

When we put joe into the `HashSet`, the `HashSet` selects a bucket based on the hash code for `joe`.  When we ask the `HashSet` if it contains a `Person`, it computes the hash code of the object that it's looking for and searches only in that bucket.

As our `hashCode()` is based on non-final fields, the hash code can change behind the scenes of our `HashSet` (and it won't find out until it has too few buckets and needs some more to optimise searching). Thus completely invalidating the basic assumption of the `HashSet`.

A correct implementation for the `Person` class would either have the names as `final`, or have `hashCode` like so

```java
public int hashCode() {  
    return 0; // we have no non-final identity fields to calculate the hashCode from
}
```