---
title: "The costs of other logging frameworks"
date: 2016-12-05T00:00:00Z
tags: ["Java"]
---

You asked for it.

Logback:

```java
@Benchmark
public void debug1Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at {}", new Date(time));
    time++;
    blackhole.consume(time);
}
@Benchmark
public void debug2Arg_date(Blackhole blackhole) {

    LOGGER.debug("Started at {}", new Date(time), null);
    time++;
    blackhole.consume(time);
}
@Benchmark
public void debugNArg_date(Blackhole blackhole) {
    LOGGER.debug("Started at {}", new Date(time), null, null);
    time++;
    blackhole.consume(time);
}
static {

    ch.qos.logback.classic.Logger root = (ch.qos.logback.classic.Logger)LoggerFactory.getLogger(org.slf4j.Logger.ROOT_LOGGER_NAME);
    root.setLevel(ch.qos.logback.classic.Level.INFO);
}
```

And the benchmarks

```
Benchmark                     Mode  Cnt          Score         Error  Units 
LogbackBenchmark.debug1Arg_date  thrpt   20  221056534.656 ± 8549233.826  ops/s
LogbackBenchmark.debug2Arg_date  thrpt   20  220576341.742 ± 3778270.898  ops/s
LogbackBenchmark.debugNArg_date  thrpt   20  134887126.088 ± 2973182.812  ops/s
```

JUL over SLF4J (same benchmark code but different dependency)

```
Benchmark                     Mode  Cnt          Score         Error  Units 
SLF4JOverJULBenchmark.debug1Arg_date  thrpt   20  213779286.286 ± 4819012.495  ops/s
SLF4JOverJULBenchmark.debug2Arg_date  thrpt   20  213707271.979 ± 2675083.826  ops/s
SLF4JOverJULBenchmark.debugNArg_date  thrpt   20  152839334.058 ± 2122611.858  ops/s
```

Then if we compare the JUL LogRecord implicitly:

```java
@Benchmark
public void logRecord(Blackhole blackhole) {
    LogRecord lr = new LogRecord(Level.FINE, "Started at {0}");
    lr.setParameters(new Object[]{new Date(time)});
    LOGGER.log(lr);
    time++;
    blackhole.consume(time);
}
```

This has the following Benchmark

```
Benchmark                Mode  Cnt         Score        Error  Units 
JulBenchmark.logRecord  thrpt   20  16422331.419 ± 148428.926  ops/s
```

**DO NOT USE AN UNGUARDED LogRecord WHEN IT WILL LIKELY NOT GET LOGGED**

Finally, Apache's Log4J version 2 (which has overrides to avoid var-args all the way up to 10 parameters):

```java
@Benchmark
public void debug1Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time));
    time++;
    blackhole.consume(time);
}

@Benchmark
public void debug2Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time), null);
    time++;
    blackhole.consume(time);
}

@Benchmark
public void debug3Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time), null, null);
    time++;
    blackhole.consume(time);
}

@Benchmark
public void debug4Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time), null, null, null);
    time++;
    blackhole.consume(time);
}

@Benchmark
public void debug5Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time), null, null, null, null);
    time++;
    blackhole.consume(time);
}

@Benchmark
public void debug6Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time), null, null, null, null, null);
    time++;
    blackhole.consume(time);
}

@Benchmark
public void debug7Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time), null, null, null, null, null, null);
    time++;
    blackhole.consume(time);
}

@Benchmark
public void debug8Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time), null, null, null, null, null, null, null);
    time++;
    blackhole.consume(time);
}

@Benchmark
public void debug9Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time), null, null, null, null, null, null, null, null);
    time++;
    blackhole.consume(time);
}

@Benchmark
public void debug10Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time), null, null, null, null, null, null, null, null, null);
    time++;
    blackhole.consume(time);
}

@Benchmark
public void debugNArg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time), null, null, null, null, null, null, null, null, null, null);
    time++;
    blackhole.consume(time);
}
```

And the benchmarks:

```
Benchmark                         Mode  Cnt          Score         Error  Units 
Log4j2Benchmark.debug1Arg_date   thrpt   20  182786163.176 ± 1894038.335  ops/s
Log4j2Benchmark.debug2Arg_date   thrpt   20  180716268.151 ± 5295999.398  ops/s
Log4j2Benchmark.debug3Arg_date   thrpt   20  178064841.181 ± 6987288.015  ops/s
Log4j2Benchmark.debug4Arg_date   thrpt   20  181537704.811 ± 4472120.312  ops/s
Log4j2Benchmark.debug5Arg_date   thrpt   20  181803075.728 ± 3963211.935  ops/s
Log4j2Benchmark.debug6Arg_date   thrpt   20  178229873.962 ± 8092548.001  ops/s
Log4j2Benchmark.debug7Arg_date   thrpt   20  181018788.479 ± 5438279.737  ops/s
Log4j2Benchmark.debug8Arg_date   thrpt   20  180443652.287 ± 4965518.359  ops/s
Log4j2Benchmark.debug9Arg_date   thrpt   20  181456134.533 ± 2014764.085  ops/s
Log4j2Benchmark.debug10Arg_date  thrpt   20  176706451.426 ± 7911521.599  ops/s
Log4j2Benchmark.debugNArg_date   thrpt   20  123243343.482 ± 2051852.105  ops/s
```

So *for the logs not logged* we have the following:

- Fastest is JUL with single argument
- Second fastest is SLF4J with one or two arguments (Logback is ever so slightly ahead but it's splitting hairs)
- Third place is Apache Log4J version 2 with up to 10 arguments
- Forth place is JUL for more than 1 argument
- Fifth place is SLF4J over JUL with more than 2 arguments
- Sixth is Logback with more than 2 arguments
- Last place is Apache Log4J with more than 10 arguments

Pick your poison... and we have not considered the *perhaps more important* performance when actually logging!
