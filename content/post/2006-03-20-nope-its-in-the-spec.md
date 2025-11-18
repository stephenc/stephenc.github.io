---
title: "Nope, it's in the spec"
date: 2006-03-20T02:00:00Z
---

From the spec:

> The deployment tool must first read the Java EE application deployment descriptor from the application `.ear` file (`META-INF/application.xml`). If the deployment descriptor is present, it fully specifies the modules included in the application. If no deployment descriptor is present, the deployment tool uses the following rules to determine the modules included in the application.

It would be nice if glassfish gave some warning that your `application.xml` might not be completely specified!