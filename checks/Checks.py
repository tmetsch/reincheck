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
from networkx import *

from modules.Bundle import Bundle
import os

class Check:
    
    def check(self, resources, scmPrefix):
        raise Exception('Not yet implemented')

class EmptyPackageCheck(Check):
    
    def check(self, directories, scm_dir):
	graph = DiGraph()
        errors = []
        report = '\n--------\n Empty package report \n--------\n'
		
	for directory in directories:
	    ## find empty
	    for root, dirs, files in os.walk(directory):
		if str(scm_dir) in dirs:
		    dirs.remove(str(scm_dir))
		if len(dirs) == 0 and len(files) == 0:
		    errors.append("Found empty directory: " + str(root))
	
	return (report, errors, graph)
    
class GetMisplacesFilesInJavaDiretories(Check):
    
    def check(self, directories, scm_dir):
	graph = DiGraph()
        errors = []
        report = '\n--------\n Checking for files which do not belong in java dirs \n--------\n'
		
	for directory in directories:
	    for root, dirs, files in os.walk(directory):
		if scm_dir in dirs:
		    dirs.remove(scm_dir)
		for file in files:
		    if file.find('.java') == -1:
			errors.append("Found a file which does not belong here" + str(os.path.join(root, file)))
	
	return (report, errors, graph)

class ImportCheck(Check):
    
    def check(self, files, scmPrefix):
        graph = DiGraph()
        errors = []
        report = '\n--------\n OSGi Import report\n--------\n'

	bundles = []
	for file in files:
            bundle = Bundle(file)
            bundles.append(bundle)
	
        for bundle1 in bundles:
            imports = bundle1.getImports()
            for bundle2 in bundles:
                if bundle1.getSymbolicName != bundle2.getSymbolicName:
	                ## look for imports
	                exports = bundle2.getExports()
	                try:
	                    temp = self.intersect(imports, exports)
	                except:
	                    print "Unexpected error:", sys.exc_info()[0]
	                if len(temp) > 0:
	                    graph.add_edge(bundle1.getSymbolicName(), bundle2.getSymbolicName())
	                    report = report + bundle1.getSymbolicName() + ' depends on ' + bundle2.getSymbolicName() + '\n'
        return (report, errors, graph)
    
    def intersect(self, a, b):
	if (len(a) > 0 and len(b) > 0):
	    return list(set(a) & set(b))
	else:
	    return list()
    
class ExportCheck(Check):
    
    def check(self, files, scmPrefix):
		
	#graph = XGraph(selfloops=True, multiedges=True)
        graph = Graph()
        errors = []
        report = '\n--------\n Looking for unused OSGi exports \n--------\n'

	bundles = []
	for file in files:
            bundle = Bundle(file)
            bundles.append(bundle)
	
        imports = []
        for bundle in bundles:
        	imports.extend(bundle.getImports())

        for bundle in bundles:
            exports = bundle.getExports()
            try:
                temp = self.unique(exports, imports)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise
            if len(temp) > 0:
                for item in temp:
                    report = report + 'Bundle ' + bundle.getSymbolicName() + ' exports package which is never imported : ' + item + '\n'

        return (report, errors, graph)

    def unique(self, a, b):
        return [item for item in a if item not in b]
