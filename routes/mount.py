from .user_routes import user_routes

def mount(app, client):
  user_routes(app, client)


