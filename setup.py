from setuptools import setup, find_packages

setup(
    name="aoc_davchoo",
    version="0.1",
    description="davchoo's solutions for Advent of Code",
    url="tbf",
    author="davchoo",
    author_email="davchoo3@gmail.com",
    install_requires=[
        "advent-of-code-data >= 0.8.0"
    ],
    packages=find_packages(),
    entry_points={
        "adventofcode.user": ["davchoo=aoc_davchoo:solve"],
    }
)