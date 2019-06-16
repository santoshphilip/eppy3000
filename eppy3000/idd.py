# Copyright (c) 2018-2019 Santosh Philip
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================
"""class for the idd file"""

import json
from munch import Munch


def readiddasmunch(fhandle):
    """read the idd json as a munch"""
    try:
        epjs = json.load(fhandle)
        as_munch = IDDMunch.fromDict(epjs)
        print(1)
    except AttributeError as e:
        try:
            fhandle = open(fhandle, 'r')
            epjs = json.load(fhandle)
            as_munch = IDDMunch.fromDict(epjs)
            print(2)
        except TypeError as e:
            if isinstance(fhandle, IDDMunch):
                print(3)
                return fhandle
            else:
                print(4)
                raise TypeError(f"expected str, bytes, os.PathLike object or Munch, not {type(fhandle)}")
    return as_munch


class IDDMunch(Munch):
    """Munch subcalssed to for the IDD json"""
    def __init__(self, *args, **kwargs):
        super(IDDMunch, self).__init__(*args, **kwargs)

    def fieldnames(self):
        """field names of the IDD object"""
        return [key for key in self.keys()]

    def fieldnames_list(self):
        """fieldnames that contain lists"""
        pass

    def fieldproperty(self, fieldname):
        """field names of the IDD object"""
        return self[fieldname]


class IDD(object):
    """hold the data from the json idd file """
    def __init__(self, iddname):
        super(IDD, self).__init__()
        self.iddname = iddname
        self.read()

    def read(self):
        """read the json file"""
        self.idd = readiddasmunch(self.iddname)
        self.version = self.idd['epJSON_schema_version']
        self.required = self.idd['required']
        self.iddobjects = {key: val['patternProperties']['.*']['properties']
                           for key, val in self.idd['properties'].items()}
