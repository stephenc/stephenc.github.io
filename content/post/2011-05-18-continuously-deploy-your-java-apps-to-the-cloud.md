---
title: "Continuously deploy your java apps to the cloud"
date: 2011-05-18T00:00:00Z
tags: ["CloudBees"]
---

In my [previous post](/post/2011-05-17-deploy-your-java-apps-to-the-cloud/) I showed how easy it is to run your java application on CloudBees' RUN@cloud service. Today I'm going to use the CloudBees Deployer plugin for Jenkins that allows you to deploy your app to the cloud from your CI server. I am using the DEV@cloud Jenkins service for my CI infrastructure, but you can use this plugin from your own Jenkins (or Nectar) server.

So first step is to install the CloudBees Deployer plugin...

1. Goto Manage Jenkins

  ![](/images/post/2011-05-18-step1.png)

2. Goto Manage Plugins

  ![](/images/post/2011-05-18-step3.png)

3. Goto the Available tab

  ![](/images/post/2011-05-18-step3.png)

4. Scroll down until you find the cloudbees-deployer-plugin. Check the box.

  ![](/images/post/2011-05-18-step4.png)

5. Scroll down and click the Install button

  ![](/images/post/2011-05-18-step5.png)

6. Restart Jenkins after it's installed.

  ![](/images/post/2011-05-18-step6.png)

7. Goto Manage Jenkins, select Configure and scroll down to the bottom

  ![](/images/post/2011-05-18-step7.png)

8. Click the Add button beside the CloudBees accounts

  ![](/images/post/2011-05-18-step8.png)

9. Add in your CloudBees account details (which you can find on your user keys screen on grandcentral)

  ![](/images/post/2011-05-18-step9.png)

10. Click on Save and then goto the Configure page for your project. Enable CloudBees Deployment and fill in the details:

  ![](/images/post/2011-05-18-step10.png)

11. Save and then kick off a build

  ![](/images/post/2011-05-18-step11.png)

12. When the build is finished, your application has been deployed:

  ![](/images/post/2011-05-18-step12.png)

There you go. Continuous Deployment on RUN@cloud.

There is a whole host of things you can do with this. You can use build promotion to trigger the deployment, you can set up a staging deployment followed by the real thing if a test staging project builds successfully... I could go on... but there is always another day! Speaking of which, my next step will probably be enabling deployment straight from the project build (for those unfortunate enough to not have a CI server) probably using the [ship-maven-plugin](http://mojo.codehaus.org/ship-maven-plugin)