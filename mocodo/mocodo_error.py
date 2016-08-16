#!/usr/bin/env python
# encoding: utf-8

import textwrap
import sys

class MocodoError(Exception):
    
    def __init__(self, errno, message):
        if sys.version_info.major == 2:
            message = message.encode("utf-8")
        message = textwrap.fill("Mocodo Err.%s - %s" % (errno, message), 80)
        super(MocodoError, self).__init__(message)
