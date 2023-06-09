import datetime
import secrets

from fastapi.responses import JSONResponse
from fastapi import HTTPException

from lib import decrypt


async def login_user_controller(client, body, response):

    # setting up db
    db = client['jotspot']
    coll = db['users']

    # getting user by provided username
    user_doc = coll.find_one({"username": body.username})

    # checking if user even exists
    if user_doc == None:
        raise HTTPException(status_code=400, detail="invalid credentials")

    # checking if passwords match
    decrypted_password = decrypt(user_doc['password'])
    if body.password != decrypted_password:
        raise HTTPException(status_code=400, detail="invalid credentials")

    # deleting all sessions associated with user
    coll = db['sessions']
    deleted_session = coll.delete_one({"user": user_doc['_id']})

    # building a new user session
    session_token = secrets.token_hex(128)
    coll.insert_one({
        'user': user_doc['_id'],
        'token': session_token,
        'created_at': datetime.datetime.now(),
        'expires_at': datetime.datetime.now() + datetime.timedelta(minutes=30)
    })

    # setting session token in cookie and returning 200 response
    response = JSONResponse(content={"detail": "user logged in"})
    response.set_cookie(key='token', value=session_token, httponly=True)

    return response
