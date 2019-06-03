"""explore how to read the original idf to the new json"""

from io import StringIO
import json
from munch import Munch

from eppy3000 import rawidf
from eppy3000 import readidd

def readiddasmunch(fhandle):
    """read the idd json as a munch"""
    epjs = json.load(fhandle)
    as_munch = Munch.fromDict(epjs)
    return as_munch

def num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError as e:
            return s


idftxt = """
Timestep,4;

Building,
    Bldg one,                !- Name
    30.,                     !- North Axis {deg}
    City,                    !- Terrain
    0.04,                    !- Loads Convergence Tolerance Value
    0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
    FullExterior,            !- Solar Distribution
    25,                      !- Maximum Number of Warmup Days
    6;                       !- Minimum Number of Warmup Days

Zone,
    Main Zone,               !- Name
    0,                       !- Direction of Relative North {deg}
    0,                       !- X Origin {m}
    0,                       !- Y Origin {m}
    0,                       !- Z Origin {m}
    1,                       !- Type
    1,                       !- Multiplier
    autocalculate,           !- Ceiling Height {m}
    autocalculate;           !- Volume {m3}

Zone,
    Another Zone,               !- Name
    90,                       !- Direction of Relative North {deg}
    11,                       !- X Origin {m}
    22,                       !- Y Origin {m}
    33,                       !- Z Origin {m}
    1,                       !- Type
    1,                       !- Multiplier
    autocalculate,           !- Ceiling Height {m}
    autocalculate;           !- Volume {m3}

"""

iddjson = """ {
    "epJSON_schema_version": "8.9.0",
    "$schema": "http://json-schema.org/draft-04/schema#",
    "required": [
        "Building",
        "GlobalGeometryRules"
    ],
    "properties": {
        "Zone": {
            "name": {
                "is_required": true,
                "type": "string",
                "reference": [
                    "AirflowNetworkNodeAndZoneNames",
                    "OutFaceEnvNames",
                    "ZoneAndZoneListNames",
                    "ZoneNames"
                ]
            },
            "format": "vertices",
            "memo": "Defines a thermal zone of the building.",
            "patternProperties": {
                ".*": {
                    "type": "object",
                    "properties": {
                        "direction_of_relative_north": {
                            "units": "deg",
                            "default": 0.0,
                            "type": "number"
                        },
                        "zone_outside_convection_algorithm": {
                            "note": "Will default to same value as SurfaceConvectionAlgorithm:Outside object setting this field overrides the default SurfaceConvectionAlgorithm:Outside for this zone SimpleCombined = Combined radiation and convection coefficient using simple ASHRAE model TARP = correlation from models developed by ASHRAE, Walton, and Sparrow et. al. MoWiTT = correlation from measurements by Klems and Yazdanian for smooth surfaces DOE-2 = correlation from measurements by Klems and Yazdanian for rough surfaces AdaptiveConvectionAlgorithm = dynamic selection of correlations based on conditions",
                            "enum": [
                                "",
                                "AdaptiveConvectionAlgorithm",
                                "DOE-2",
                                "MoWiTT",
                                "SimpleCombined",
                                "TARP"
                            ],
                            "type": "string"
                        },
                        "z_origin": {
                            "units": "m",
                            "default": 0.0,
                            "type": "number"
                        },
                        "floor_area": {
                            "note": "If this field is 0.0, negative or autocalculate, then the floor area of the zone is automatically calculated and used in subsequent calculations. If this field is positive, then the number entered here will be used.",
                            "units": "m2",
                            "default": "Autocalculate",
                            "anyOf": [
                                {
                                    "type": "number"
                                },
                                {
                                    "enum": [
                                        "",
                                        "Autocalculate"
                                    ],
                                    "type": "string"
                                }
                            ]
                        },
                        "zone_inside_convection_algorithm": {
                            "note": "Will default to same value as SurfaceConvectionAlgorithm:Inside object setting this field overrides the default SurfaceConvectionAlgorithm:Inside for this zone Simple = constant natural convection (ASHRAE) TARP = variable natural convection based on temperature difference (ASHRAE) CeilingDiffuser = ACH based forced and mixed convection correlations for ceiling diffuser configuration with simple natural convection limit AdaptiveConvectionAlgorithm = dynamic selection of convection models based on conditions TrombeWall = variable natural convection in an enclosed rectangular cavity",
                            "enum": [
                                "",
                                "AdaptiveConvectionAlgorithm",
                                "CeilingDiffuser",
                                "Simple",
                                "TARP",
                                "TrombeWall"
                            ],
                            "type": "string"
                        },
                        "ceiling_height": {
                            "note": "If this field is 0.0, negative or autocalculate, then the average height of the zone is automatically calculated and used in subsequent calculations. If this field is positive, then the number entered here will be used. Note that the Zone Ceiling Height is the distance from the Floor to the Ceiling in the Zone, not an absolute height from the ground.",
                            "units": "m",
                            "default": "Autocalculate",
                            "anyOf": [
                                {
                                    "type": "number"
                                },
                                {
                                    "enum": [
                                        "",
                                        "Autocalculate"
                                    ],
                                    "type": "string"
                                }
                            ]
                        },
                        "part_of_total_floor_area": {
                            "default": "Yes",
                            "enum": [
                                "",
                                "No",
                                "Yes"
                            ],
                            "type": "string"
                        },
                        "volume": {
                            "note": "If this field is 0.0, negative or autocalculate, then the volume of the zone is automatically calculated and used in subsequent calculations. If this field is positive, then the number entered here will be used.",
                            "units": "m3",
                            "default": "Autocalculate",
                            "anyOf": [
                                {
                                    "type": "number"
                                },
                                {
                                    "enum": [
                                        "",
                                        "Autocalculate"
                                    ],
                                    "type": "string"
                                }
                            ]
                        },
                        "multiplier": {
                            "default": 1.0,
                            "minimum": 1.0,
                            "type": "number"
                        },
                        "y_origin": {
                            "units": "m",
                            "default": 0.0,
                            "type": "number"
                        },
                        "type": {
                            "default": 1.0,
                            "minimum": 1.0,
                            "type": "number",
                            "maximum": 1.0
                        },
                        "x_origin": {
                            "units": "m",
                            "default": 0.0,
                            "type": "number"
                        }
                    }
                }
            },
            "legacy_idd": {
                "numerics": {
                    "fields": [
                        "direction_of_relative_north",
                        "x_origin",
                        "y_origin",
                        "z_origin",
                        "type",
                        "multiplier",
                        "ceiling_height",
                        "volume",
                        "floor_area"
                    ]
                },
                "field_info": {
                    "direction_of_relative_north": {
                        "field_type": "n",
                        "field_name": "Direction of Relative North"
                    },
                    "zone_outside_convection_algorithm": {
                        "field_type": "a",
                        "field_name": "Zone Outside Convection Algorithm"
                    },
                    "name": {
                        "field_type": "a",
                        "field_name": "Name"
                    },
                    "z_origin": {
                        "field_type": "n",
                        "field_name": "Z Origin"
                    },
                    "floor_area": {
                        "field_type": "n",
                        "field_name": "Floor Area"
                    },
                    "zone_inside_convection_algorithm": {
                        "field_type": "a",
                        "field_name": "Zone Inside Convection Algorithm"
                    },
                    "ceiling_height": {
                        "field_type": "n",
                        "field_name": "Ceiling Height"
                    },
                    "part_of_total_floor_area": {
                        "field_type": "a",
                        "field_name": "Part of Total Floor Area"
                    },
                    "volume": {
                        "field_type": "n",
                        "field_name": "Volume"
                    },
                    "multiplier": {
                        "field_type": "n",
                        "field_name": "Multiplier"
                    },
                    "y_origin": {
                        "field_type": "n",
                        "field_name": "Y Origin"
                    },
                    "type": {
                        "field_type": "n",
                        "field_name": "Type"
                    },
                    "x_origin": {
                        "field_type": "n",
                        "field_name": "X Origin"
                    }
                },
                "alphas": {
                    "fields": [
                        "name",
                        "zone_inside_convection_algorithm",
                        "zone_outside_convection_algorithm",
                        "part_of_total_floor_area"
                    ]
                },
                "fields": [
                    "name",
                    "direction_of_relative_north",
                    "x_origin",
                    "y_origin",
                    "z_origin",
                    "type",
                    "multiplier",
                    "ceiling_height",
                    "volume",
                    "floor_area",
                    "zone_inside_convection_algorithm",
                    "zone_outside_convection_algorithm",
                    "part_of_total_floor_area"
                ]
            },
            "type": "object"
        }
    },
    "epJSON_schema_build": "40101eaafd"
}
"""

fhandle = StringIO(idftxt)
raw_idf = rawidf.readrawidf(fhandle)
# raw_idf can come with upper for idfobject names. need code to change them back to natural. Map between what is in iddjson and make a dict from capts to natural. test using the upper in readrawidf() that has been commented out.
js = readiddasmunch(StringIO(iddjson))
iddpath = "/Applications/EnergyPlus-9-0-1/Energy+.schema.epJSON"
js = readiddasmunch(open(iddpath, 'r'))

# print(js.properties.Zone.legacy_idd.fields)
# print('-')
# print(js.properties.Zone.legacy_idd.numerics.fields)
# print('-')
# print(js.properties.Zone.legacy_idd.alphas.fields)

idfobjcount = {}
idfjson = {}
keys = raw_idf.keys()
order = 0
for key in keys:
    count = idfobjcount.setdefault(key, 0)
    idfobjcount[key] = count + 1
    dct = idfjson.setdefault(key, dict())
    fieldnames = js.properties[key].legacy_idd.fields
    idfobjects = raw_idf[key]
    for idfobject in idfobjects:
        order += 1
        if fieldnames[0] == 'name':
            alst = {fieldname:idfvalue for idfvalue, fieldname in zip(idfobject[2:], fieldnames[1:])}
            dct.update({idfobjectname:alst})
        else:
            alst = {fieldname:idfvalue for idfvalue, fieldname in zip(idfobject[1:], fieldnames)}
            idfobjectname = f"{key} {idfobjcount[key]}"
        alst["idf_order"] = order
        numericfields = js.properties[key].legacy_idd.numerics.fields
        for fieldkey in alst.keys():
            if fieldkey in numericfields:
                alst[fieldkey] = num(alst[fieldkey])
        dct.update({idfobjectname:alst})

print(idfjson)




