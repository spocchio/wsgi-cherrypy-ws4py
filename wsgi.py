import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import EchoWebSocket
import atexit

# the following 4 lines are suggested in the cherrypy website:      
# http://tools.cherrypy.org/wiki/ModWSGI
cherrypy.config.update({'environment': 'embedded'}) 
if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
	cherrypy.engine.start(blocking=False)
	atexit.register(cherrypy.engine.stop)

# initialize the websocket plugin of ws4py
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()  

# my application
class Root(object):
	def index(self):
		return 'I work!'
	def ws(self):
		print('THIS IS NEVER PRINTED :(')
	index.exposed=True
	ws.exposed=True
# registering the websocket
conf={'/ws':{'tools.websocket.on': True,'tools.websocket.handler_cls': EchoWebSocket}}


import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
logger.addHandler(stream)


# lets go!
application = cherrypy.Application(Root(), script_name='', config=conf)