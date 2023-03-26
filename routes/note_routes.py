from pydantic import BaseModel
from fastapi import Response
from fastapi import Request

from controllers import create_note_controller
from middleware import auth_middleware


def note_routes(app, client):

    # CREATING A NOTE
    class CreateNoteBody(BaseModel):
        name: str
        content: str

    @app.post("/note/create")
    async def create_note(request: Request, body: CreateNoteBody, response: Response):
        try:
            request = await auth_middleware(request, response, client)
            response = await create_note_controller(body, response, client)
            return response
        except Exception as error:
            response.status_code = error.status_code
            return error
