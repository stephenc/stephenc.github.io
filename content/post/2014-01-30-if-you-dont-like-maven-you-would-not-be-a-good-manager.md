---
title: "If you don't like Maven, you would not be a good manager..."
date: 2014-01-30T00:00:00Z
---

We have all had the bad technical managers… the ones who tell you to go and do something… and then micromanage the task they have “delegated” to you.

They are a pain to work for.

One of the qualities of a good manager is to tailor their delegation to the people they are delegating to.

So they task Gillian, a senior engineer, with “writing some smoke tests to verify that the application works when deployed to the app server” and they are happy to let Gillian work within that scope because they trust that Gillian will come back to seek clarification if the description is lacking, or if there are issues down the road.

Kevin, a junior engineer, on the other hand, has proven over many many tasks to need more detail, so they give Kevin a more detailed written description of the task and they check in on Kevin as he is going along… because Kevin has proven that he needs a certain level of micromanagement… the good manager is all the time testing to see if Kevin can survive with less micromanagement.

Note: one of the biggest cognitive distortions of bad managers is the thinking that in order to treat everyone fairly, you must treat everyone equally. If we did that then either Gillian gets micromanaged which is unfair to Gillian or Kevin gets under-managed which is unfair to Kevin.

So, what does all that have to do with liking Maven?

Well Maven is a build tool. If you need Maven to build a .war file, you should just tell it to build a .war file

```xml
<project>
    <groupId>…</groupId>
    <artifactId>…</artifactId>
    <version>…</version>
    <packaging>war</packaging>
    <dependencies>
        ...
    </dependencies>
</project>
```

Why do you want to micromanage Maven and tell it every little thing it must do to build the .war file. Wait until you see what it did with your instructions, then and only then should you refine your instructions.

So… If you don't like Maven, you would not be a good manager… The corollaries are not necessarily true though...

* Liking Maven does not mean you will be a good manager… there are other qualities that make a good manager… understanding when and how to micromanage is only one of those qualities

* Being a good manager does not mean you will like Maven… for example if all your developers (who love to micromanage and thankfully are not managers because of their micromanagement adoration) tell you that Maven is a pain… well a good manager will hear what their team is saying and take it on board… after all they are there to manage, not to do… if they were to see a Maven build where it has not been micromanaged by the developers, then a different view they will form.