# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Scripted agents."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

from pysc2.lib import raw_units as ru
from pysc2.lib import units

_PLAYER_SELF = features.PlayerRelative.SELF
_PLAYER_NEUTRAL = features.PlayerRelative.NEUTRAL  # beacon/minerals
_PLAYER_ENEMY = features.PlayerRelative.ENEMY

FUNCTIONS = actions.FUNCTIONS

class MoveToBeacon(base_agent.BaseAgent):
  """An agent specifically for solving the MoveToBeacon map using the raw interface."""

  def step(self, obs):
    super(MoveToBeacon, self).step(obs)

    raw_units = [ru.RawUnit(u) for u in obs.observation.raw_units]
    for u in raw_units:
      if u.owner == ru.PLAYER_NEUTRAL:
        target = u.pos
      else:
        marine = u.tag

    return FUNCTIONS.Move_raw_pos("now", target, [marine])

class CollectMineralShards(base_agent.BaseAgent):
  """An agent for solving the CollectMineralShards map with feature units using the raw interface."""

  def reset(self):
    super(CollectMineralShards, self).reset()

    self.minerals = []
    self.marines = []
    self.marines_target = []

  def step(self, obs):
    super(CollectMineralShards, self).step(obs)

    raw_units = [ru.RawUnit(u) for u in obs.observation.raw_units]
    if len(self.marines) == 0:
      for u in raw_units:
        if u .owner != ru.PLAYER_NEUTRAL:
          self.marines.append(u)
          self.marines_target.append(0)

    if len(self.minerals) == 0:
      self.minerals = []
      for u in raw_units:
        if u .owner == ru.PLAYER_NEUTRAL:
          self.minerals.append(u)

    for i, m in enumerate(self.marines):
      if self.marines_target[i] not in raw_units:
        self.marines_target[i] = 0

      if self.marines_target[i] == 0 and len(self.minerals) > 0:
        # No order, we will give it one
        # Find closest mineral and send the marine there
        dist = [m.dist_to(x) for x in self.minerals]
        min_idx = np.argmin(dist)
        tar = self.minerals[min_idx]
        self.marines_target[i] = tar.tag
        del self.minerals[min_idx]
        return FUNCTIONS.Move_raw_pos("now", tar.pos, [m.tag])

    return FUNCTIONS.no_op()

class BuildDrone(base_agent.BaseAgent):
  """An agent that tries to build drones."""

  def step(self, obs):
    super(BuildDrone, self).step(obs)

    raw_units = [ru.RawUnit(u) for u in obs.observation.raw_units]

    # See also https://github.com/Blizzard/s2client-proto/blob/238b7a9b38f98504adf934808b1ed61f534048aa/s2clientprotocol/sc2api.proto#L562
    # Note that the food cap and food used seems to be inverted in the prototxt, but not in pysc2
    minerals = obs.observation.player.minerals
    food_cap = obs.observation.player.food_cap
    food_used = obs.observation.player.food_used

    if food_cap > food_used:
      if minerals >= 50:
        for u in raw_units:
          if u.unit_type == units.Zerg.Larva:
            return FUNCTIONS.Train_Drone_raw_quick("now", [u.tag])
            
    elif minerals >= 100:
      for u in raw_units:
          if u.unit_type == units.Zerg.Larva:
            return FUNCTIONS.Train_Overlord_raw_quick("now", [u.tag])

    return FUNCTIONS.no_op()
        
    