import copy
import random

from simple_rl.agents import QLearningAgent, RandomAgent, RMaxAgent, FixedPolicyAgent, DelayedQAgent
from simple_rl.mdp.MDPClass import MDP
from simple_rl.planning import ValueIteration
from simple_rl.run_experiments import run_agents_on_mdp

# from cleanup_block import CleanUpBlock
# from cleanup_door import CleanUpDoor
# from cleanup_room import CleanUpRoom

# TODO UNSURE IF I'M SUPPOSED TO BE COPYING STUFF OR NOT
from cleanup_task import CleanUpTask


class CleanUpMDP(MDP):
    ACTIONS = ["up", "down", "left", "right"]
    CLASSES = ["room", "block", "door"]

    # TODO NOTE MAYBE ADD AGENT CLASS.  SEE THE TAXI OOMDP CLASS

    def __init__(self, task, init_loc=(0, 0), blocks=[], rooms=[], doors=[], rand_init=False, gamma=0.99,
                 init_state=None):
        from cleanup_state import CleanUpState
        self.task = task
        # self.rand_init = rand_init
        if rand_init:
            block_loc = [(x, y) for block in blocks for (x, y) in (block.x, block.y)]
            init_loc = random.choice(
                [(x, y) for room in rooms for (x, y) in room.points_in_room if (x, y) not in block_loc])
        self.init_state = CleanUpState(task, init_loc[0], init_loc[1], blocks=blocks, doors=doors, rooms=rooms) \
            if init_state is None or rand_init else init_state
        self.cur_state = init_state
        MDP.__init__(self, self.ACTIONS, self._transition_func, self._reward_func, init_state=init_state, gamma=gamma)
        legal_states = [(x, y) for room in rooms for x, y in room.points_in_room]
        legal_states.extend([(door.x, door.y) for door in doors])
        self.legal_states = set(legal_states)
        self.rooms = rooms
        self.doors = doors

    def _transition_func(self, state, action):
        # TODO ACCOUNT FOR PULL ACTION
        dx, dy = self.transition(action)
        new_x = state.x + dx
        new_y = state.y + dy
        copy = state.copy()
        if (new_x, new_y) not in self.legal_states:
            return copy

        blocks = self._account_for_blocks(new_x, new_y, state, action)
        if blocks is not None:
            copy.blocks = blocks
            copy.x = new_x
            copy.y = new_y

        # print("Agent " + str((copy.x, copy.y)))
        # print("Block " + str((copy.blocks[0].x, copy.blocks[0].y)))
        # print(str(copy))

        return copy

    def _account_for_blocks(self, x, y, state, action):
        copy_blocks = state.blocks[:]
        if x == state.x and y == state.y:
            return copy_blocks
        for i in range(len(state.blocks)):
            block = state.blocks[i]
            if x == block.x and y == block.y:
                dx, dy = self.transition(action)
                new_x = block.x + dx
                new_y = block.y + dy
                if (new_x, new_y) not in self.legal_states:
                    return None
                else:
                    block = block.copy()
                    block.x = new_x
                    block.y = new_y
                    copy_blocks[i] = block
                    return copy_blocks
        return copy_blocks

        # old_room = self.check_in_room(state, state.x, state.y)
        # new_room = self.check_in_room(state, new_x, new_y)
        # copy = state.copy()
        # if not old_room:
        #     print(str(state))
        #     print(action)
        # # assert old_room != False
        # still_in_room = new_room and old_room and old_room.__eq__(new_room)
        # # print(still_in_room)
        # # TODO BUG HERE.  CAN'T MOVE TO OTHER ROOMS WELL
        # if not still_in_room and (bool(new_room) or bool(old_room)):
        #     door_points = [(door.x, door.y) for door in state.doors]
        #     if (state.x, state.y) in door_points or (state.x + dx, state.y + dy) in door_points:
        #         print(str((state.x, state.y)))
        #         print("moving to new room")
        #         # print(str((new_x, new_y)))
        #
        #         # if still_in_room:
        #         blocks = state.account_for_blocks(new_x, new_y, action)
        #         if blocks is not None:
        #             copy.blocks = blocks
        #             copy.x = new_x
        #             copy.y = new_y
        # # print(str(copy))
        # else:
        #
        #     blocks = state.account_for_blocks(new_x, new_y, action)
        #     if blocks is not None:
        #         # print("here")
        #         copy.blocks = blocks
        #         copy.x = new_x
        #         copy.y = new_y
        # print(str(copy.blocks[0]))
        # print(str(copy))
        return copy

        # x = state.x + dx if still_in_room else state.x
        # y = state.y + dy if still_in_room else state.y
        # new_x = state.x + dx
        # new_y = state.y + dy
        #
        # # if still_in_room:
        # blocks = state.account_for_blocks(new_x, new_y, action)
        # if blocks is None:
        #     return copy
        #
        # copy.blocks = blocks
        # return copy

    def check_in_room(self, x, y):
        for room in self.rooms:
            if (x, y) in room.points_in_room:
                return room
        return False

    @staticmethod
    def transition(action):
        dx = 0
        dy = 0
        if action == "up":
            dx = 0
            dy = 1
        elif action == "down":
            dx = 0
            dy = -1
        elif action == "left":
            dx = -1
            dy = 0
        elif action == "right":
            dx = 1
            dy = 0
        return dx, dy

    def _reward_func(self, state, action):
        next_state = self.transition_func(state, action)
        # for task in self.tasks:
        # task_block = None


        # if task_room.contains(task_block):
        #     print("It successfully got to the goal")
        # print(10.0 if task_room.contains(task_block) else 0.0)
        if self.is_terminal(self.task, state):
            return 0.0
        return 1000.0 if self.is_terminal(self.task, next_state) else -1.0

    @staticmethod
    def is_terminal(task, next_state):
        if task.block_name is None:
            task_block = [block for block in next_state.blocks if block.color == task.block_color][0]
        # elif self.task.block_name is None:
        else:
            task_block = [block for block in next_state.blocks if block.name == task.block_name][0]

        # task_room = None

        if task.goal_room_name is None:
            task_room = [room for room in next_state.rooms if room.color == task.goal_room_color][0]
        else:
            task_room = [room for room in next_state.rooms if room.name == task.goal_room_name][0]

        return task_room.contains(task_block)

    def __str__(self):
        # TODO WRITE OUT LATER
        return "CleanUpMDP: " + str(self.task)

    # def get_init_state(self):
    #     return self.init_state

    def get_actions(self):
        return self.ACTIONS

    def reset(self):
        self.cur_state = copy.deepcopy(self.init_state)
        if self.rand_init:
            block_loc = [(x, y) for block in blocks for (x, y) in (block.x, block.y)]
            new_loc = random.choice([(x, y) for room in self.init_state.rooms for (x, y) in
                                     room.points_in_room if (x, y) not in block_loc])
            self.cur_state.x, self.cur_state.y = new_loc

    def visualize_agent(self, agent):
        from simple_rl.utils import mdp_visualizer as mdpv
        from cleanup_visualizer import draw_state
        mdpv.visualize_agent(self, agent, draw_state)
        input("Press anything to quit ")

    def visualize_value(self):
        from simple_rl.utils import mdp_visualizer as mdpv
        from cleanup_visualizer import draw_state
        mdpv.visualize_value(self, draw_state)
        input("Press anything to quit ")

    def visualize_learning(self, agent, delay=0.0):
        from simple_rl.utils import mdp_visualizer as mdpv
        from cleanup_visualizer import draw_state
        mdpv.visualize_learning(self, agent, draw_state, delay=delay)
        input("Press anything to quit")

    def visualize_interaction(self):
        from simple_rl.utils import mdp_visualizer as mdpv
        from cleanup_visualizer import draw_state
        mdpv.visualize_interaction(self, draw_state)
        input("Press anything to quit ")


if __name__ == "__main__":
    from cleanup_block import CleanUpBlock
    from cleanup_door import CleanUpDoor
    from cleanup_room import CleanUpRoom

    task = CleanUpTask("blue", "red")
    room1 = CleanUpRoom("room1", [(x, y) for x in range(5) for y in range(3)], "blue")
    block1 = CleanUpBlock("block1", 1, 1, color="blue")
    room2 = CleanUpRoom("room2", [(x, y) for x in range(5, 10) for y in range(3)], color="red")
    rooms = [room1, room2]
    blocks = [block1]
    doors = [CleanUpDoor(4, 2)]
    mdp = CleanUpMDP(task, rooms=rooms, doors=doors, blocks=blocks)
    mdp.visualize_interaction()

    # vi = ValueIteration(mdp)
    # vi.run_vi()
    # print(vi.get_num_states())
    #
    # action_seq, state_seq = vi.plan(mdp.get_init_state())
    # vi.print_value_func()
    #
    # for i in range(len(action_seq)):
    #     print("action: " + action_seq[i])
    #     print("agent: " + str((state_seq[i].x, state_seq[i].y)))
    #     print("block: " + str((state_seq[i].blocks[0].x, state_seq[i].blocks[0].y)))
    #     # print("\t", action_seq[i], state_seq[i])

    # ql_agent = QLearningAgent(actions=mdp.get_actions())
    # rand_agent = RandomAgent(actions=mdp.get_actions())
    # delayed_q = DelayedQAgent(actions=mdp.get_actions())
    # rmax_agent = RMaxAgent(actions=mdp.get_actions())
    # run_agents_on_mdp([ql_agent, rand_agent, delayed_q, rmax_agent], mdp, instances=5, episodes=100, steps=40,
    #                   reset_at_terminal=True, verbose=False)











    # def _reward_func(self, state, action):
    #     if self.is_goal_state(state, action):
    #         return 1.0 - self.step_cost
    #     else:
    #         return -self.step_cost

    # def is_goal_state(self, state, action):
    #     # Makes sure each block is in its corresponding room
    #     new_state = self.transition_func(state, action)
    #     for block, goal_room in new_state.blocks, self.goal_locs:
    #         if not goal_room.contains(block):
    #             # The block is not in the correct room so return false
    #             return False
    #
    #     if self.is_goal_terminal:
    #         return False
    #     return True

## TODO NOTE CURRENTLY ASSUMING ONE BLOCK FOR EACH GOAL LOCATION
## TODO ASSUMING GOAL_LOCS IS A SET OF ROOMS
# def __init__(self, width=24, height=24, init_loc=(1, 1), rand_init=False,
#              goal_locs=[CleanUpRoom([(x + 1, y + 1) for x in range(24) for y in range(24)])], walls=[],
#              is_goal_terminal=True, include_direction_attribute=False, include_pull_action=False,
#              include_wall_pf_s=False, lockable_doors=False, lock_prob=0.5, gamma=0.99, init_state=None,
#              slip_prob=0.0, step_cost=0.0, name="gridworld"):
#     self.width = width
#     self.height = height
#     if rand_init and len(walls) < width * height:
#         init_loc = random.randint(1, width), random.randint(1, height)
#         while init_loc in walls:
#             init_loc = random.randint(1, width), random.randint(1, height)
#     self.init_loc = init_loc
#
#     self.goal_locs = goal_locs
#     self.walls = walls
#
#     self.include_direction_attribute = include_direction_attribute
#     # TODO ACCOUNT FOR PULL ACTION
#     self.include_pull_action = include_pull_action
#     if include_pull_action:
#         self.ACTIONS.append("pull")
#
#     self.include_wall_pf_s = include_wall_pf_s
#     self.lockable_doors = lockable_doors
#     self.lock_prob = lock_prob
#
#     init_state = CleanUpState(init_loc[0], init_loc[1]) if init_state is None or rand_init else init_state
#
#     MDP.__init__(self, self.ACTIONS, self._transition_func, self._reward_func, init_state=init_state, gamma=gamma)
#
#     if type(goal_locs) is not list:
#         raise ValueError(
#             "(simple_rl) GridWorld Error: argument @goal_locs needs to be a list of locations. For example: [(3,3), (4,3)].")
#
#     self.is_goal_terminal = is_goal_terminal
#     self.slip_prob = slip_prob
#     self.step_cost = step_cost
#     self.name = name
