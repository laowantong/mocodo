import json
import os
from pathlib import Path


def font_metrics_factory(params):
    class FontMetrics:

        data = json.loads((Path(params["script_directory"]) / "font_metrics.json").read_text())

        def __init__(self, font):
            if font["family"] not in self.data["fonts"]:
                font["family"] = "Courier New"
            ref_size = self.data["size"]
            metrics = self.data["fonts"][font["family"]]
            alphabet = self.data["alphabet"]
            self.font_height = int(round(metrics["height"] * font["size"] / ref_size))
            self.width = {c: ord(x) for (c, x) in zip(alphabet, metrics.get("widths", []))}
            self.ratio = font["size"] * metrics.get("correction", 1) / ref_size
            self.default_width = metrics["default"]

        def get_pixel_height(self):
            return self.font_height

        def get_pixel_width(self, s):
            width = sum(self.width.get(c, self.default_width) for c in s)
            return int(round(self.ratio * width)) + 1

    return FontMetrics
