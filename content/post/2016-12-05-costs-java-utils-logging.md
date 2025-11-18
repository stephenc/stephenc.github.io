---
title: "The costs of Java Utils Logging"
date: 2016-12-05T00:00:00Z
tags: ["Java"]
---

One of my colleagues had a question:

Now for some context, when the Jenkins project started off, Kohsuke was working for Sun and felt it would be wrong, as a Sun employee, to use a logging framework other than that provided by the JVM as using a different logging framework could be seen as being implication that the built in Java Utils Logging framework was a steaming pile of excrement.

Now while JUL is not a complete and utter steaming pile of excrement, at times it does indeed throw shades at being one.

**This post is not a defence of Java Utils Logging. This post is an analysis of how to use Java Utils Logging such that performance does not end up down the toilet.**

When you are using Java Utils Logging there are many many ways to actually log something:

```java
// simple style

LOGGER.info("A message");

// explicit level style

LOGGER.log(Level.INFO, "A message");

// explicit level and stack trace

LOGGER.log(Level.INFO, "A message with a stack trace", e);

// explicit level and single parameter

LOGGER.log(Level.INFO, "A message with a {0} parameter", param);

// explicit level and multiple parameters

LOGGER.log(Level.INFO, "A message with parameter {0} and {1}", new Object[]{param0,param1});

// explicit level, stack trace and parameter(s)

LogRecord lr = new LogRecord(Level.INFO, "A message with parameter {0} and {1} and a stack trace");

lr.setThrown(e);

lr.setParams(new Object[]{param0,param1});

LOGGER.log(lr);
```

Now each of the above achieves basically the same thing, sending a message to the logs under differing use cases. The LOGGER.info() variant is intended to be used when you have a constant message to report... but invariably somebody starts doing the easy string concatenation with that style, rather than use the parameterised logging as the JUL framework intended, so you will sometimes see:

```java
LOGGER.info("Accepted incoming connection #" + connectionNumber + " from " + socket.getAddress() + " and processing with " + handler); 
```

Rather than

```java
LOGGER.log(Level.INFO, "Accepted incoming connection #{0} from {1} and processing with {2}", new Object[]{connectionNumber,socket.getAddress(),handler});
```

At the INFO level (which is normally logged by default) this may not be as critical, but once we move the code from development to production and notch the levels down the difference can be an order of magnitude or more.

The reason becomes clear when we look at the source code for Logger:

```java
/**
 * Log a message, with no arguments.
 * <p>
 * If the logger is currently enabled for the given message
 * level then the given message is forwarded to all the
 * registered output Handler objects.
 * <p>
 * @param level One of the message level identifiers, e.g., SEVERE
 * @param msg The string message (or a key in the message catalog)
 */
public void log(Level level, String msg) {
    if (!isLoggable(level)) {
        return;
    }
    LogRecord lr = new LogRecord(level, msg);
    doLog(lr);
}

/**
 * Log a message, with an array of object arguments.
 * <p>
 * If the logger is currently enabled for the given message
 * level then a corresponding LogRecord is created and forwarded
 * to all the registered output Handler objects.
 * <p>
 * @param level One of the message level identifiers, e.g., SEVERE
 * @param msg The string message (or a key in the message catalog)
 * @param params array of parameters to the message
 */
public void log(Level level, String msg, Object params[]) {
    if (!isLoggable(level)) {
        return;
    }
    LogRecord lr = new LogRecord(level, msg);
    lr.setParameters(params);
    doLog(lr);
}

/**
 * Log an INFO message.
 * <p>
 * If the logger is currently enabled for the INFO message
 * level then the given message is forwarded to all the
 * registered output Handler objects.
 * <p>
 * @param msg The string message (or a key in the message catalog)
 */
public void info(String msg) {
    log(Level.INFO, msg);
}
```

So that LOGGER.info() call requires that we build up the string first, and only after the string has been instantiated do we check if the logger is logging that level whereas the parameterised message just passes the string constant and the object array but doesn't do much actual work.

One would hope, given sufficient time, that the LOGGER.log(level,msg) call would also get inlined and the JVM might be smart enough to re-order the isLoggable check ahead of the string concatenation and everything would be equal *in the long run*.

Well, that's a nice theory, but users would need to wait for that to occur, plus your log statements are likely in the middle of large methods anyway and the Logger methods are not final so the JVM would need to put in some guards *just in case somebody loaded a Logger subclass that would invalidate the optimisation*. 

So what is the impact anyway?

Enter [JMH](http://openjdk.java.net/projects/code-tools/jmh/) we can run a micro-benchmark to see what the different styles perform like **when our logger is not logging**.

Firstly we need to grab a baseline:

```java
public class JulBenchmark {

    private static final Logger LOGGER = Logger.getLogger(JulBenchmark.class.getName());

    static long time;

    @Benchmark
 public void noLogging(Blackhole blackhole) {
        time++;
        blackhole.consume(time);
    }

 @Benchmark
 public void blackholeStringConcat(Blackhole blackhole) {
        blackhole.consume("Started at " + new Date(time));
        time++;
        blackhole.consume(time);
    }

 @Benchmark
 public void blackholeStringFormat(Blackhole blackhole) {
        blackhole.consume(String.format("Started at %tc", time));
        time++;
        blackhole.consume(time);
    }

 @Benchmark
 public void blackholeSimpleArray(Blackhole blackhole) {
        blackhole.consume(new Object[]{time});
        time++;
        blackhole.consume(time);
    }

 @Benchmark
 public void blackholeDateArray(Blackhole blackhole) {
        blackhole.consume(new Object[]{new Date(time)});
        time++;
        blackhole.consume(time);
    }

}
```

In each of our benchmarks, we pass through the blackhole and we consume the time static field with it so that the time differences we observe are all just for the statements above the time++ and by incrementing the time value we prevent the JVM from optimising concatenation to a constant string value.

The results:

```
Benchmark                                      Mode  Cnt          Score          Error  Units
JulBenchmark.blackholeDateArray               thrpt   20   97371938.780 ±  2903787.552  ops/s
JulBenchmark.blackholeSimpleArray             thrpt   20  100902747.726 ±  1383605.583  ops/s
JulBenchmark.blackholeStringConcat            thrpt   20    3727524.654 ±    62280.481  ops/s
JulBenchmark.blackholeStringFormat            thrpt   20     601454.586 ±     5689.042  ops/s
JulBenchmark.noLogging                        thrpt   20  366202499.287 ± 13837552.431  ops/s
```

So creating an Array just to throw it down the black hole is two orders of magnitude better than building a string to be thrown down the black hole which is an order of magnitude better than using String.format. It doesn't really matter whether our array creation even included wrapping the long as a Date.

Our alarm bells should be ringing rather loudly by now... that String concatenation is a horrific cost to pay and the array creation is really quite cheap compared to doing nothing.

Now let's look at what happens if we do some logging at a level that goes nowhere:

```java
@Benchmark
public void helperStringConcat(Blackhole blackhole) {
    LOGGER.fine("Started at " + new Date(time));
    time++;
    blackhole.consume(time);
}

@Benchmark
public void levelStringConcat(Blackhole blackhole) {
    LOGGER.log(Level.FINE, "Started at " + new Date(time));
    time++;
    blackhole.consume(time);
}

@Benchmark
public void levelMessage1Arg_custom(Blackhole blackhole) {
    LOGGER.log(Level.FINE, "Started at {0,date,EEE MMM dd HH:mm:ss zzz yyyy}", time);
    time++;
    blackhole.consume(time);
}

@Benchmark
public void levelMessage1Arg_date(Blackhole blackhole) {
    LOGGER.log(Level.FINE, "Started at {0}", new Date(time));
    time++;
    blackhole.consume(time);
}

@Benchmark
public void levelMessageNArg_custom(Blackhole blackhole) {
    LOGGER.log(Level.FINE, "Started at {0,date,EEE MMM dd HH:mm:ss zzz yyyy}", new Object[]{time});
    time++;
    blackhole.consume(time);
}

@Benchmark
public void levelMessageNArg_date(Blackhole blackhole) {
    LOGGER.log(Level.FINE, "Started at {0}", new Object[]{new Date(time)});
    time++;
    blackhole.consume(time);
}
```

So what does the benchmark say for these?

```
Benchmark                                      Mode  Cnt          Score          Error  Units
JulBenchmark.helperStringConcat               thrpt   20    3878438.607 ±    57378.392  ops/s
JulBenchmark.levelMessage1Arg_custom          thrpt   20  166976758.162 ±  6073258.725  ops/s
JulBenchmark.levelMessage1Arg_date            thrpt   20  267808265.736 ±  4607295.478  ops/s
JulBenchmark.levelStringConcat                thrpt   20    3904071.260 ±   112723.048  ops/s
JulBenchmark.levelMessageNArg_custom          thrpt   20  167622786.200 ±  3108069.452  ops/s
JulBenchmark.levelMessageNArg_date            thrpt   20  178923942.807 ±  2145153.495  ops/s
```

So as we feared... that String concatenation is killing our performance... 

But what is going on with the single arg date... let's take a look at the bytecode:

```
      public void levelMessage1Arg_custom(org.openjdk.jmh.infra.Blackhole);
        descriptor: (Lorg/openjdk/jmh/infra/Blackhole;)V
        flags: ACC_PUBLIC    Code:      stack=5, locals=2, args_size=2
             0: getstatic     #4                  // Field LOGGER:Ljava/util/logging/Logger;
             3: getstatic     #15                 // Field java/util/logging/Level.FINE:Ljava/util/logging/Level;
             6: ldc           #22                 // String Started at {0,date,EEE MMM dd HH:mm:ss zzz yyyy}
             8: getstatic     #2                  // Field time:J
            11: invokestatic  #19                 // Method java/lang/Long.valueOf:(J)Ljava/lang/Long;
            14: invokevirtual #23                 // Method java/util/logging/Logger.log:(Ljava/util/logging/Level;Ljava/lang/String;Ljava/lang/Object;)V
            17: getstatic     #2                  // Field time:J
            20: lconst_1
            21: ladd
            22: putstatic     #2                  // Field time:J
            25: aload_1
            26: getstatic     #2                  // Field time:J
            29: invokevirtual #3                  // Method org/openjdk/jmh/infra/Blackhole.consume:(J)V
            32: return
          LineNumberTable:
            line 110: 0
            line 111: 17
            line 112: 25
            line 113: 32
          LocalVariableTable:
            Start  Length  Slot  Name   Signature
                0      33     0  this   Lcom/onedash/JulBenchmark;
                0      33     1 blackhole   Lorg/openjdk/jmh/infra/Blackhole;
        RuntimeVisibleAnnotations:
          0: #53()
```

And Long.valueOf looks like

```java
public static Long valueOf(long l) {
    final int offset = 128;
    if (l >= -128 && l <= 127) { // will cache
return LongCache.cache[(int)l + offset];
    }
    return new Long(l);
}
```

I wonder what would happen if we ignored the cache...

```java
@Benchmark
public void levelMessage1Arg_customWAT(Blackhole blackhole) {
    LOGGER.log(Level.FINE, "Started at {0,date,EEE MMM dd HH:mm:ss zzz yyyy}", new Long(time));
    time++;
    blackhole.consume(time);
}

@Benchmark
public void levelMessageNArg_customWAT(Blackhole blackhole) {
    LOGGER.log(Level.FINE, "Started at {0,date,EEE MMM dd HH:mm:ss zzz yyyy}", new Object[]{new Long(time)});
    time++;
    blackhole.consume(time);
}
```

If we look at the benchmarks for those:

```
Benchmark                                      Mode  Cnt          Score          Error  Units
JulBenchmark.levelMessage1Arg_customWAT       thrpt   20  273177646.084 ±  7367926.789  ops/s
JulBenchmark.levelMessageNArg_customWAT       thrpt   20  178868531.695 ±  8171421.563  ops/s
```

So bypassing the auto-boxing and using explicit boxing of a Long is actually about 7% faster when you are putting the Long in an array... but when passed using the single argument helper, explicit boxing is 63% faster!

I wonder if somebody should tell IntelliJ to quit whining!

Finally, what about if we move the guard out explicitly:

```java
@Benchmark
public void guardedLevelMessageNArg(Blackhole blackhole) {
    if (LOGGER.isLoggable(Level.FINE)) {
        LOGGER.log(Level.FINE, "Started at {0,date,EEE MMM dd HH:mm:ss zzz yyyy}", new Object[]{new Long(time)});
    }
    time++;
    blackhole.consume(time);
}
```

What does that benchmark like:

```
Benchmark                              Mode  Cnt          Score         Error  Units
JulBenchmark.guardedLevelMessageNArg  thrpt   20  295175956.393 ± 5381049.710  ops/s
```

OK, so back to Baptiste's original question:

- The arrays are actually very cheap, at least compared to auto-boxing of say longs
- The LOGGER.info() style is just not worth the risk, always give the level that makes it easier to switch to parameterized.
- When not being logged, JUL logging can be very cheap e.g. compare noLogging benchmark with levelMessage1Arg_date or levelMessage1Arg_customWAT where we saw our throughput only drop by about 25%. This compares quite favourably with guardedLevelMessageNArg which only has a drop of 20%

My recommendations are thus:

**IF YOU HAVE TO USE Java Utils Logging**

1. Bash people on the head so you can use a better logging framework
2. Never use the LOGGER.info() style statements, too risky that somebody will be lazy and concatenate something in there
3. In regular code: Don't worry about the array creation
4. In proven hot-spot code where logging defaults to off: Wrap all logging statements with a guard of (LOGGER.isLoggable(Level.___)) { ... }. If you have multiple guards in the same method, extract the level check to a local variable.

And please remember point #1
