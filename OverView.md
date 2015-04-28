# Introduction #

ReInCheck is currently still in development. I wrote it for fun and currently is only working for multi module maven projects.

## Features ##

  * Configurable tool to check the integrity of your source code projects
  * programming language independent
  * source code management system independent
  * support of networkx graphs

## Walkers ##

A walker is a tool which ReInCheck uses to 'walk' through your repository. A walker defines for each project where the source code, the test code, resource files and target files are located.

Currently only a walker for a multi module maven project exists. It returns all the source code directories from the modules itself when he is asked to return the source code directories.

With the help of walkers it is possible to support almost any kind of repository layouts for your project. Just write your own :-)

## Checks ##

Checks are run based on resources. Each check can do what every he wants. He only has to return a report, errors and maybe a graph. When a graph is returned it is currently directly shown to the user.

Currently the following checks exist:

  * EmptyPackageCheck - Checks if a directory contains no files
  * GetMisplacesFilesInJavaDiretories - Checks if a directory contains other files then .java
  * ImportCheck - Can be run when the target files are OSGi bundles. Will create a graoh with all the dependencies and report those.
  * ExportCheck - Can be run when the target files are OSGi bundles. Will create a list of packages which are never imported but exported by one bundle
  * CheckForMissingJUnitTest - Looks for missing Junittest. If the normal would be /src/main/java/Somefile.java it tries to find the file /src/test/java/SomefileTest.java. Interfaces are not taken in account.
  * CheckForUndeletedJUnitTest - Looks if there is a source file for every Junittest. E.g. /src/test/java/SomefileTest.java should have a /src/main/java/Somefile.java

## Config file ##

With help of the config.ini file you can state which checks should be run for which kind of resources.

An example config.ini files looks like:

```
[repository]
path = /home/tmetsch/workspace/sample-app/
scmPrefix = .svn

[walker]
rootWalker = MultiModuleMavenWalker

[checks]
srcChecks = EmptyPackageCheck, GetMisplacesFilesInJavaDiretories
testChecks = EmptyPackageCheck, GetMisplacesFilesInJavaDiretories
resourceChecks = 
targetChecks = ImportCheck, ExportCheck
```

The first property states where the root of the repository is. This needs to a checkout of the source code. If you want to use the target checks you will also need to build it.

The second property states which subdirectories within the source code ReInCheck should no visit. In this case do not look into the .svn directories.

The walked property states which walker should be used.

Finally the checks are defined. In this case it states: for every source and test directory check if there are empty packages and if there are misplaced files. No checks on resource files are run. But the target files are OSGi bundles so the Export- and ImportCheck can be run.

## Upcoming features ##

  * Support of configuring to store graphs instead of displaying them