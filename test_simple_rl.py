# Add simple_rl to system path.
import os
import sys

import pygame

if __name__=="__main__":
    pass

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, parent_dir)

from simple_rl.agents import QLearningAgent, RandomAgent, RMaxAgent
from simple_rl.planning import ValueIteration
from simple_rl.tasks import GridWorldMDP
from simple_rl.run_experiments import run_agents_on_mdp

# # Setup MDP.
# mdp = GridWorldMDP(width=6, height=6, init_loc=(1, 1), goal_locs=[(6, 6)])
#
# # Setup Agents.
# ql_agent = QLearningAgent(actions=mdp.get_actions())
# rand_agent = RandomAgent(actions=mdp.get_actions())
# rmax_agent = RMaxAgent(actions=mdp.get_actions(), horizon=3, s_a_threshold=1)
#
# # Run experiment and make plot.
# run_agents_on_mdp([ql_agent, rand_agent, rmax_agent], mdp, instances=5, episodes=100, steps=40, reset_at_terminal=True,
#                   verbose=False)

from simple_rl.tasks import FourRoomMDP
from simple_rl.tasks.grid_world import grid_visualizer

four_room_mdp = FourRoomMDP(9, 9, goal_locs=[(9, 9), (5, 4)], gamma=0.95)

# Run experiment and make plot.
pygame.event.get()
four_room_mdp.visualize_value()
pygame.event.get()
# four_room_mdp.visualize_policy()