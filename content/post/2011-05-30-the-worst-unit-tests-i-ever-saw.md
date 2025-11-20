---
title: "The worst Unit Tests I ever saw"
date: 2011-05-30T00:00:00Z
---

In relation to http://dhanji.github.com/#unit-tests-false-idol here is the tail of the worst test case I ever came across...

In a former employers, there was an employee who we will call [Kevin McCallister](http://en.wikipedia.org/wiki/Kevin_McCallister) in order to protect the guilty. In any case, for various reasons, I ended up having to maintain some of the code that Kevin wrote...

I ran all the test cases and measured the code coverage, it seemed high and there were lots of test cases... but bugs a plenty kept on hitting me... I finally found the answer in one test class... which looked a little something like this:

```java
/**
 * Tests the FooBar class
 * @author Kevin McCallister
 */

public void FooBarTest {
    @Test
    public void smokes() {
        try {
            new FooBar().method1();
        } catch (Throwable t) {}
        try {
            new FooBar().method2();
        } catch (Throwable t) {}
        try {
            new FooBar().method3();
        } catch (Throwable t) {}
    
        // ...
    
        try {
            new FooBar().method15();
        } catch (Throwable t) {}
    
        // ...
    
        try {
            new FooBar().method30();
        } catch (Throwable t) {}

    }

    @Test
    public void method1DoesSomething() {
        // write later
    }

    @Test
    public void method1DoesSomethingElse() {
        // write later
    }
    
    @Test
    public void method1DoesAnotherThing() {
        // write later
    }
    
    @Test
    public void method1DoesSomethingWhenFoo() {
        // write later
    }
    
    @Test
    public void method1DoesSomethingWhenBar() {
        // write later
    }
    
    @Test
    public void method1DoesSomethingWhenBarAfterFoo() {
        // write later
    }
    
    @Test
    public void method1DoesSomethingWhenFooAfterBar() {
        // write later 
    }

    // ...
}
```

To make myself clear, there was one method at the top that called every function and would never fail (gives you the code coverage) and a couple of hundred empty test methods that did nothing but had names that sounded like nice test cases...

![Kevin!!!](/images/post/2011-05-30-kevin.jpg)

So there you have it, how not to write unit tests