#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os.path
from ki import db
from ki.models import Trees

if len(sys.argv) < 2:
    print("No source file specified, assume output.json as source file")
    source = "output.json"
else:
    source = sys.argv[1]
if not os.path.isfile(source):
    raise FileNotFoundError(f"Source file {source} was not found")
with open(source) as f:
    data = json.load(f)
    [db.session.add(Trees.parse(data[i])) for i in range(len(data))]
db.session.commit()
