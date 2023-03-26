
from pydantic import BaseModel
from fastapi import Response
from fastapi import Request
from fastapi import Depends
from fastapi import HTTPException

from controllers import create_user_controller
from controllers import delete_all_users_controller
from controllers import login_user_controller
from controllers import logout_user_controller
from controllers import get_logged_in_user_controller
from middleware import auth_middleware


def user_routes(app, client):

    # CREATING A USER
    class CreateUserBody(BaseModel):
        username: str
        password: str

    @app.post("/user/create")
    async def create_user(body: CreateUserBody, response: Response):
        try:
            response = await create_user_controller(body, response, client)
            return response
        except Exception as error:
            response.status_code = error.status_code
            return error

    # DELETING ALL USERS
    @app.delete("/user/delete/all")
    async def delete_all_users(request: Request, Response: Response):
        try:
            response = await delete_all_users_controller(client)
            return response
        except Exception as error:
            response.status_code = error.status_code
            return error

    # LOGGING IN A USER
    class LoginUserBody(BaseModel):
        username: str
        password: str

    @app.post("/user/login")
    async def login_user(body: LoginUserBody, response: Response):
        try:
            response = await login_user_controller(client, body, response)
            return response
        except Exception as error:
            response.status_code = error.status_code
            return error

    # GET THE LOGGED IN USER
    @app.get("/user")
    async def get_logged_in_user(request: Request, response: Response):
        try:
            request = await auth_middleware(request, response, client)
            response = await get_logged_in_user_controller(request, request)
            return response
        except Exception as error:
            response.status_code = error.status_code
            return error

    # LOG OUT THE CURRENT USER
    @app.get("/user/logout")
    async def logout_user(request: Request, response: Response):
        try:
            request = await auth_middleware(request, response, client)
            response = await logout_user_controller(request, response, client)
            return response
        except Exception as error:
            response.status_code = error.status_code
            return error
