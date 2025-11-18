---
title: "About test coverage"
date: 2013-04-19T00:00:00Z
---

I was given a link to yet another article preaching about how 100% code coverage is the only goal (the article is preaching, not Tatu BTW)

{{< x "cowtowncoder" "325060869052575747" >}}

There is an issue I have with how the 100% coverage advocates present their argument, but we'll get to that later.

The case for 100% coverage is put quite simply:

> Anything less than 100% coverage means that there are some lines in your code that are untested, and are you seriously willing to let code be released without being tested?
> 
> Now if your code is 100 lines long, and you have 95% coverage, 5 lines doesn't seem too bad. In fact looking at the code coverage report you see those 5 lines, and you make a judgement call that they are an acceptable risk. No harm done, right?
> 
> When the code grows to 1,000 lines long, 95% coverage is giving you less of that warm and fuzzy feeling, but a quick scan of the coverage report and you can visually check the 50 lines untested, and you make a judgement call that they are an acceptable risk. No harm done, right?
> 
> With a 10,000+ LOC code base and 95% coverage and your boss wants to know if it is OK to push this code into production now, the 500+ uncovered lines that you need to review are now much more than a headache…

Are you a convert now? Do you believe in 100% coverage? It's a nice argument. But there is a flaw… in some cases that is!

When you are dealing with a dynamically typed language, especially some of the more expressive ones, the only tests you can have are the tests you write yourself. In those languages, the 100% coverage zealots have me sold (at least for code that needs to be maintained and is longer than 100 lines or so!)

But in different languages we can, and do, have additional tests that are provided by tooling:

* Syntax tests that verify that every line of code is syntactically correct

* Scoping tests (in languages that force declaring names before first use within a scope) that verify that each line only accesses those names within the correct scope for the line.

* Type tests (in statically typed languages)

And that's not all… most of the code I write runs on the JVM, there are more tests I can add to the mix when on the JVM

* Static analysis tools, such as Checkstyle, PMD and Findbugs provide an additional set of tests that I can run automatically on my code looking for common problems and possible mistakes. In fact I've found and fixed bugs with Findbugs in code that had 100% coverage already.

* Annotation's in code can be used to, not only document the code contracts, but aid and assist Findbugs in catching bugs. Specifically I am referring to the `@CheckForNull` and `@NonNull` annotations. I apply these annotations to the production code, and there are tests applied to the code for free by the toolchain I use

So when I am writing Java code, every line I write already has at least five tests covering it **and** I haven't even started adding unit tests into the mix!

Now I am not arguing that the above tests are enough for your code on it's own… but when you look at my *unit test* coverage at 83.7% and ask am I "happy to ship with 1,630 untested lines of code", I will answer that those 1,630 lines of code are tested, they may not be our best tests, but we have tests on them.

Show me a real code base with 100% coverage, and I will show you a good number of crappy tests helping that code base get to 100% coverage...

On the other hand, if you ask me am I happy to ship that Ruby on Rails / Node.JS / etc application into production with 99.5% coverage, I'll say no way are we shipping that code with 50 untested LOC.