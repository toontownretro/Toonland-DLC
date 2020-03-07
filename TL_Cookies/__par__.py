########################## THE TOON LAND DLC ##########################
# Filename: __par__.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# Loads all of the Toon Land DLC package files into our private namespace
# as module objects. Do not modify.
####

import os
import imp

filepaths = [os.path.join(root, filename)
    for root, folders, files in os.walk(__modulebase__)
    for filename in files
    if (filename.endswith('.py')) and (root != '%s\\security' % __modulebase__)
    if not filename.startswith('_')
]
modules = {}

for filepath in filepaths:
    moduleName = filepath.split('\\')[-1].split('.', 1)[0]
    exec("%s = imp.new_module(moduleName)" % moduleName)
    exec('from __main__ import *', eval(moduleName).__dict__)
    execfile(filepath, eval(moduleName).__dict__)
    modules[moduleName] = eval(moduleName)

for moduleName in modules:
    _globals = dict((key, value) for key, value in globals().items() if (key != moduleName))
    eval(moduleName).__dict__.update(_globals)

execfile('%s\\__init__.py' % __modulebase__)