from competitors.fonq import FonqCompetitor
from competitors.flinders import FlindersCompetitor

COMPETITORS = [
    FlindersCompetitor(),
    FonqCompetitor()
]


def find_competitor(name, country):
    for c in COMPETITORS:
        if c.name == name and c.country == country:
            return c
