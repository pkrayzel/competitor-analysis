#!/bin/ash
scrapy crawl -o "s3://made-competitor-analysis/%(name)s/%(category)s/%(time)s" -t json -a category=2_seat_sofas -a category_url=https://www.fonq.nl/producten/categorie-2_zitsbank/ fonq