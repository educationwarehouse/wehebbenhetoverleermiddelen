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

from py4web import action, request, abort, redirect, URL
from py4web.utils.form import FormStyleDefault
from py4web.utils.grid import Grid, GridClassStyle
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash




@action("index")
@action.uses("index.html", auth, T)
def index():

    return dict(tijdlijn=db(db.tijdlijn).select())


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
