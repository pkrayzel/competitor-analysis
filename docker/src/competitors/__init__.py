import inject

from competitors.fonq import FonqCompetitor
from competitors.flinders import FlindersCompetitor
from competitors.bolia import BoliaCompetitor


class CompetitorNotFoundException(Exception):

    pass


@inject.params(competitors_map='competitors_map')
def find_competitor(country, name, competitors_map):
    key=f"{country}_{name}"

    result = competitors_map.get(key)

    if not result:
        raise CompetitorNotFoundException(f"Competitor not found for country: {country}, name: {name}")

    return result