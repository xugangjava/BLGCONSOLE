import bottle
from core.api import *
from core.console import *
from core.apis import *

def run_bottle():
    from beaker.middleware import SessionMiddleware
    session_opts = {
        'session.type': 'file',
        'session.cookie_expires': 3600,
        'session.data_dir': './data',
        'session.auto': True
    }
    app = SessionMiddleware(bottle.app(), session_opts)
    bottle.debug(DEBUG)
    bottle.run(app=app, host='192.168.3.11', port=8000, reloader=DEBUG)


if __name__ == '__main__':
    run_bottle()
