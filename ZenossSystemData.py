#!/bin/env python

import zlib
import pickle
import json
from pprint import pprint as pp

dat = open("ZenossSystemData.dat", "r").read()
data = zlib.decompress(dat)


dill = pickle.dumps(data)

sweet = json.dumps(dill) #, sort_keys=True,
#                   indent=4, separators=(',', ': '))


sweet = sweet.strip("\"S'")
sweet = sweet.strip("\\n'\np0\n.")
sweet = sweet.translate(None, "\\")
sweet = sweet.translate(None, "\\'")

pp(sweet)
