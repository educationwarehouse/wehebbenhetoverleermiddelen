"""
This file defines the database models
"""

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
# db.commit()
#