from more_itertools import collapse


class SpaceObject:
    def __init__(self, name):
        self.name = name
        self.orbits = None  # The object that this orbits
        self.in_orbit = []  # The objects in direct orbit of this object
        self.num_indirect_orbits = 0


def recursive_iter_up(obj: SpaceObject):
    yield obj
    for obj in obj.in_orbit:
        yield from recursive_iter_up(obj)


def recursive_iter_down(obj: SpaceObject):
    yield obj
    if obj.orbits is not None:
        yield from recursive_iter_down(obj.orbits)


def process_data(data):
    orbits = [orbit.split(")") for orbit in data.splitlines()]
    object_names = set(collapse(orbits))
    objects = {name: SpaceObject(name) for name in object_names}
    for obj, obj_in_orbit in orbits:
        obj = objects[obj]
        obj_in_orbit = objects[obj_in_orbit]

        obj_in_orbit.orbits = obj
        obj.in_orbit.append(obj_in_orbit)

    COM = objects["COM"]
    COM.num_indirect_orbits = -1
    for obj in recursive_iter_up(COM):
        if obj.orbits is not None:
            obj.num_indirect_orbits = obj.orbits.num_indirect_orbits + 1
    COM.num_indirect_orbits = 0
    return objects


def solve_a(data):
    objects = process_data(data)
    total_orbits = len(objects) - 1 + sum(obj.num_indirect_orbits for obj in objects.values())
    return total_orbits


def solve_b(data):
    objects = process_data(data)
    you_object = objects["YOU"]
    santa_object = objects["SAN"]
    you_orbits = set(recursive_iter_down(you_object))
    santa_orbits = set(recursive_iter_down(santa_object))
    common_orbits = you_orbits.intersection(santa_orbits)
    first_common = max(common_orbits, key=lambda obj: obj.num_indirect_orbits)
    orbital_transfers = you_object.num_indirect_orbits + santa_object.num_indirect_orbits - 2 * (first_common.num_indirect_orbits + 1)
    return orbital_transfers
