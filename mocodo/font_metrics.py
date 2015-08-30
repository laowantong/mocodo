#!/usr/bin/env python
# encoding: utf-8

import sys
import codecs
import os
import json


def font_metrics_factory(params):
    if params["tkinter"]:
        try:
            import Tkinter as tk
            import tkFont
            root = tk.Tk()
        except:
            root = None
        if root:
            
            class FontMetricsWithTk():

                def __init__(self, font):
                    kargs = dict((str(k), v) for (k, v) in font.iteritems())
                    kargs["size"] = -font["size"]
                    self.font = tkFont.Font(**kargs)

                def get_pixel_height(self):
                    return self.font.metrics("linespace")

                def get_pixel_width(self, string):
                    return self.font.measure(string)
            return FontMetricsWithTk
            
        sys.stderr.write(u"Warning: Tkinter is not correctly installed or Mocodo is run on server side with no display. Option 'tkinter' ignored.\n")
    path = os.path.join(params["script_directory"], "font_metrics.json")
    text = codecs.open(path, "r", "utf8").read()
    
    class FontMetricsWithoutTk():

        def __init__(self, font):
            if font["family"] not in self.static_data["fonts"]:
                # sys.stderr.write(u"Warning: Missing metrics for font '%s'. If it is installed on your system, you may run update_font_metrics.py to add it (require Tkinter). In the meantime, I will replace it by Courier New.\n" % font["family"])
                font["family"] = u"Courier New"
            ref_size = self.static_data["size"]
            metrics = self.static_data["fonts"][font["family"]]
            self.font_height = int((metrics["height"] * font["size"] + 0.5) / ref_size)
            self.width = dict((c, ord(x)) for (c, x) in zip(
                self.static_data["alphabet"], metrics.get("widths", [])))
            self.ratio = font["size"] * metrics.get("correction", 1.0) / ref_size
            self.default_width = metrics["default"]

        def get_pixel_height(self):
            return self.font_height

        def get_pixel_width(self, string):
            return int(self.ratio * sum(self.width.get(c, self.default_width) for c in string) + 0.5)
    
    FontMetricsWithoutTk.static_data = json.loads(text)
    return FontMetricsWithoutTk




