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

import numpy

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

from pysc2.lib import raw_units as ru

_PLAYER_SELF = features.PlayerRelative.SELF
_PLAYER_NEUTRAL = features.PlayerRelative.NEUTRAL  # beacon/minerals
_PLAYER_ENEMY = features.PlayerRelative.ENEMY

FUNCTIONS = actions.FUNCTIONS

class MoveToBeacon(base_agent.BaseAgent):
  """An agent specifically for solving the MoveToBeacon map."""

  def step(self, obs):
    super(MoveToBeacon, self).step(obs)

    raw_units = obs.observation.raw_units
    for u in raw_units:
      if ru.get_unit_owner(u) == 16:
        target = ru.get_unit_pos(u)
      else:
        marine = int(ru.get_unit_tag(u))
        m_pos = ru.get_unit_pos(u)

    # print(target, m_pos)
    # print(marine)

    if FUNCTIONS.Move_raw.id in obs.observation.available_actions:
      return FUNCTIONS.Move_raw("now", target, marine)
      # return FUNCTIONS.no_op()
    else:
      return FUNCTIONS.select_army("select")

    return FUNCTIONS.no_op()