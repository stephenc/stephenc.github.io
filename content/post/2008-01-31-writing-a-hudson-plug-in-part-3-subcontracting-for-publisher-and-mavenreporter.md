---
title: "Writing a Hudson plug-in (Part 3 – Subcontracting for Publisher and MavenReporter)"
date: 2008-01-31T00:00:00Z
tags: ["Jenkins"]
---

In this, the third installment, I will introduce some helper classes that we can use to let Publisher and MavenReporter subcontract the job of creating the build reports. Firstly, we have the Ghostwriter interface. An implementation of a Ghostwriter is the work-horse that writes the build report. Secondly, we have the BuildProxy class. This class is a more general MavenBuildProxy that works for both Maven builds and non-Maven builds. In part 4 we will tie these helpers into the Hudson plugin framework with an AbstractMavenReporterImpl and AbstractPublisherImpl from which we can extend our plugin's MavenReporter and Publisher.

The classes presented here and in part 4 should be generic enough that most plugins can be implemented on the back of them, hence my reason for making them this generic.

## Ghostwriter

A class or interface should be named after its function. PublisherDelegate, RealReporter, etc, just did not seem snappy enough, so I've picked Ghostwriter, as I think it encapsulates the idea of actually doing the writing without the consumer knowing who did the work!

```java
package hudson.plugins.helpers;

import hudson.model.BuildListener;
import hudson.model.AbstractBuild;
import hudson.FilePath;

import java.io.Serializable;
import java.io.IOException;

public interface Ghostwriter extends Serializable {
    public static interface SlaveGhostwriter
            extends Ghostwriter {
        boolean performFromSlave(BuildProxy build,
                                 BuildListener listener)
                throws InterruptedException, IOException;
    }

    public static interface MasterGhostwriter
            extends Ghostwriter {
        boolean performFromMaster(AbstractBuild build,
                                  FilePath executionRoot,
                                  BuildListener listener)
                throws InterruptedException, IOException;
    }
}
```

This interface is really a marker interface for a class that implements at least one of `SlaveGhostwriter` and `MasterGhostwriter`. The idea between these two child interfaces is that they encapsulate execution on the slave or the master.

Let's look at `Ghostwriter.MasterGhostwriter` the method for performing our plugin's action receives three parameters:

- The build that this plugin is being executed on;
- The file path location of the execution of the build (Note: this is a `FilePath` as the execution of the build is most likely remote from the master); and
- The build listener where to allow us to add information to the build log

These are mostly the same parameters as `hudson.tasks.BuildStep` provides in its perform method, however we have substituted a file path for a launcher. The logic here is that with the Maven project type, the root of the maven module needs to be passed back to the plugin, so we will need this file path information. With the Free-style project type, the root easily and unambiguously available from the `build` parameter. The exceptions that we declare are needed as this method could be being called from the slave via the remoting support built into Hudson.

If we now turn to `Ghostwriter.SlaveGhostwriter`. In this case, the perform method takes two parameters

- The build proxy, modelled after MavenBuildProxy, which contains the essential information required for our plugin; and
- The build listener.

The idea with both of these interfaces is that our plugin implementation does some work figuring out what our Ghostwriter is supposed to do. If we are in a Maven project, we can determine some of the information from the pom.xml and the rest from Hudson. If we are in any other type of project, we determine all the information from Hudson. We capture that configuration in a Ghostwriter instance, and we send the Ghostwriter off to do our work. The Ghostwriter then goes off to the slave or the master as necessary and does it's job. We have separated our concerns as we have:

- A publisher for determining the configuration for a freestyle project;
- A maven reported for determine the configuration for a Maven2 project; and
- A ghostwriter for getting the job done

Now it is time to look at our next helper class

## BuildProxy

This is our workhorse class, it is designed to hide the different execution paths to calling the `Ghostwriter` and ensuring that there are no differences (as far as the `Ghostwriter` is concerned) between the Free-style project type and the Maven2 project type. As I said earlier, it is modelled on `MavenBuildProxy`, so we have getters for the important directories on the Master that are needed on the Slave. For example, if we need to copy a file to the artifacts directory of the master, the build directory of the master, or the project directory of the master.

```java
package hudson.plugins.helpers;

import hudson.FilePath;
import hudson.maven.MavenBuildProxy;
import hudson.util.IOException2;
import hudson.model.Action;
import hudson.model.Result;
import hudson.model.AbstractBuild;
import hudson.model.BuildListener;

import java.util.Calendar;
import java.util.List;
import java.util.ArrayList;
import java.io.IOException;

import org.apache.maven.project.MavenProject;

public final class BuildProxy implements Serializable {
    private final FilePath artifactsDir;
    private final FilePath projectRootDir;
    private final FilePath buildRootDir;
    private final FilePath executionRootDir;
    private final Calendar timestamp;

    private BuildProxy(FilePath artifactsDir,
                       FilePath projectRootDir,
                       FilePath buildRootDir,
                       FilePath executionRootDir,
                       Calendar timestamp) {
        this.artifactsDir = artifactsDir;
        this.projectRootDir = projectRootDir;
        this.buildRootDir = buildRootDir;
        this.executionRootDir = executionRootDir;
        this.timestamp = timestamp;
    }

    public FilePath getArtifactsDir() {
        return artifactsDir;
    }

    public FilePath getBuildRootDir() {
        return buildRootDir;
    }

    public FilePath getExecutionRootDir() {
        return executionRootDir;
    }

    public FilePath getProjectRootDir() {
        return projectRootDir;
    }

    public Calendar getTimestamp() {
        return timestamp;
    }
}
```

There are additional methods, but I want to outline the key function of `BuildProxy` before introducing them. Also, the constructor is `private` because we will use these additional methods it instantiate the BuildProxy for us.

In my experience, the primary information that a plugin needs to know (when executing on the slave) are the five pieces of information that are stored in `BuildProxy`

- The artifacts directory - the directory on the master where artifacts for this project are to be stored;
- The build root directory - the directory on the master where build reports for this build are to be stored;
- The project root directory - the directory on the master where project reports are to be stored;
- The timestamp when the build started - for example to identify new artifacts produced during the build; and finally
- The execution root directory - the directory either on the slave or the master from which the build was performed

Now, when our plugin is executing on the slave, it will need to pass back information to the real build. For example, if our plugin completes successfully, we will want to attach `Action` objects to the `AbstractBuild` in order to allow the user to see the results of our plugin on the build pages in Hudson. If there were problems when executing our plugin, we may want to fail the build, mark it as unstable, or stop any other plugins from executing. To handle these cases, we need to add some mutable properties to our `BuildProxy`:

```java
...

public final class BuildProxy implements Serializable {

    ...

    private final List<Action> actions = new ArrayList<Action>();
    private Result result = null;
    private boolean continueBuild = true;

    ...

    public List<Action> getActions() {
        return actions;
    }

    public Result getResult() {
        return result;
    }

    public void setResult(Result result) {
        this.result = result;
    }

    public boolean isContinueBuild() {
        return continueBuild;
    }

    public void setContinueBuild(boolean continueBuild) {
        this.continueBuild = continueBuild;
    }

    ...

}
```

So now our `Ghostwriter.SlaveGhostwriter` has the ability to:

- Add actions to the build;
- Modify the result of the build; and
- Flag that the build should finish as early as possible.

At this point we are ready to introduce the static methods that will invoke the `Ghostwriter` for our `Publisher` or `MavenReporter`.

First off, we have a `doPerform` method designed to be called from a `Publisher`:

```java
...

public final class BuildProxy {

    ...

    public static boolean doPerform(Ghostwriter ghostwriter,
                                    AbstractBuild build,
                                    BuildListener listener)
            throws IOException, InterruptedException {

        // first, do we need to do anything on the slave

        if (ghostwriter instanceof Ghostwriter.SlaveGhostwriter) {

            // construct the BuildProxy instance that we will use

            BuildProxy buildProxy = new BuildProxy(
                    new FilePath(build.getArtifactsDir()),
                    new FilePath(build.getProject().getRootDir()),
                    new FilePath(build.getRootDir()),
                    build.getProject().getModuleRoot(),
                    build.getTimestamp());

            BuildProxyCallableHelper callableHelper =
                new BuildProxyCallableHelper(buildProxy, ghostwriter, listener);

            try {
                buildProxy = buildProxy.getExecutionRootDir().act(callableHelper);

                buildProxy.updateBuild(build);

                // terminate the build if necessary
                if (!buildProxy.isContinueBuild()) {
                    return false;
                }
            } catch (Exception e) {
                throw unwrapException(e, listener);
            }
        }

        // finally, on to the master

        final Ghostwriter.MasterGhostwriter masterGhostwriter =
            Ghostwriter.MasterGhostwriter.class.cast(ghostwriter);

        return masterGhostwriter == null
                || masterGhostwriter.performFromMaster(build,
                        build.getProject().getModuleRoot(),
                        listener);
    }

    private static RuntimeException unwrapException(Exception e,
                                                    BuildListener listener)
            throws IOException, InterruptedException {
        if (e.getCause() instanceof IOException) {
            throw new IOException2(e.getCause().getMessage(), e);
        }
        if (e.getCause() instanceof InterruptedException) {
            e.getCause().printStackTrace(listener.getLogger());
            throw new InterruptedException(e.getCause().getMessage());
        }
        if (e.getCause() instanceof RuntimeException) {
            throw new RuntimeException(e.getCause());
        }
        // How on earth do we get this far down the branch
        e.printStackTrace(listener.getLogger());
        throw new RuntimeException("Unexpected exception", e);
    }

    public void updateBuild(AbstractBuild build) {
        // update the actions
        build.getActions().addAll(actions);

        // update the result
        if (result != null && result.isWorseThan(build.getResult())) {
            build.setResult(result);
        }
    }

    ...
}
```

The method is initially called from the master. It takes a `Ghostwriter`, a build and a build listener. First off it checks if the `Ghostwriter` wants to execute some tasks on the slave, i.e. if it implements `Ghostwriter.SlaveGhostwriter`, sending the `Ghostwriter` over to the slave with a `BuildProxy` and updating the real build when the `BuildProxy` is returned. Finally, if the `Ghostwriter` wants to execute some tasks on the master, i.e. if it implements `Ghostwriter.MasterGhostwriter` we pass control over to the `Ghostwriter` again. _**Note:** slave execution is **pass-by-value**._. Thus, if the `Ghostwriter` is executed on both the slave and the master, changes made to the `Ghostwriter` on the slave will not be picked up when executing on the master.

Now, for the method that will be called from a `MavenReporter`:

```java
...

public final class BuildProxy implements Serializable {

    ...

    public static boolean doPerform(Ghostwriter ghostwriter,
                                    MavenBuildProxy mavenBuildProxy,
                                    MavenProject pom,
                                    final BuildListener listener)
            throws InterruptedException, IOException {

        // first, construct the BuildProxy instance that we will use

        BuildProxy buildProxy = new BuildProxy(
                mavenBuildProxy.getArtifactsDir(),
                mavenBuildProxy.getProjectRootDir(),
                mavenBuildProxy.getRootDir(),
                new FilePath(pom.getBasedir()),
                mavenBuildProxy.getTimestamp());

        // do we need to do anything on the slave

        if (ghostwriter instanceof Ghostwriter.SlaveGhostwriter) {
            final Ghostwriter.SlaveGhostwriter slaveGhostwriter =
                (Ghostwriter.SlaveGhostwriter) ghostwriter;

            // terminate the build if necessary
            if (!slaveGhostwriter.performFromSlave(buildProxy, listener)) {
                return false;
            }
        }

        // finally, on to the master

        try {
            return mavenBuildProxy.execute(
                new BuildProxyCallableHelper(buildProxy,
                                             ghostwriter,
                                             listener));
        } catch (Exception e) {
            throw unwrapException(e, listener);
        }
    }

    ...
}
```

This method is initially called from the slave. It takes the `Ghostwriter`, the `MavenBuildProxy`, the pom and the build listener. We start off by creating the `BuildProxy` from the `MavenBuildProxy` and the pom, then we invoke the `Ghostwriter` if necessary (i.e. if it executes on the slave). Finally, we send the `BuildProxy` and the `Ghostwriter` over to the master in order to add any required build actions and, if necessary execute on the master.

Both of these two static helper methods make use of a `Callable` that is used by Hudson's remoting support to send tasks between the master and the slave:

```java
package hudson.plugins.helpers;

import hudson.remoting.Callable;
import hudson.maven.MavenBuildProxy;
import hudson.maven.MavenBuild;
import hudson.model.BuildListener;

import java.io.IOException;

class BuildProxyCallableHelper implements Callable<BuildProxy, Exception>,
        MavenBuildProxy.BuildCallable<Boolean, Exception> {

    private final BuildProxy buildProxy;
    private final Ghostwriter ghostwriter;
    private final BuildListener listener;

    BuildProxyCallableHelper(BuildProxy buildProxy,
                             Ghostwriter ghostwriter,
                             BuildListener listener) {
        this.buildProxy = buildProxy;
        this.ghostwriter = ghostwriter;
        this.listener = listener;
    }

    public Boolean call(MavenBuild mavenBuild) throws Exception {
        buildProxy.updateBuild(mavenBuild);
        if (ghostwriter instanceof Ghostwriter.MasterGhostwriter) {
            final Ghostwriter.MasterGhostwriter masterBuildStep =
                    (Ghostwriter.MasterGhostwriter) ghostwriter;
            return masterBuildStep.performFromMaster(
                    mavenBuild,
                    buildProxy.getExecutionRootDir(),
                    listener);
        }
        return true;
    }

    public BuildProxy call() throws Exception {
        if (ghostwriter instanceof Ghostwriter.SlaveGhostwriter) {
            final Ghostwriter.SlaveGhostwriter slaveBuildStep =
                    (Ghostwriter.SlaveGhostwriter) ghostwriter;
            try {
                buildProxy.setContinueBuild(
                        slaveBuildStep.performFromSlave(buildProxy, listener));
                return buildProxy;
            } catch (IOException e) {
                throw new Exception(e);
            } catch (InterruptedException e) {
                throw new Exception(e);
            }
        }
        return buildProxy;
    }
}
```

Ok, that's enough for now. The full source code (including javadoc comments) for these classes is available in Hudson's CVS server underneath the /hudson/hudson/plugins/javancss/ directory. The next part of this tutorial will demonstrate how to use these methods by introducing an `AbstractMavenReporterImpl` and an `AbstractPublisherImpl` from which we can inherit our publisher and maven reporter.
