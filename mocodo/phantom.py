#!/usr/bin/env python
# encoding: utf-8

import font_metrics


class Phantom:

    def __init__(self, phantom_count = 0):
        self.name = " %s" % phantom_count
        self.attributes = []
        self.legs = [] # iterating over box's legs does nothing if it is not an association
        self.kind = "phantom"
        self.clause = ":"

    def calculate_size(self, style):
        self.w = 0
        self.h = 0