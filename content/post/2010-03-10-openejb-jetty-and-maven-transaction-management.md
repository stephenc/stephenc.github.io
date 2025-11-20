---
title: "OpenEjb, Jetty and Maven - Transaction Management"
date: 2010-03-10T00:00:00Z
tags: ["Java", "Maven", "JavaEE"]
---

I've been meaning to blog about getting transaction management working with OpenEjb and Jetty using `jetty:run`... it's still an on-going story... but the following might get you going...

First off, in your `pom.xml` you need to add the configuration for `maven-jetty-plugin`... we need to dance around the various activemq/activeio versions and ensure that we get the correct version of ant... 

```xml
<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" 
	    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.apache.openejb.examples</groupId>
  <artifactId>jetty-openejb</artifactId>
  <packaging>war</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>jetty-openejb Maven Webapp</name>
  <url>http://maven.apache.org</url>
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <finalName>${project.artifactId}</finalName>
    <plugins>
      <plugin>
        <groupId>org.mortbay.jetty</groupId>
        <artifactId>maven-jetty-plugin</artifactId>
        <version>6.1.22</version>
        <dependencies>
          <dependency>
            <groupId>org.apache.activemq</groupId>
            <artifactId>activemq-core</artifactId>
            <version>4.1.1</version>
            <exclusions>
              <exclusion>
                <groupId>commons-logging</groupId>
                <artifactId>commons-logging</artifactId>
              </exclusion>
              <exclusion>
                <groupId>commons-logging</groupId>
                <artifactId>commons-logging-api</artifactId>
              </exclusion>
              <exclusion>
                <groupId>org.apache.activemq</groupId>
                <artifactId>activeio-core</artifactId>
              </exclusion>
            </exclusions>
          </dependency>
          <dependency>
            <groupId>org.apache.activemq</groupId>
            <artifactId>activemq-ra</artifactId>
            <version>4.1.1</version>
            <exclusions>
              <exclusion>
                <groupId>commons-logging</groupId>
                <artifactId>commons-logging</artifactId>
              </exclusion>
              <exclusion>
                <groupId>commons-logging</groupId>
                <artifactId>commons-logging-api</artifactId>
              </exclusion>
              <exclusion>
                <groupId>org.apache.activemq</groupId>
                <artifactId>activeio-core</artifactId>
              </exclusion>
            </exclusions>
          </dependency>
          <dependency>
            <groupId>org.apache.activemq</groupId>
            <artifactId>activeio-core</artifactId>
            <version>3.1.2</version>
            <exclusions>
              <exclusion>
                <groupId>commons-logging</groupId>
                <artifactId>commons-logging</artifactId>
              </exclusion>
              <exclusion>
                <groupId>commons-logging</groupId>
                <artifactId>commons-logging-api</artifactId>
              </exclusion>
            </exclusions>
          </dependency>
          <dependency>
            <groupId>org.apache.openejb</groupId>
            <artifactId>openejb-core</artifactId>
            <version>3.1.2</version>
            <exclusions>
              <exclusion>
                <groupId>org.apache.activemq</groupId>
                <artifactId>activemq-core</artifactId>
              </exclusion>
              <exclusion>
                <groupId>org.apache.activemq</groupId>
                <artifactId>activemq-ra</artifactId>
              </exclusion>
              <exclusion>
                <groupId>org.apache.activemq</groupId>
                <artifactId>activeio-core</artifactId>
              </exclusion>
              <exclusion>
                <groupId>junit</groupId>
                <artifactId>junit</artifactId>
              </exclusion>
            </exclusions>
          </dependency>
          <!-- in order to use the latest version of openejb, we need to exclude
               the dependencies provided in jsp-2.1-jetty -->
          <dependency>
            <groupId>org.mortbay.jetty</groupId>
            <artifactId>jsp-2.1-jetty</artifactId>
            <version>6.1.22</version>
            <exclusions>
              <exclusion>
                <groupId>ant</groupId>
                <artifactId>ant</artifactId>
              </exclusion>
            </exclusions>
          </dependency>
        </dependencies>
        <configuration>
          <jettyConfig>${basedir}/src/main/jetty/jetty.xml</jettyConfig>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

Next we need to configure a `src/main/jetty/jetty.xml` to bind the UserTransaction instance into jetty... 

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE Configure PUBLIC "-//Mort Bay Consulting//DTD Configure//EN" "http://jetty.mortbay.org/configure.dtd">
<Configure id="srv" class="org.mortbay.jetty.Server">
  <New class="javax.naming.InitialContext">
    <Arg>
      <New class="java.util.Properties">
        <Call name="setProperty">
          <Arg>java.naming.factory.initial</Arg>
          <Arg>org.apache.openejb.client.LocalInitialContextFactory</Arg>
        </Call>
      </New>
    </Arg>
    <Call name="lookup" id="tm">
      <Arg>openejb:TransactionManager</Arg>
    </Call>
  </New>
  <New class="org.mortbay.jetty.plus.naming.Transaction">
    <Arg>
      <New class="org.apache.openejb.core.CoreUserTransaction">
        <Arg>
          <Ref id="tm"/>
        </Arg>
      </New>
    </Arg>
  </New>
</Configure>
```

And presto-chango, now jetty has a transaction manager provided by openejb. 

> [!NOTE]
> If we don't mind storing that in a jetty-env in `/WEB-INF`, you can put the same config in `WEB-INF/jetty-env.xml`

OK, so here are the issues:

* Reloading does not work (because `org.apache.openejb.core.ivm.naming.IvmContext` does not support the `destroySubcontext(Context)` method
* We are using jetty's JNDI provider in the web-app and openejb's JNDI provider for the EJBs... this is because 

  When jetty binds names to JNDI (using `org.mortbay.jetty.plus.naming.Resource` or `org.mortbay.jetty.plus.naming.Transaction`) it binds the object to JNDIName and it also binds a `NamingEnrtry` for the object to `__/JNDIName` 

  Unfortunately, openejb's JNDI implementation seems to be somewhat strange in this regard... if we add the `SystemProperties` to jetty to have it use openejb's JNDI implementation, e.g. add the following to `/project/build/plugins/plugin[maven-jetty-plugin]/configuration/systemProperties`                         
  ```xml
  <systemProperty>
    <name>java.naming.factory.initial</name>
    <value>org.apache.openejb.client.LocalInitialContextFactory</value>                         
  </systemProperty>
  ```

  Then when we bind `__/UserTransaction` it gets bound to `openejb:__/UserTransaction` but when we lookup `__/UserTransaction` openejb looks up `openejb:local/__/UserTransaction` 

  And that is just for starters... there seems to be a whole host of other JNDI strangeness between jetty's side and openejb's side

  The side effect of all this is that if you want resource refs to work correctly, you need to fish them out of openejb's JNDI context and push them into jetty's JNDI context 

In any case this is at least a start!