from competitors.fonq import FonqCompetitor
from competitors.flinders import FlindersCompetitor
from competitors.bolia import BoliaCompetitor

COMPETITORS = [
    # FlindersCompetitor(),
    # FonqCompetitor(),
    BoliaCompetitor()
]


def find_competitor(name, country):
    for c in COMPETITORS:
        if c.name == name and c.country == country:
            return c
