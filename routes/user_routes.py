
from pydantic import BaseModel
from fastapi import Response
from fastapi import Request

from controllers import create_user_controller
from controllers import delete_all_users_controller
from controllers import login_user_controller
from controllers import logout_user_controller
from controllers import get_logged_in_user_controller

def user_routes(app, client):

  # CREATING A USER
  class CreateUserBody(BaseModel):
    username: str
    password: str
  @app.post("/user/create")
  def create_user(body: CreateUserBody, res: Response):
    response = create_user_controller(body, res, client)
    return response
  
  # DELETING ALL USERS
  @app.delete("/user/delete/all")
  def delete_all_users():
    response = delete_all_users_controller(client)
    return response

  # LOGGING IN A USER
  class LoginUserBody(BaseModel):
    username: str
    password: str
  @app.post("/user/login")
  def login_user(body: LoginUserBody, res: Response):
    response = login_user_controller(client, body, res)
    return response

  # GET THE LOGGED IN USER
  @app.get("/user")
  def get_logged_in_user(req: Request, res: Response):
    response = get_logged_in_user_controller(req, res, client)
    return response

    
  # LOG OUT THE CURRENT USER
  @app.get("/user/logout")
  def logout_user(req: Request, res: Response):
    response = logout_user_controller(req, res, client)
    return response

      


