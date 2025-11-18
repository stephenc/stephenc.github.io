---
title: "Continuously deploy your java apps to the cloud"
date: 2011-05-01T00:00:00Z
tags: ["CloudBees"]
---

In my previous post showed how easy it is to run your java application on CloudBees' RUN@cloud service. Today I'm going to use the CloudBees Deployer plugin for Jenkins that allows you to deploy your app to the cloud from your CI server. I am using the DEV@cloud Jenkins service for my CI infrastructure, but you can use this plugin from your own Jenkins (or Nectar) server.

So first step is to install the CloudBees Deployer plugin...

1. Goto Manage Jenkins

2. Goto Manage Plugins3. Goto the Available tab4. Scroll down until you find the cloudbees-deployer-plugin. Check the box.5. Scroll down and click the Install button6. Restart Jenkins after it's installed.7. Goto Manage Jenkins, select Configure and scroll down to the bottom8. Click the Add button beside the CloudBees accounts9. Add in your CloudBees account details (which you can find on your user keys screen on grandcentral)10. Click on Save and then goto the Configure page for your project. Enable CloudBees Deployment and fill in the details: 11. Save and then kick off a build12. When the build is finished, your application has been deployed:There you go. Continuous Deployment on RUN@cloud.

There is a whole host of things you can do with this.  You can use build promotion to trigger the deployment, you can set up a staging deployment followed by the real thing if a test staging project builds successfully... I could go on... but there is always another day! Speaking of which, my next step will probably be enabling deployment straight from the project build (for those unfortunate enough to not have a CI server) probably using the ship-maven-plugin