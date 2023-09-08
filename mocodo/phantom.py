class Phantom:

    counter = 0

    @classmethod
    def reset_counter(cls):
        cls.counter = 0

    def __init__(self):
        self.name_view = self.name = f" {Phantom.counter}"
        Phantom.counter += 1
        self.attributes = []
        self.legs = [] # iterating over box's legs does nothing if it is not an association
        self.kind = "phantom"
        self.source = ":"
        self.identifier = None
        self.page = 0

    def calculate_size(self, *ignored):
        self.w = 0
        self.h = 0

    def register_center(self, geo):
        pass

    def register_boxes(self, boxes):
        self.boxes = boxes
