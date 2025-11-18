---
title: "The costs of guarding logging with Apache Log4J version 2"
date: 2016-12-05T00:00:00Z
tags: ["Java"]
---

Another interesting tidbit:

```java
@Benchmark
public void debug1Arg_date(Blackhole blackhole) {
    LOGGER.debug("Started at %s", new Date(time));
    time++;
    blackhole.consume(time);
}

@Benchmark
public void guardedDebug1Arg_date(Blackhole blackhole) {
    if (LOGGER.isDebugEnabled()) {
        LOGGER.debug("Started at %s", new Date(time));
    }
    time++;
    blackhole.consume(time);
}
```

Gives the following benchmark results:

```
Benchmark                            Mode  Cnt          Score         Error  Units
Log4jBenchmark.debug1Arg_date         thrpt   20  179653191.248 ± 2731044.349  ops/s
Log4jBenchmark.guardedDebug1Arg_date  thrpt   20  207001790.376 ± 2074020.617  ops/s
```

We can also compare guarding with SLF4J over logback

```
Benchmark                              Mode  Cnt          Score         Error  Units
SLF4JBenchmark.debug1Arg_date         thrpt   20  220765608.629 ± 6555782.899  ops/s
SLF4JBenchmark.guardedDebug1Arg_date  thrpt   20  241286730.504 ± 9532328.812  ops/s
```

So where performance is critical, seems to be about 10% faster if you guard that log statement!
