## routing.py
#from channels.routing import route

#channel_routing = [
#    route('websocket.receive', 'app.consumers.ws_echo'),
#    route('websocket.connect', 'app.consumers.ws_add'),
#]

from channels import route
from app.consumers import connect_blog, disconnect_blog


channel_routing = [
    # Called when incoming WebSockets connect
    route("websocket.connect", connect_blog, path=r'^/Tesis/Publicacion/(?P<slug>[-\w]+)/stream/$'),

    # Called when the client closes the socket
    route("websocket.disconnect", disconnect_blog, path=r'^/Tesis/Publicacion/(?P<slug>[-\w]+)/stream/$'),

    # A default "http.request" route is always inserted by Django at the end of the routing list
    # that routes all unmatched HTTP requests to the Django view system. If you want lower-level
    # HTTP handling - e.g. long-polling - you can do it here and route by path, and let the rest
    # fall through to normal views.
]
