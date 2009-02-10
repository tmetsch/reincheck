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


import zipfile
import string
import sys

class Bundle:
    
    manifest = {}
    
    def __init__(self, jarFile):
        zip = zipfile.ZipFile(jarFile)
        for file in  zip.filelist:
            if file.filename.find('MANIFEST.MF') > -1:
                manifestFile = zip.read(file.filename)
        zip.close
        
        mf = {}
        
        temp =  string.replace(manifestFile, "\r\n ", "").split('\n')
        for item in temp:
            mf[item.partition(': ')[0]] = item.partition(': ')[2]

        #global manifest
        self.manifest = mf
        
        if len(self.manifest) == 0:
            raise ValueError('No manifest found!')
    
    def getSymbolicName(self):
        try:
            return self.manifest['Bundle-SymbolicName'].replace('\r', '')
        except:
            return list()
    
    def getImports(self):
        try:
            imports = self.manifest['Import-Package'].replace('\n','').replace('\r','').split(',')
            strippedimports = [item[:item.find(';')].replace('\"','') for item in imports]
            return imports
        except:
            return list()
    
    def getExports(self):
        try:
            exports = self.manifest['Export-Package'].replace('\n','').split(',')
            strippedexports = [item[:item.find(';')].replace('\"','') for item in exports]
            # if item.find(';') > -1
            return strippedexports
        except:
            return list()
    
    def getRequiredBundles(self):
        try:
            return self.manifest['Required-Bundles'].replace('\n','').split(',')
        except:
            return list()

    def getMetaInformation(self, tagName):
        return self.manifest[tagName]