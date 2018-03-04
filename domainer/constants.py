import six

if six.PY34:  # pragma: 2.7 no cover
    from connexion.apps.aiohttp_app import AioHttpApp as App
else:  # pragma: 3 no cover
    from connexion.apps.flask_app import FlaskApp as App

APP_CLS = App
