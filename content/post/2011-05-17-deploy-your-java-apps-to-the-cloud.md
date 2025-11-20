---
title: "Deploy your java apps to the cloud"
date: 2011-05-17T00:00:00Z
tags: ["CloudBees"]
---

I work for [CloudBees Inc.](http://www.cloudbees.com/), they are a great company with great products. I have mostly been working on the [DEV@](http://www.cloudbees.com/dev.cb) side of the fence which is focused on continuous integration and basically the development side of your application, but we also have the [RUN@](http://www.cloudbees.com/run.cb) side of the fence where we provide a [platform as a service (PaaS)](http://en.wikipedia.org/wiki/Platform_as_a_service) for running your java web applications on the cloud. I could give you the sales pitch, but I'll leave it at: the technologies and people behind RUN@ were one of the key reasons why I decided to join CloudBees.

Well I've been busy on [some stuff](http://nectar.cloudbees.com/products-features-scale.cb#rbac) since joining, so I decided it was time to actually try out the RUN@ stuff for my self. So here is my experience:

My test application:

I'm on the [Apache Maven PMC](http://maven.apache.org/), so I'm going to build it with... shock... horror... Maven.

I am partial to the odd bit of JSF, so it will be a JSF 2.0 application based off of [Apache MyFaces](http://myfaces.apache.org/).

I love [Jetty](http://eclipse.org/jetty/) as a servlet container for local testing, so we'll use that hammer too.

Let's get started...

First the pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- basic information -->

    <groupId>com.blogspot.javaadventure.cloudbees.run</groupId>
    <artifactId>jsf2-hello-world</artifactId>
    <version>0.1-SNAPSHOT</version>
    <packaging>war</packaging>

    <!-- Project information -->

    <name>JSF 2.0 Hello World</name>
    <description>
        A JSF 2.0 web application that says hello world.
    </description>
    <properties>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <project.build.outputEncoding>UTF-8</project.build.outputEncoding>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <!-- Dependency details -->
    <dependencies>
        <dependency>
            <groupId>org.apache.myfaces.core</groupId>
            <artifactId>myfaces-api</artifactId>
            <version>2.0.5</version>
        </dependency>
        <dependency>
            <groupId>org.apache.myfaces.core</groupId>
            <artifactId>myfaces-impl</artifactId>
            <version>2.0.5</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.8.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <!-- Build settings -->
    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <artifactId>maven-clean-plugin</artifactId>
                    <version>2.4.1</version>
                    </plugin>
                <plugin>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>2.3.2</version>
                    <configuration>
                    <source>1.6</source>
                    <target>1.6</target>
                    </configuration>
                </plugin>
                <plugin>
                    <artifactId>maven-deploy-plugin</artifactId>
                    <version>2.6</version>
                </plugin>
                <plugin>
                    <artifactId>maven-failsafe-plugin</artifactId>
                    <version>2.8.1</version>
                    <executions>
                        <execution>
                            <goals>
                                <goal>integration-test</goal>
                                <goal>verify</goal>
                            </goals>
                        </execution>
                    </executions>
                </plugin>
                <plugin>
                    <artifactId>maven-install-plugin</artifactId>
                    <version>2.3.1</version>
                </plugin>
                <plugin>
                    <artifactId>maven-jar-plugin</artifactId>
                    <version>2.3.1</version>
                </plugin>
                <plugin>
                    <artifactId>maven-surefire-plugin</artifactId>
                    <version>2.8.1</version>
                </plugin>
                <plugin>
                    <artifactId>maven-release-plugin</artifactId>
                    <version>2.1</version>
                </plugin>
                <plugin>
                    <artifactId>maven-resources-plugin</artifactId>
                    <version>2.5</version>
                </plugin>
                <plugin>
                    <groupId>org.mortbay.jetty</groupId>
                    <artifactId>jetty-maven-plugin</artifactId>
                    <version>8.0.0.M2</version>
                </plugin>
            </plugins>
        </pluginManagement>
        <plugins>
            <plugin>
            <artifactId>maven-release-plugin</artifactId>
            <configuration>
                <autoVersionSubmodules>true</autoVersionSubmodules>
                <goals>install</goals>
            </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

Then the `src/main/webapp/WEB-INF/web.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app version="2.5" xmlns="http://java.sun.com/xml/ns/javaee"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd">
    <display-name>JSF 2.0 Hello World</display-name>
    <description>
        A JSF 2.0 web application that says hello world.
    </description>
    <context-param>
        <param-name>javax.faces.STATE_SAVING_METHOD</param-name>
        <param-value>server</param-value>
    </context-param>
    <context-param>
        <param-name>javax.faces.DEFAULT_SUFFIX</param-name>
        <param-value>.xhtml</param-value>
    </context-param>
    <context-param>
        <param-name>javax.faces.FACELETS_SKIP_COMMENTS</param-name>
        <param-value>true</param-value>
    </context-param>
    <context-param>
        <param-name>javax.faces.PROJECT_STAGE</param-name>
        <param-value>Production</param-value>
        <!--param-value>Development</param-value-->
    </context-param>
    <!-- [jetty] does not initialize myfaces correctly for some reason -->
    <listener>
        <listener-class>org.apache.myfaces.webapp.StartupServletContextListener</listener-class>
    </listener>
    <!-- [/jetty] -->
    <servlet>
        <servlet-name>Faces Servlet</servlet-name>
        <servlet-class>javax.faces.webapp.FacesServlet</servlet-class>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>Faces Servlet</servlet-name>
        <url-pattern>*.xhtml</url-pattern>
    </servlet-mapping>
    <session-config>
        <session-timeout>60</session-timeout>
    </session-config>
    <welcome-file-list>
        <welcome-file>index.xhtml</welcome-file>
    </welcome-file-list>
</web-app>
```

Then the backing bean (`src/main/java/com/blogspot/javaadventure/cloudbees/run/GreeterBean.java)

```java
package com.blogspot.javaadventure.cloudbees.run;

import javax.faces.bean.ManagedBean;
import javax.faces.bean.ViewScoped;
import java.io.Serializable;

@ManagedBean(name="greeter")
@ViewScoped
public class GreeterBean implements Serializable {
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getResponse() {
        if (name != null && !name.isEmpty()) {
            return "Hello " + name;
        } else {
            return null;
        }
    }
}
```

Should always have some tests (`src/test/java/com/blogspot/javaadventure/cloudbees/run/GreeterBeanTest.java`)

```java
package com.blogspot.javaadventure.cloudbees.run;

import org.junit.Test;
import static org.hamcrest.CoreMatchers.*;
import static org.junit.Assert.*;

public class GreeterBeanTest {
    @Test
    public void nullNameMeansNoGreeting() throws Exception {
        GreeterBean instance = new GreeterBean();
        instance.setName(null);
        assertThat(instance.getResponse(), nullValue());
    }

    @Test
    public void noNameMeansNoGreeting() throws Exception {
        GreeterBean instance = new GreeterBean();
        instance.setName("");
        assertThat(instance.getResponse(), nullValue());
    }

    @Test
    public void aNameMeansGreeting() throws Exception {
        GreeterBean instance = new GreeterBean();
        instance.setName("Fred");
        assertThat(instance.getResponse(), notNullValue());
    }
}
```

Next the page of our web application (`src/main/webapp/index.xhtml`), i'm going to use the JSF 2.0 ajax support (because it's there)

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
        xmlns:ui="http://java.sun.com/jsf/facelets"
        xmlns:h="http://java.sun.com/jsf/html"
        xmlns:f="http://java.sun.com/jsf/core">
    <ui:insert name="metadata"/>
    <h:head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>
            JSF 2.0 Hello World
        </title>
    </h:head>
    <h:body>
        <f:view>
            <h:form>
                <h:outputLabel for="greeter" value="Please tell me your name:"/>
                <h:inputText id="greeter" value="#{greeter.name}">
                    <f:ajax event="keyup" render="text"/>
                </h:inputText>
            </h:form>
            <h:outputText id="text" value="${greeter.response}"/>
        </f:view>
    </h:body>
</html>
```

Let's test it locally

```sh
$ mvn jetty:run[INFO] Scanning for projects...
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] Building JSF 2.0 Hello World 0.1-SNAPSHOT
[INFO] ------------------------------------------------------------------------
[INFO]

...

WARNING:

*******************************************************************
*** WARNING: Apache MyFaces-2 is running in DEVELOPMENT mode.   ***
***                                         ^^^^^^^^^^^         ***
*** Do NOT deploy to your live server(s) without changing this. ***
*** See Application#getProjectStage() for more information.     ***
*******************************************************************

2011-05-17 10:22:10.982:INFO::Started SelectChannelConnector@0.0.0.0:8080
[INFO] Started Jetty Server
```

Fire up a browser to http://localhost:8080/ and here's what we get:

![](/images/post/2011-05-17-local-app-running.png)

OK, so now I turn off DEVELOPMENT mode in the web.xml, build my app and deploy it to RUN@cloud... and [here](http://jsf2-hello-world.stephenc.cloudbees.net/)'s what we get:

![](/images/post/2011-05-17-paas-app-running.png)

That was cool. Didn't have to change anything (other than switch to production mode for safety as it's being deployed in the wild) and I did all this in under 20 minutes (including signing up for RUN@cloud)

My next steps will be to integrate this web application with DEV@cloud and our Jenkins plugin for deployment to RUN@cloud so that I can show off continuous deployment! But that will be a different day!