# Python imports.
from __future__ import print_function
from collections import defaultdict
try:
    import pygame
except ImportError:
    print("Warning: pygame not installed (needed for visuals).")
import random
import sys

# Other imports.
from simple_rl.planning import ValueIteration

def _draw_state(screen,
                cleaup_mdp,
                state,
                policy=None,
                action_char_dict={},
                show_value=False,
                agent=None,
                draw_statics=False,
                agent_shape=None):
    '''
    Args:
        screen (pygame.Surface)
        grid_mdp (MDP)
        state (State)
        show_value (bool)
        agent (Agent): Used to show value, by default uses VI.
        draw_statics (bool)
        agent_shape (pygame.rect)

    Returns:
        (pygame.Shape)
    '''
    # Make value dict.
    val_text_dict = defaultdict(lambda: defaultdict(float))
    if show_value:
        if agent is not None:
            # Use agent value estimates.
            for s in agent.q_func.keys():
                val_text_dict[s.x][s.y] = agent.get_value(s)
        else:
            # Use Value Iteration to compute value.
            vi = ValueIteration(cleanup_mdp)
            vi.run_vi()
            for s in vi.get_states():
                val_text_dict[s.x][s.y] = vi.get_value(s)

    # Make policy dict.
    policy_dict = defaultdict(lambda: defaultdict(str))
    if policy:
        vi = ValueIteration(cleanup_mdp)
        vi.run_vi()
        for s in vi.get_states():
            policy_dict[s.x][s.y] = policy(s)

    # Prep some dimensions to make drawing easier.
    scr_width, scr_height = screen.get_width(), screen.get_height()
    width_buffer = scr_width / 10.0
    height_buffer = 30 + (scr_height / 10.0)  # Add 30 for title.

    width = max(cleaup_mdp.legal_states, key=lambda tup: tup[0])[0]
    height = max(cleaup_mdp.legal_states, key=lambda tup: tup[1])[1]

    cell_width = (scr_width - width_buffer * 2) / width
    cell_height = (scr_height - height_buffer * 2) / height
    # goal_locs = grid_mdp.get_goal_locs()
    # lava_locs = grid_mdp.get_lava_locs()
    font_size = int(min(cell_width, cell_height) / 4.0)
    reg_font = pygame.font.SysFont("CMU Serif", font_size)
    cc_font = pygame.font.SysFont("Courier", font_size * 2 + 2)

    # TODO WORKING HERE. FOLLOWING GRID_VISUALIZER