import json
from pathlib import Path


def font_metrics_factory(params):
    class FontMetrics:

        data = json.loads((Path(params["script_directory"]) / "resources" / "font_metrics.json").read_text("utf8"))

        def __init__(self, font):
            if font["family"] not in self.data["fonts"]:
                font["family"] = "Courier New"
            metrics = self.data["fonts"][font["family"]]
            self.font_height = int(round(metrics["height"] * font["size"] / self.data["size"]))
            alphabet = self.data["alphabet"]
            self.width = {c: ord(x) for (c, x) in zip(alphabet, metrics.get("widths", []))}
            self.default_width = metrics["default"]
            self.ratio = font["size"] * metrics.get("correction", 1) / self.data["size"]
            self.ratio *= params["adjust_width"]

        def get_pixel_height(self):
            return self.font_height

        def get_pixel_width(self, s):
            width = sum(self.width.get(c, self.default_width) for c in s)
            return int(round(self.ratio * width)) + 1

    return FontMetrics
