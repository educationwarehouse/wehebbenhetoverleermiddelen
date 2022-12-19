"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""
import datetime

from py4web import action, request, abort, redirect, URL
from py4web.utils.form import FormStyleDefault
from py4web.utils.grid import Grid, GridClassStyle
from yatl.helpers import A

from .models import months_that_have_items
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash


@action("index")
@action.uses("index.html", auth, db)
def index():
    months_with_items = months_that_have_items()

    return dict(
        months=months_with_items
    )


@action("eddie", method=['POST', 'GET'])
@action('eddie/<path:path>', method=['POST', 'GET'])
@action.uses("eddie.html", auth.user, db)
def eddie(path=None):
    grid = Grid(path,
                formstyle=FormStyleDefault,
                grid_class_style=GridClassStyle,  # GridClassStyle or GridClassStyleBulma
                query=(db.tijdlijn.id > 0),
                orderby=[db.tijdlijn.datum],
                search_queries=[['Zoek op titel', lambda val: db.tijdlijn.titel.contains(val)]]
    )

    user = auth.get_user()
    return dict(grid=grid)


@action("dev_insert_timeline_items")
@action.uses(db)
def dev_insert_timeline_items():
    # remove me
    db.tijdlijn.truncate()

    n = 0
    for month in range(1, 12):
        for day in range(1, 10):
            date = datetime.datetime(year=2022, month=month, day=day)

            db.tijdlijn.insert(
                titel=f"Timeline item {date}",
                type=day % 4 + 1,
                datum=date,
                auteur="Robin van der Noord",
                url="https://trialandsuccess.nl",
            )
            n += 1

    return f"inserted {n}"
