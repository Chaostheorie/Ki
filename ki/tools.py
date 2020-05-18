__doc__ = "Ki CLI Toolkit helper functions"


def reform(transformer, obj):
    """Reforms raw xml dict, coords and simplify keys"""
    res = dict()
    for key, val in obj.items():
        if key == "fis:ORA_GEOMETRY":
            continue
        elif key[:3] == "fis":
            res[str(key[4:]).lower()] = val
        else:
            res[key] = val
    coords = obj["fis:ORA_GEOMETRY"]["gml:Point"]["gml:pos"].split(" ")
    res["coords"] = transformer.transform(coords[0], coords[1])
    return res
