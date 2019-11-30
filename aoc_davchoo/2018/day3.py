import re
import collections
import itertools


def process_data(data: str):
    claims = data.splitlines()
    regex = re.compile(r"(\d+)")
    claim_data = list(map(regex.findall, claims))
    return claim_data


def create_claim_map(claims):
    claim_map = collections.defaultdict(int)

    for claim_data in claims:
        claim_id, x, y, w, h = map(int, claim_data)
        for fabric_x in range(x, x + w):
            for fabric_y in range(y, y + h):
                claim_map[fabric_x, fabric_y] += 1
    return claim_map


def solve_a(data):
    claims = process_data(data)
    claim_map = create_claim_map(claims)

    total_shared_fabric = [num_claimed > 1 for num_claimed in claim_map.values()].count(True)

    return total_shared_fabric


def solve_b(data):
    claims = process_data(data)
    claim_map = create_claim_map(claims)
    for claim_data in claims:
        claim_id, x, y, w, h = map(int, claim_data)
        # Loop over all positions on claim
        for pos in itertools.product(range(x, x+w), range(y, y+h)):
            if claim_map[pos] > 1:
                break
        else:
            return claim_id
    return "Failed"
