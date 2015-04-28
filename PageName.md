# Introduction #

This page shows howto to ReInCheck within a multi module maven based project, where each maven modules embeds a OSGi Bundle.

# Details #

I wanted too test the integrity of a project which consists of several OSGi bundles. Each OSGi bundle is define as it's own maven module.

Currently I am able to run some test to verify that no empty packages exists, no other files than java files are located in the source diretories, what the dependencies between my bundles are, which export statement are unnecessary,

## Environment ##

The repository looks as follows:

```
[...]
sample-app
-> bundle1
---> src/main/java
---> src/test/java
---> target/bundle1.jar
-> bundle2
---> src/main/java
---> src/test/java
---> target/bundle2.jar
```

## Setup ##

I checked out reincheck and used the following config.ini to call _python reincheck.py config.ini_:

```
[repository]
path = /home/tmetsch/workspace/sample-app
scmPrefix = .svn

[walker]
rootWalker = MultiModuleMavenWalker

[checks]
srcChecks = EmptyPackageCheck, GetMisplacesFilesInJavaDiretories, CheckForMissingJUnitTest
testChecks = EmptyPackageCheck, GetMisplacesFilesInJavaDiretories, CheckForUndeletedJUnitTest
resourceChecks =
targetChecks = ImportCheck, ExportCheck
```

## Howto run ReInCheck ##

Simply run _python reincheck.py config.ini_

## Sample Report ##

This is currently the output of reincheck:

```
DEBUG:root:
--------
 Empty package report 
--------

DEBUG:root:
--------
 Checking for files which do not belong in java dirs 
--------

DEBUG:root:
--------
 Empty package report 
--------

WARNING:root:Found empty directory: /home/tmetsch/workspace/sample-app/bundle1/src/test/java/blubber

--------
 Checking for files which do not belong in java dirs 
--------

DEBUG:root:
--------
 OSGi Import report
--------
bundle1 depends on bundle2

DEBUG:root:
--------
 Looking for unused OSGi exports 
--------
Bundle bundle1 exports package which is never imported : some.test.package

```

It states that there is one empty package. That bundle1 depends on bundle2 (Currently also a graph is shown) and that a package from bundle1 is never important by another bundle and therefor somehow useless.