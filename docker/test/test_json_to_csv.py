import pytest

import sys

sys.path.append("../src")

from competitors.flinders import FlindersCompetitor
from competitors.fonq import FonqCompetitor
from competitors.bolia import BoliaCompetitor


@pytest.mark.parametrize("example", [
    {
        "json_item": {"country": "nl", "competitor": "flinders", "category": "corner_sofa",
                      "category_url": "https://www.flinders.nl/wonen-stoelen-fauteuils",
                      "page_url": "https://www.flinders.nl/vitra-eames-lounge-chair-fauteuil-sneeuwwit",
                      "product_number": 0, "page_number": 2, "product_info": {"price": 253.3,
                                                                              "title": "Vitra Eames Lounge chair fauteuil (nieuwe afmetingen) sneeuwwit",
                                                                              "technical_details": {
                                                                                  "afmetingen": "(b) 84 x (d) 85 x (h) 89 cm",
                                                                                  "zithoogte": "38",
                                                                                  "ruimte": "Alleen geschikt voor binnen",
                                                                                  "materiaal": "Aluminium (metaal), Multiplex, Walnoot (hout)",
                                                                                  "garantie": "2 jaar", "merk": "Vitra",
                                                                                  "categorie": "Fauteuils",
                                                                                  "productsoort": "Vitra fauteuil",
                                                                                  "productfamilie": "Vitra Eames Lounge Chair",
                                                                                  "ontwerper": "Charles & Ray Eames",
                                                                                  "herkomst": "Zwitserland"}}},
        "expected_csv_item": {
            "country": "nl",
            "category": "corner_sofa",
            "competitor": "flinders",
            "price": 253.3,
            "title": "Vitra Eames Lounge chair fauteuil (nieuwe afmetingen) sneeuwwit",
            "width": 84.0,
            "height": 89.0,
            "depth": 85.0,
            "seat_height": 38.0,
            "material": "Aluminium (metaal), Multiplex, Walnoot (hout)",
            "color": ""
        },
        "competitor": FlindersCompetitor()
    },
    {
        "json_item": {"country": "nl", "competitor": "fonq", "category": "floor_lights",
                      "category_url": "https://www.fonq.nl/producten/categorie-vloerlampen/",
                      "page_url": "https://www.fonq.nl/product/bepurehome-theatre-vloerlamp/274282/",
                      "product_number": 0, "page_number": 10,
                      "product_info": {"price": 169.0, "title": "BePureHome Theatre Vloerlamp",
                                       "technical_details": {"fitting": "E27", "materiaal": "Metaal",
                                                             "hoogte": "170 cm", "breedte": "50 cm",
                                                             "lichtbron_meegeleverd": "Nee", "diepte": "43 cm",
                                                             "snoerlengte_in_meters": "1,3",
                                                             "productnummer": "246012", "ean_code": "8714713080731",
                                                             "aantal_lichtbronnen": "1", "bestelcode": "800842-M",
                                                             "garantie": "2 jaar", "kleur": "Messing",
                                                             "kleurtint": "Antiek messing", "lichtbron": "LED",
                                                             "productserie": "Theatre", "vermogen_(in_watt)": "40"}}},
        "expected_csv_item": {
            "country": "nl",
            "category": "floor_lights",
            "competitor": "fonq",
            "price": 169.0,
            "title": "BePureHome Theatre Vloerlamp",
            "width": 50.0,
            "height": 170.0,
            "depth": 43.0,
            "seat_height": 0.0,
            "material": "Metaal",
            "color": "Messing"
        },
        "competitor": FonqCompetitor()
    },
    {
        "json_item": {"country": "nl", "competitor": "bolia", "category": "2_seat_sofas",
                      "category_url": "https://www.bolia.com/nl-nl/banken/alle-banken/?Model=2-zitsbank&Model=2%C2%BD-zitsbank&size=10000",
                      "page_url": "https://www.bolia.com/nl-nl/producten/01-202-01_12397759", "product_number": 2,
                      "page_number": 10, "product_info": {"price": 2265.0, "title": "Scandinavia Remix 2-zitsbank",
                                                          "technical_details": {
                                                              "description": "Scandinavia Remix is een modern designicoon, ontworpen door Glismand & R\u00fcdiger. De constructie van de bank is gemaakt van massief, duurzaam hout en de dubbelbeklede kussens zorgen ervoor dat de bank jarenlang meegaat. Onder de slanke kussens bevindt zich een hoogwaardige voering en een hellende rand die de kussens op hun plaats houdt. De poten zijn verkrijgbaar in diverse materialen en twee hoogtes, en de kussens hebben zowel een donzen als schuimvulling. Je bepaalt zelf of je de Scandinavia Remix laat bekleden met zacht velours, klassiek leer, gerecycled katoen of een van onze talloze andere meubelstoffen. Het resultaat is een klassieke bank waarvan alle details doordacht en mooi uitgevoerd zijn.",
                                                              "diepte": "90 cm", "zitdiepte": "58 cm",
                                                              "breedte": "162 cm", "rughoogte": "80/83 cm",
                                                              "zithoogte": "42/45  cm", "stof": "Bergo - Stof",
                                                              "kleur": "Raw Amber", "zitcomfort": "Schuim-Schuim",
                                                              "poten": "20 cm witgeolied eiken\n",
                                                              "land van herkomst": "Handgemaakt in EU",
                                                              "vulling, rugkussen en zitkussen": "Koudschuim of koudschuim met dons",
                                                              "montage": "De poten moeten gemonteerd worden",
                                                              "opmerking": "De armleuning kan van deze bank worden verwijderd"}}},
        "expected_csv_item": {
            "country": "nl",
            "category": "2_seat_sofas",
            "competitor": "bolia",
            "price": 2265.0,
            "title": "Scandinavia Remix 2-zitsbank",
            "width": 162,
            "height": 170.0,
            "depth": 90.0,
            "seat_height": 0.0,
            "material": "",
            "color": "Raw Amber"
        },
        "competitor": FonqCompetitor()
    },
])
def test_conversion_json_to_csv(example):
    competitor = example["competitor"]
    csv_dict = competitor.convert_to_csv_item(example["json_item"])

    assert csv_dict["country"] == example["expected_csv_item"]["country"]
    assert csv_dict["category"] == example["expected_csv_item"]["category"]
    assert csv_dict["competitor"] == example["expected_csv_item"]["competitor"]
    assert csv_dict["price"] == example["expected_csv_item"]["price"]
    assert csv_dict["title"] == example["expected_csv_item"]["title"]
    assert csv_dict["width"] == example["expected_csv_item"]["width"]
    assert csv_dict["depth"] == example["expected_csv_item"]["depth"]
    assert csv_dict["height"] == example["expected_csv_item"]["height"]
    assert csv_dict["seat_height"] == example["expected_csv_item"]["seat_height"]
    assert csv_dict["material"] == example["expected_csv_item"]["material"]
    assert csv_dict["color"] == example["expected_csv_item"]["color"]
