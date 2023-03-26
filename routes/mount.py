from .user_routes import user_routes
from .note_routes import note_routes

def mount(app, client):
  user_routes(app, client)
  note_routes(app, client)


