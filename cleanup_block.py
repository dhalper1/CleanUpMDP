class CleanUpBlock:

    def __init__(self, name, x=0, y=0, shape="", color=""):
        self.name = name
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    @staticmethod
    def class_name():
        return "block"

    def name(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, CleanUpBlock) and self.x == other.x and self.y == other.y and self.name == other.name \
               and self.shape == other.shape and self.color == other.color

    def __hash__(self):
        # return hash(self.name) ^ hash(self.x) ^ hash(self.y) ^ hash(self.shape) ^ hash(self.color)
        return hash(tuple([self.name, self.x, self.y, self.shape, self.color]))

    def copy_with_name(self, new_name):
        return CleanUpBlock(new_name, x=self.x, y=self.y, shape=self.shape, color=self.color)

    @staticmethod
    def variable_keys():
        return ["x", "y", "shape", "color"]

    def get(self, variable_key):
        if variable_key == "x":
            return self.x
        elif variable_key == "y":
            return self.y
        elif variable_key == "shape":
            return self.shape
        elif variable_key == "color":
            return self.color
        else:
            return None

    def copy(self):
        return CleanUpBlock(name=self.name, x=self.x, y=self.y, shape=self.shape, color=self.color)

    def __str__(self):
        return "BLOCK.  Name: " + self.name + ", (x,y): (" + str(self.x) + "," + str(self.y) + "), Shape: " + \
                self.shape + ", Color: " + self.color
