"""
This file defines the database models
"""
from collections import defaultdict
from typing import NamedTuple

from pydal.objects import Row

from .common import db, Field
from pydal.validators import *

### Define your table below
#

db.define_table('types',
                Field('naam'),
                format='%(naam)s'
                )

db.define_table('tijdlijn',
                Field('type', 'reference types', requires=IS_NULL_OR(IS_IN_DB(db, 'types.id', '%(naam)s', zero='maak een keuze'))),
                Field('titel'),
                Field('datum', 'date', requires=IS_NULL_OR(IS_DATE())),
                Field('auteur'),
                Field('url')
                )

#
## always commit your models to avoid problems later
#
db.commit()

MONTHS = [
    "_",
    "jan",
    "feb",
    "maa",
    "apr",
    "mei",
    "jun",
    "jul",
    "aug",
    "sep",
    "okt",
    "nov",
    "dec"
]


class MonthInfo(NamedTuple):
    year: int
    month: int
    count: int
    items: list[Row]

    @property
    def description(self):
        """
        Create a representation in the form 'jan 2022' (Dutch month abbreviation with numeric year)
        """
        month = MONTHS[self.month]
        return f"{month} {self.year}"


def all_items_by_year_month() -> dict[tuple[int, int], list[Row]]:
    """
    Get tijdlijn items (with type converted from id to name), grouped by a tuple of year and month.

    :return: tuple (year, month): list of tijdlijn rows
    """
    year = db.tijdlijn.datum.year()
    month = db.tijdlijn.datum.month()
    items = defaultdict(list)

    query = db.tijdlijn.id > 0
    query &= db.tijdlijn.type == db.types.id
    rows = db(query).select(db.tijdlijn.ALL, db.types.naam, year, month)
    for row in rows:
        info = row.as_dict()['tijdlijn']
        info['type'] = row.types.naam
        items[(row[year], row[month])].append(info)

    return items


def months_that_have_items() -> list[MonthInfo]:
    """
    Find months that have items and return:
    - year
    - month
    - count in that month of that year
    - list of items in that month of that year

    in the form of a MonthInfo instance
    """
    query = db.tijdlijn

    year = db.tijdlijn.datum.year()
    month = db.tijdlijn.datum.month()
    count = db.tijdlijn.id.count()

    items = all_items_by_year_month()
    rows = db(query).select(year, month, count,
                            groupby=[year, month],
                            orderby=[year, month]
                            )

    return [MonthInfo(row[year], row[month], row[count], items[(row[year], row[month])]) for row in rows]
