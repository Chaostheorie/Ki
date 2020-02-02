#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import xmltodict
import json
from pyproj import Transformer
"""
To use this snippet you need to run wfs-downloader first
See https://github.com/Chaostheorie/Ki/tree/master/snippets
"""


def reform(obj):
    """Reforms raw xml dict and simplify keys"""
    return obj


transformer = Transformer.from_crs("EPSG:4326", "EPSG:26917", always_xy=True)

with open('strassenbaeume.xml', 'rb') as f:
    data = xmltodict.parse(f)["wfs:FeatureCollection"]
    trees = [reform(data["wfs:member"]["fis:s_wfs_baumbestand_an"][i])
             for i in range(int(data["@numberReturned"]))]

with open("output.json", "w+") as f:
    json.dump(trees, f)
