class CleanUpDoor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(tuple([self.x, self.y]))

    def copy(self):
        return CleanUpDoor(self.x, self.y)

    def __eq__(self, other):
        return isinstance(other, CleanUpDoor) and self.x == other.x and self.y == other.y

    def __str__(self):
        return str((self.x, self.y))







    # # TODO NOTE:  NOT YET ACCOUNTING FOR LOCKED DOORS
    # # def __init__(self, top, bottom, left, right, name="door1", locked=False, can_be_locked=False):
    # #     self.name = name
    # #     self.locked = locked
    # #     self.top = top
    # #     self.bottom = bottom
    # #     self.left = left
    # #     self.right = right
    # #     self.can_be_locked = can_be_locked
    # def __init__(self, top, bottom, left, right, name="door1"):
    #     self.name = name
    #     self.top = top
    #     self.bottom = bottom
    #     self.left = left
    #     self.right = right
    #
    # @staticmethod
    # def class_name():
    #     return "door"
    #
    # def copy(self):
    #     return CleanUpDoor(self.top, self.bottom, self.left, self.right, self.name)
    #     # return CleanUpDoor(self.top, self.bottom, self.left, self.right, self.name, self.locked, self.can_be_locked)
    #
    # def __str__(self):
    #     return "name: " + self.name + ", top: " + str(self.top) + ", bottom: " + str(self.bottom) + ", left: " + str(
    #         self.left) + ", right: " + str(self.right) + "."
    #     # return "name: " + self.name + ", top: " + str(self.top) + ", bottom: " + str(self.bottom) + ", left: " + str(
    #     #     self.left) + ", right: " + str(self.right) + ", locked: " + str(self.locked) + ", can be locked: " + str(
    #     #     self.can_be_locked)
