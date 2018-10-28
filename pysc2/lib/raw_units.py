def get_unit_type(np_array):
    return np_array[0]

# Self = 1, Ally = 2, Neutral = 3, Enemy = 4
def get_unit_alliance(np_array):
    return np_array[1]

# 1-15, 16 = neutral
def get_unit_owner(np_array):
    return np_array[11]

# Returns (x, y)
def get_unit_pos(np_array):
    return np_array[12], np_array[13]

def get_unit_tag(np_array):
    return np_array[27]
