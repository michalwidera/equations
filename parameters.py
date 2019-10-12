#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


class ConfigParameters(object):
    def set_range(self, new_range):
        self.test_range = new_range

    def __init__(self):
        self.set_range(5)


cfg_prm = ConfigParameters()
