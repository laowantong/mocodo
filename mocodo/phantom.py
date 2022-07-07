class Phantom:

    def __init__(self, phantom_count = 0):
        self.name_view = self.name = " %s" % phantom_count
        self.attributes = []
        self.legs = [] # iterating over box's legs does nothing if it is not an association
        self.kind = "phantom"
        self.clause = ":"
        self.identifier = None
        self.page = 0

    def calculate_size(self, *ignored):
        self.w = 0
        self.h = 0

    def register_center(self, geo):
        pass

    def register_boxes(self, boxes):
        self.boxes = boxes
