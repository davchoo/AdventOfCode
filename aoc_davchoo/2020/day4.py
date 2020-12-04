import re


def process_data(data):
    passports = []
    current_passport = {}
    for line in data.splitlines():
        if line == "":
            passports.append(current_passport)
            current_passport = {}
            continue
        for key, value in (entry.split(":") for entry in line.split()):
            current_passport[key] = value
    passports.append(current_passport)
    return passports


def is_present(passport: dict, ignore_cid: bool):
    required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    if not ignore_cid:
        required_fields.append("cid")

    return all(field in passport.keys() for field in required_fields)


validation = {
    "byr": lambda x: len(x) == 4 and 1920 <= int(x) <= 2002,
    "iyr": lambda x: len(x) == 4 and 2010 <= int(x) <= 2020,
    "eyr": lambda x: len(x) == 4 and 2020 <= int(x) <= 2030,
    "hgt": lambda x: ("cm" in x and (150 <= int(x[:-2]) <= 193)) or ("in" in x and (59 <= int(x[:-2]) <= 76)),
    "hcl": lambda x: re.match(r"#[0-9a-f]{6}", x) is not None,
    "ecl": lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
    "pid": lambda x: int(x) and len(x) == 9
}


def is_valid(passport: dict):
    try:
        return all(validator(passport[field]) for field, validator in validation.items())
    except Exception:
        return False


def solve_a(data):
    passports = process_data(data)
    valid = [is_present(passport, True) for passport in passports]
    return valid.count(True)


def solve_b(data):
    passports = process_data(data)
    valid = [is_present(passport, True) and is_valid(passport) for passport in passports]
    return valid.count(True)
