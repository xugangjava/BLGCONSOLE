from gevent import monkey

monkey.patch_all()
import bottle
from core.api import *
from core.console import *
from core.apis import *
from core.coin_console import *


def run_bottle():
	from beaker.middleware import SessionMiddleware
	session_opts = {
		'session.type': 'ext:database',
		'session.url': 'mysql+mysqldb://root:%s@localhost/poker?charset=utf8' % DB_PWD,
		'session.cookie_expires': 60000,
		'session.auto': True,
	}
	app = SessionMiddleware(bottle.app(), session_opts)
	bottle.debug(DEBUG)
	bottle.run(app=app, host='192.168.6.102', port=8000, reloader=DEBUG)


if __name__ == '__main__':
	run_bottle()
