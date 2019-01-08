from .point import Point

PLAYER_NEUTRAL = 16

# See the numpy array definition on line 987 in features.py
class RawUnit():
    def __init__(self, np_array):
        self.unit_type, \
        self.alliance, \
        self.health, \
        self.shield, \
        self.energy, \
        self.cargo_space_taken, \
        self.build_progress, \
        self.health_percent, \
        self.shield_percent, \
        self.energy_percent, \
        self.display_type, \
        self.owner, \
        self.posx, \
        self.posy, \
        self.facing, \
        self.screen_radius, \
        self.cloak, \
        self.is_selected, \
        self.blip, \
        self.is_powered, \
        self.mineral_contents, \
        self.vespene_contents, \
        self.cargo_space_max, \
        self.assigned_harvesters, \
        self.ideal_harvesters, \
        self.weapon_cooldown, \
        self.order_len, \
        self.tag = np_array.tolist()

    @property
    def pos(self):
        return Point(self.posx, self.posy)

    def dist_to(self, other):
        return self.pos.dist(other.pos)

    def __repr__(self):
        return 'Unit type %d; tag %d' % (self.unit_type, self.tag)

    def __str__(self):
        return 'Unit type %d; tag %d' % (self.unit_type, self.tag)

    def __eq__(self, other): 
        if type(other) == int:
            return self.tag == other
        return self.tag == other.tag

    def __hash__(self):
        return hash(self.tag)