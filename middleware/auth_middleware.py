import datetime

from fastapi import Request
from fastapi import HTTPException
from fastapi import Response
from bson.objectid import ObjectId


async def auth_middleware(request: Request, response: Response, client):

    # checking for token
    token = request.cookies.get('token')
    if token == None:
        raise HTTPException(status_code=401, detail="unauthorized")

    # setting up db and pulling current user
    db = client['jotspot']
    coll = db['sessions']
    session = coll.find_one({'token': token})

    # if the session does not exist (for whatever reason), throw an error
    if session == None:
        raise HTTPException(status_code=401, detail='session does not exist')

    # checking if the current session is expired
    session_is_expired = True if session['expires_at'] < datetime.datetime.now(
    ) else False
    if session_is_expired:
        coll.delete_one({'_id': ObjectId(session['_id'])})
        raise HTTPException(status_code=401, detail="session expired")

    # getting the current user
    coll = db['users']
    user = coll.find_one({'_id': ObjectId(session['user'])})

    # if the current session has no user, unauth
    if user == None:
        response.status_code = 401
        raise HTTPException(status_code=401, detail="session expired")

    # tying the user to the request object
    request.state.user = user

    return request
