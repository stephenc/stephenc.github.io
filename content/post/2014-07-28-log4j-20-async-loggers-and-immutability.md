---
title: "Log4j 2.0 Async loggers and immutability"
date: 2014-07-28T00:00:00Z
tags: ["Java"]
---

One of the headline grabbing things that people seem to be raving about over Log4J 2.0 is async loggers.

Now do not get me wrong, they are great… as long as you know what you are doing.

If you are using async loggers you had better make sure you are only passing immutable objects to your loggers, because otherwise you may end up logging the state of your objects at the time of the log record being written and *not the time you called log*.

Now there are many other good reasons why you should use immutable objects for your logging, but async logging is the tipping point.

A few years ago I was burned by this exact class of problem in a conferencing call bridge, where we had a log message recording the participants that were actively talking (i.e. their volume was greater than the threshold). Spurious line noise would result in messages like:

```
Bob has started talking, Bob’s volume is 1, threshold is 64
Bob has stopped talking, Bob’s volume is 120, threshold is 64
```

Which was a result of the mutable object that held the volume for Bob being changed by the media server in between creating the log record and writing the log record to disk.

Consider the following simple test class:

```java
package test;

import org.apache.logging.log4j.LogManager;import org.apache.logging.log4j.Logger;

import java.util.concurrent.atomic.AtomicLong;

public class App {
	private static final AtomicLong value = new AtomicLong();

	public String toString() {
        return Long.toString(value.get());
    }


    public long next() {
        return value.incrementAndGet();
    }

    public static void main(String[] args) {
        for (int i = 0; i < 32; i++) {
            new Thread() {
                final Logger logger = LogManager.getLogger(App.class);
                final App instance = new App();

                @Override 
                public void run() {
                    for (int i = 0; i < 100000; i++) {
                        logger.warn("{} == {}", instance.next(), instance);
                    }
                }
            }.start();
        }
    }
}
```

Now run this code...

Here is the first few lines of logging output

```
2014-07-28 15:59:45,729 WARN t.App [Thread-13] 13 == 13 
2014-07-28 15:59:45,730 WARN t.App [Thread-29] 29 == 29 
2014-07-28 15:59:45,729 WARN t.App [Thread-15] 15 == 15 
2014-07-28 15:59:45,729 WARN t.App [Thread-6] 6 == 6 
2014-07-28 15:59:45,730 WARN t.App [Thread-30] 30 == 30 
2014-07-28 15:59:45,729 WARN t.App [Thread-20] 20 == 20 
2014-07-28 15:59:45,729 WARN t.App [Thread-8] 8 == 8 
2014-07-28 15:59:45,730 WARN t.App [Thread-28] 28 == 28 
2014-07-28 15:59:45,729 WARN t.App [Thread-19] 19 == 19 
2014-07-28 15:59:45,729 WARN t.App [Thread-18] 18 == 18 
2014-07-28 15:59:45,729 WARN t.App [Thread-5] 5 == 6 
2014-07-28 15:59:45,731 WARN t.App [Thread-13] 33 == 37 
2014-07-28 15:59:45,731 WARN t.App [Thread-8] 39 == 39 
2014-07-28 15:59:45,731 WARN t.App [Thread-28] 40 == 41 
2014-07-28 15:59:45,731 WARN t.App [Thread-18] 42 == 43 
2014-07-28 15:59:45,731 WARN t.App [Thread-5] 43 == 43
```

Spot anything wrong with that?

Now of course I have written the class to have mutable state… because I wanted to test if Log4J 2.0 was capturing the `toString()`` at the time of logging… which it isn’t.

So if you have an object with a `toString()`` method that depends on mutable state, you will have to:

* Check that the logger is enabled for the logging level

* Call `toString()` by hand

* Pass the `toString()` result as the parameter.

To make my previous code work with Asynchronous loggers (other than by fixing the mutable state) I would need to log like this:

```java
if (logger.isWarnEnabled()) {
    logger.warn("{} == {}", instance.next(), instance.toString()); 
}
```

Yep, we are back to that old pattern.

TL;DR Unless you know that *every* parameter object passed to a log statement is using immutable objects, enabling Asynchronous loggers in Log4J may well result in logs with messages you cannot trust.

### Update

Here is the log4j2.xml configuration file I used

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Don't forget to set system property-DLog4jContextSelector=org.apache.logging.log4j.core.async.AsyncLoggerContextSelector to make all loggers asynchronous. -->
<Configuration status="WARN">
  <Appenders>
    <!-- Async Loggers will auto-flush in batches, so switch off immediateFlush. -->
    <RandomAccessFile name="RandomAccessFile" fileName="async.log" immediateFlush="false" append="false">
      <PatternLayout>
        <Pattern>%d %p %c{1.} [%t] %m %ex%n</Pattern>
      </PatternLayout>
    </RandomAccessFile>
  </Appenders>
  <Loggers>
    <Root level="info" includeLocation="false">
      <AppenderRef ref="RandomAccessFile"/>
    </Root>
  </Loggers>
</Configuration>
```

Which is the example on the [Log4j Website](http://logging.apache.org/log4j/2.x/manual/async.html#AllAsync)