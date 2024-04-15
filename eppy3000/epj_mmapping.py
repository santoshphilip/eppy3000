# Copyright (c) 2022 Santosh Philip
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================

"""
Subclass from collections.abc.MutableMapping to get finer control over a dict like
object.

epj.epobjects is a dict and is not connected to epj.model

There are 2 dicts:

- epj.model is the real dict where the epJSON data is held as a dict
- in eppy3000 one does not work directly on epj.model
- one works on epj.epobjects that holds the same data as epj.model
- this means that any operations done on epj.epobjects should make
- equivalent changes in epj.model

This can be done thru subclassing collections.abc.MutableMapping, rather than subclassing dict

https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict

# Alex Martelli describes how to use collections.MutableSequence in
# <http://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list>
"""
# from the link
# https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict
# loolks like we can have a case insensitive keys
# and still retain the original case of the key


# Note:
# The values of the dict are lists
# the list does not have to be subclasses from collections.abc.MutableSequence
# as eppy does
# since bothe the dicts will point to the same list

# how do we incrementally implement this ??
# start by implementing epj.popepobject, epj.removeepobject & epj.removeallepobjects

from collections.abc import MutableMapping
from collections.abc import MutableSequence

# TODO - unit tests. use samples from main() and commented out code at the end of file
# TODO


def epjsequence2dict(epjs):
    """convert the epjsequence to a dict to compare to epj[key]"""
    return {item["eppyname"]: {key: item[key] for key in item} for item in epjs}


class EpjSequence(MutableSequence):
    """simple Mutable Sequence to stes to ut some stuff"""

    def __init__(self, adict, themodel=None):
        super(EpjSequence, self).__init__()
        self.themodel = themodel
        self.list1 = [adict[key] for key in adict]

    def __getitem__(self, i):
        return self.list1[i]

    def __setitem__(self, i, v):
        oldv = self.list1[i]
        self.themodel[oldv["eppykey"]].pop(oldv["eppyname"])
        self.themodel[v["eppykey"]][v["eppyname"]] = v
        self.list1[i] = v

    def __delitem__(self, i):
        val = self.list1[i]
        del self.list1[i]
        self.themodel[val["eppykey"]].pop(val["eppyname"])

    def __len__(self):
        return len(self.list1)

    # __setitem__ should take care of this.
    def insert(self, i, v):
        self.themodel[v["eppykey"]][v["eppyname"]] = v
        self.list1.insert(i, v)

    def __str__(self):
        return self.list1.__str__()

    def __repr__(self):
        return self.list1.__repr__()

    # # TODO - not sure
    # def __eq__(self, other):
    #     """Test for equality uses the IDF.model.dt list, list2."""
    #     return self.list1 == other.list1


class EpjMapping(MutableMapping):
    """simple Mutable mapping to test out some stuff"""

    def __init__(self, themodel):
        super(EpjMapping, self).__init__()
        self.themodel = themodel
        self.store = {
            key: EpjSequence(self.themodel[key], self.themodel) for key in self.themodel
        }

    def __getitem__(self, key):
        return self.store[self._keytransform(key)]

    def __setitem__(self, key, value):
        self.store[self._keytransform(key)] = value
        self.themodel[key] = epjsequence2dict(value)

    def __delitem__(self, key):
        del self.store[self._keytransform(key)]
        del self.themodel[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def _keytransform(self, key):
        return key

    # --- not needed, but coded for readability during usage ----

    def __str__(self):
        return self.store.__str__()

    def __repr__(self):
        return self.store.__repr__()

    def keys(self):
        return self.store.keys()


def eppyfields(epj):
    """put eppy fields into epj"""
    for key in epj:
        for kkey in epj[key]:
            epj[key][kkey]["eppykey"] = key
            epj[key][kkey]["eppyname"] = kkey
    return epj


def main():
    # print("Main")
    # manufactur an epj
    epj = dict(
        Zone=dict(zone1=dict(area=15, type="conditioned")),
        Wall=dict(wall1=dict(area=23, ZoneName="zone1")),
    )
    epj = eppyfields(epj)
    epjmm = EpjMapping(epj)
    # print(epjmm.keys())
    # print(epjmm)


if __name__ == "__main__":
    main()

# print("Main")
# # manufacture an epj
# epj = dict(Zone=dict(zone1=dict(area=15, type="conditioned")), Wall=dict(wall1=dict(area=23, ZoneName="zone1")))
# # for key in epj:
# #     EpjSequence(epj[key])
# # {key:EpjSequence(themodel[key]) for key in themodel}
# epj = eppyfields(epj)
# mm = EpjMapping(epj)
# zones = mm['Zone']
# newzone = dict(eppykey='Zone', eppyname='new zone', area=16, type='unconditioned')
# zones[0] = newzone
# print(mm)
# print(epj)
# mm.pop('Zone')
# print(mm)
# print(epj)
