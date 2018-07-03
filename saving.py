#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle, os


class document:
    def __init__(self, _warrior, _now_floor, _floors, _police_prob, _police_defeated, _choice, _police_served):
        self.warrior = _warrior
        self.now_floor = _now_floor
        self.floors = _floors
        self.POLICE_PROB = _police_prob
        self.police_defeated = _police_defeated
        self.police_served = _police_served
        self.choice = _choice
    def save(self, _id):
        with open(os.path.join('C:\MagicTowerSavings', _id), "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

def load(_id):
    with open(os.path.join('C:\MagicTowerSavings', _id), "rb") as f:
        return pickle.load(f)
