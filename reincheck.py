#!/usr/bin/env python

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

from ConfigParser import ConfigParser
from modules.Bundle import Bundle

import matplotlib.pyplot as P
import networkx as nx

import logging
import os
import sys

config_file = '/home/tm226479/data/workspace/reincheck/config.ini'

def runThoseSuperChecks(listOfChecks, directory, scmPrefix):
    for aCheck in listOfChecks:
        if aCheck == '':
            break
        try:
            exec("from checks.Checks import %s" % aCheck)
            checkinstance = eval(aCheck)()
            (report, error, graph) = checkinstance.check(directory, scmPrefix)
            logging.debug(report)
            if len(error) > 0:
                for err in error:
                    logging.warning(err)
            if (graph):
                try:
                    nx.draw(graph, pos=nx.circular_layout(graph))
                    P.show()
                except: # matplotlib not available
                    pass
        except ImportError:
            logging.warning('The check %s was not found.' % aCheck)

if __name__ == '__main__':
    # some initial setup
    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 2:
        print 'Please use the following syntac reincheck <config.ini>'
        sys.exit(0)
    else:
        config_file = sys.argv[1]
        
    config = ConfigParser()
    config.read(config_file)

    # get the root walker
    walkerName = config.get('walker', 'rootWalker')
    path = config.get('repository', 'path')
    scmPrefix = config.get('repository', 'scmPrefix')
    
    try:
        exec('from modules.Walker import %s' % walkerName)
        walker = eval(walkerName)(path)
    except ImportError:
        logging.warning('The walker %s was not found.' % walkerName)
    
    # run the source checks
    listOfChecks = config.get('checks','srcChecks').split(',')
    srcDirs = walker.getSourceDirectories()
    if len(srcDirs) > 0:
        runThoseSuperChecks(listOfChecks, srcDirs, scmPrefix) 
    
    # run the test checks
    listOfChecks = config.get('checks','testChecks').split(',')
    testDirs = walker.getTestDirectories()
    if len(testDirs) > 0:
        runThoseSuperChecks(listOfChecks, testDirs, scmPrefix) 
    
    # run the resource checks
    listOfChecks = config.get('checks','resourceChecks').split(',')
    resourceFiles = walker.getResourceFiles()
    if len(resourceFiles) > 0:
        runThoseSuperChecks(listOfChecks, resourceFiles, scmPrefix) 
    
    # run target ckecks
    listOfChecks = config.get('checks','targetChecks').split(',')
    targetFiles = walker.getTargetFiles()    
    if len(targetFiles) > 0:
        runThoseSuperChecks(listOfChecks, targetFiles, scmPrefix) 