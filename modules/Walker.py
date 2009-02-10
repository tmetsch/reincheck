# Reincheck, Tool for testing integrity of source code repositories
# Copyright (C) 2009  Thijs Metsch <tmetsch@gmail.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import os

class Walker():

    projectRoot = ''

    def __init__(self, root):
        self.projectRoot = root
    
    def getSourceDirectories(self):
        raise Exception("Not yet implemented.")

    def getTestDirectories(self):
        raise Exception("Not yet implemented.")

    def getResourceFiles(self):
        raise Exception("Not yet implemented.")

    def getTargetFiles(self):
        raise Exception("Not yet implemented.")

class MultiModuleMavenWalker(Walker):

    srcDirectoryPrefix = 'src/main/java'
    testDirectoryPrefix = 'src/test/java'
    targetDirectoryPrefix = 'target'

    def __init__(self, root):
        Walker.__init__(self,root)

    def getSourceDirectories(self):
        srcDirectories = []

        for f in os.listdir(self.projectRoot):
            if os.path.isdir(os.path.join(self.projectRoot, f, self.srcDirectoryPrefix)):
                srcDirectories.append(str(os.path.join(self.projectRoot, f, self.srcDirectoryPrefix)))

        return srcDirectories
    
    def getTestDirectories(self):
        testDirectories = []
        
        for f in os.listdir(self.projectRoot):
            if os.path.isdir(os.path.join(self.projectRoot, f, self.testDirectoryPrefix)):
                testDirectories.append(str(os.path.join(self.projectRoot, f, self.testDirectoryPrefix)))

        return testDirectories
    
    def getTargetFiles(self):
        targetFiles = []
        
        for f in os.listdir(self.projectRoot):
            if os.path.isdir(os.path.join(self.projectRoot, f, self.targetDirectoryPrefix)):
                path = str(os.path.join(self.projectRoot, f, self.targetDirectoryPrefix))
                dirList=os.listdir(path)
                for fname in dirList:
                    if fname.find('.jar') != -1:
                        targetFiles.append(str(os.path.join(path, fname)))
        return targetFiles
    
    def getResourceFiles(self):
        resourceFiles = []
        return resourceFiles
