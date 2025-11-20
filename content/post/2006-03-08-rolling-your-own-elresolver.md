---
title: "Rolling your own ELResolver"
date: 2006-03-08T03:00:00Z
---

ELResolvers are where you get to extend the new unified EL for your own pages. They are not that difficult to extend, it's just a case of:  

1. Have your class extend from `ELResolver` 
2. Implement the abstract methods 
3. Add an `<el-resolver>` element to your `<application>` section in `faces-config.xml`
4. Start using your resolver!  

OK, so why would you want to do this? Well, for one it can make some things a lot easier. I was driven to find this solution in order to dynamically generate h:dataTables with variable numbers of columns.  Ordinarily you would need to bind the h:dataTable to a backing bean and have the backing bean add in the extra columns, but with `c:forEach` now being compatible with JSF, we have an alternative.  

Here's the model of the data we are trying to present: (the classes are coming from EJB entities which are mapping to a legacy database)

```java
  public class Result { 
  	// ...
  	private Sample sample;
  	private ResultType resultType;
  	private String value;
  	// ...  
  }  

  public class Sample { 
  	// ...
  	private String name;
  	private Collection<Result> results;
  	// ... 
  }  

  public class Project {
   // ... 
   private String name; 
   private Collection<Sample> samples;
   // ... 
}
```

We want to display a results table for all the samples from the project object we have been passed... it should look something like

| Sample | TypeA | TypeB | TypeC | ... |
|--------|-------|-------|-------|-----|
| 1      | ...   | ...   | ...   | ... |
| 2      | ...   | ...   | ...   | ... |
| ...    | ...   | ...   | ...   | ... |

where there are as many columns as there are types.  We add a method to the project class that returns `Collection<ResultType>`  and what we'd like to do is:

```xml
<h:dataTable value="#{project.samples}" var="sample">
  <h:column>
    <h:outputText value="#{sample.name}"/>
  </h:column>
  <c:forEach items="#{project.resultTypes}" var="resultType">
    <h:column>
      <h:outputText value="#{sample.results[resultType].value}"/>
    </h:column>
  </c:forEach>
</h:dataTable>
```

Normally this would only work if `sample.results` is a `Map<String,Result>` and each `ResultType` can be converted into a string that happens to be the key of the map. We end up writing a wrapper class for a `Map` and since we've been given a collection and not a map, efficiency is not the best.  

But a custom `ELResolver` can help us:  

I'll post more when I have simplified my resolver to fit this example