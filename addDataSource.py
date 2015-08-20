#!/usr/bin/env python
#
################################################
##  Connect to dmd and create a new template  ##
##                   -or-                     ##
##          Create a new Datasource           ##
##                   -or-                     ##
##          Create a new DataPoint            ##
##  If any of the above already exists then   ##
##     the script will just modify or ignore  ##
##     them and move to the next thing that   ##
##     needs to be created.                   ##
################################################
#
# simple example: ./addDataSource.py <datasourcename> <datapointname>
# complicated example:
#  you can have a list of files named after the datasourcename that contains
#  a list of the datapoint names
#  Then you go a bit crazy...
#
#  for resource in $(ls files*.txt)
#  do
#    while read line
#    do
#      sleep 1
#      echo -n "adding" $resource $line "..."
#      ./addDataSource.py $resource $line
#      echo "done"
#    done < $resource
#  done

import sys

import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
dmd = ZenScriptBase(connect=True).dmd

from Products.Zuul import getFacade
from transaction import commit

# Edit the things below
myDeviceClass = "/zport/dmd/Path/To/Device/Class/Here"
myTemplate = "The Template Name"

#Don't edit below here unless you REALLY MEAN IT
myTemplatePath = myDeviceClass + "/rrdTemplates/" + myTemplate
myDataSource = sys.argv[1]
myDataSourcePath = myTemplatePath + "/datasources/" + myDataSource
myCommand = "check_foo -args"
myDataPoint = sys.argv[2]
myDataPointPath = myDataSourcePath + "/datapoints/" + myDataPoint

try:
    #find out if the datapoint already exists
    dmd.getObjByPath(myDataPointPath)
except:
    #an except means it doesn't, so create it.
    facade = getFacade("template")
    facade.addTemplate(myTemplate, myDeviceClass)
    facade.addDataSource(myTemplatePath, myDataSource, "COMMAND")
    facade.setInfo(myDataSourcePath, {'commandTemplate':myCommand})
    facade.addDataPoint(myDataSourcePath, myDataPoint)
    try:
        commit()
    except:
        #sometimes a commit doesn't work because
        #of concurrent reads or whatever.
        #if so, just sleep for a sec and retry
        import time
        time.sleep(2)
        commit()

