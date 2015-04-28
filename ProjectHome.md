Everybody knows about the broken-window principal. But when software projects grow and become older ever repository get broken windows. This can be missing unittest, files which are left over from refactoring which are not longer needed, unneeded files, empty packages and modules, old untouched documents, dependencies between modules which are not allowed but became a backbone of the software by now, changes which where done in the code but not in the metafiles (like descriptions, names) etc.

Think about this one:

_How great would it be to know that your repository is clean and your (new)colleagues can checkout the code, compile and run it within minutes? wouldn't it be great?_

This REpository INtegrity CHECKer tries to find those issues and will report on them. By checking the dependencies, consistency of the metafiles, consistency of the repository, for unneeded files, old files, empty directories, missing unittest and even more if you write your own checks.

ReInCheck tries to fill the gap between existing tools like issues trackers, svnchecker, checkstyle, findbugs and many others. The linking between tools is one of the most important parts for this.

Start [here with an overview](OverView.md) and if you are done have a look here: [on howto setup ReInCheck for a multi module maven OSGi based application](PageName.md)

If you have any ideas, comments or suggestions feel free to contact me.