import copy
import random

from simple_rl.mdp.StateClass import State

# from cleanup_block import CleanUpBlock
from cleanup_mdp import CleanUpMDP


class CleanUpState(State):
    def __init__(self, task, x, y, blocks=[], doors=[], rooms=[]):
        self.x = x
        self.y = y
        self.blocks = blocks
        self.doors = doors
        self.rooms = rooms
        self.task = task
        State.__init__(self, data=[task, (x, y), blocks, doors, rooms])
        # for item in self.data:
        #     print(item)

    def __hash__(self):
        alod = [tuple(self.data[i]) for i in range(1, len(self.data))]
        alod.append(self.data[0])
        return hash(tuple(alod))

    def __str__(self):
        str_builder = "(" + str(self.x) + ", " + str(self.y) + ")\n"
        str_builder += "\nBLOCKS:\n"
        for block in self.blocks:
            str_builder += str(block) + "\n"
        str_builder += "\nDOORS:\n"
        for door in self.doors:
            str_builder += str(door) + "\n"
        str_builder += "\nROOMS:\n"
        for room in self.rooms:
            str_builder += str(room) + "\n"
        return str_builder

    @staticmethod
    def list_eq(alod1, alod2):
        if len(alod1) != len(alod2):
            return False
        sa = set(alod2)
        for item in alod1:
            if item not in sa:
                return False

        return True

        # return sorted(alod1) == sorted(alod2)
        # alod1.sort()
        # alod2.sort()
        # for a1, a2 in alod1, alod2:
        #     if not a1.__eq__(a2):
        #         return False
        # return True

    def __eq__(self, other):
        return isinstance(other, CleanUpState) and self.x == other.x and self.y == other.y and \
               self.list_eq(other.rooms, self.rooms) and self.list_eq(other.doors, self.doors) and \
               self.list_eq(other.blocks, self.blocks)
        # if isinstance(other, CleanUpState) and self.list_eq(other.rooms, self.rooms) and \
        #         self.list_eq(other.doors, self.doors) and self.list_eq(other.blocks, self.blocks):
        #     return True
        # else:
        #     return False

    def is_terminal(self):
        # return CleanUpMDP.is_terminal(next_state=self)
        # return CleanUpMDP.is_terminal()
        # TODO WRITE THIS
        # pass
        return CleanUpMDP.is_terminal(self.task, next_state=self)

    def copy(self):
        # # TODO FILL OUT
        # return self
        new_blocks = [block.copy() for block in self.blocks]
        new_rooms = [room.copy() for room in self.rooms]
        new_doors = [door.copy() for door in self.doors]
        return CleanUpState(self.task, self.x, self.y, new_blocks, new_doors, new_rooms)


    # def visualize_policy(self, policy):
    #     from simple_rl.utils import mdp_visualizer as mdpv
    #     from grid_visualizer import _draw_state
    #     ["up", "down", "left", "right"]
    #
    #     action_char_dict = {
    #         "up":u"\u2191",
    #         "down":u"\u2193",
    #         "left":u"\u2190",
    #         "right":u"\u2192"
    #     }
    #
    #     mdpv.visualize_policy(self, policy, _draw_state, action_char_dict)
    #     raw_input("Press anything to quit ")
    #
    # def visualize_agent(self, agent):
    #     from simple_rl.utils import mdp_visualizer as mdpv
    #     from grid_visualizer import _draw_state
    #     mdpv.visualize_agent(self, agent, _draw_state)
    #     raw_input("Press anything to quit ")
    #
    # def visualize_value(self):
    #     from simple_rl.utils import mdp_visualizer as mdpv
    #     from grid_visualizer import _draw_state
    #     mdpv.visualize_value(self, _draw_state)
    #     raw_input("Press anything to quit ")
    #
    # def visualize_learning(self, agent, delay=0.0):
    #     from simple_rl.utils import mdp_visualizer as mdpv
    #     from grid_visualizer import _draw_state
    #     mdpv.visualize_learning(self, agent, _draw_state, delay=delay)
    #     raw_input("Press anything to quit ")
    #
    # def visualize_interaction(self):
    #     from simple_rl.utils import mdp_visualizer as mdpv
    #     from grid_visualizer import _draw_state
    #     mdpv.visualize_interaction(self, _draw_state)
    #     raw_input("Press anything to quit ")

    # def reset(self):
    #     if self.rand_init:
    #         init_loc = random.randint(0, width), random.randint(0, height)
    #         self.cur_state = CleanUpState(self.task, init_loc[0], init_loc[1], blocks=self.blocks, rooms=self.rooms,
    #                                       doors=self.doors)
    #     else:
    #         self.cur_state = copy.deepcopy(self.init_state)