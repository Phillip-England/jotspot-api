import datetime

from fastapi import HTTPException

from lib import encrypt
from lib import Validator


async def create_user_controller(body, response, client):

    # setting up db
    db = client["jotspot"]
    coll = db["users"]

    # checking for duplacates
    result = coll.find_one({"username": body.username})
    if result != None:
        raise HTTPException(status_code=400, detail="user already exists")

    # building username validator
    username_validator = Validator(body.username) \
        .set_max_length(32, 'username must contain 32 characters or less') \
        .set_min_length(3, 'username must contain 3 or more characters') \
        .set_whitelist("-_", 'username can only contain letters, numbers, dashes, and underscores') \
        .set_required('username is required')
    username_validator.validate()

    # dealing with username validation results
    if username_validator.is_valid == False:
        first_error = username_validator.errors[0]
        raise HTTPException(status_code=400, detail=first_error)

    # building password validator
    password_validator = Validator(body.password) \
        .set_max_length(64, 'password must contain 64 characters or less') \
        .set_min_length(8, 'password must contain 8 or more characters') \
        .set_whitelist('!@#$%^&*()', 'password can only contain letters, numbers, and the following symbols: !@#$%^&*()') \
        .set_required('password is required')
    password_validator.validate()

    # dealing with password validation results
    if password_validator.is_valid == False:
        first_error = password_validator.errors[0]
        raise HTTPException(status_code=400, detail=first_error)

    # encrypting passwords
    encrypted_password = encrypt(body.password)

    # inserting user into db
    result = coll.insert_one({
        "username": body.username,
        "password": encrypted_password,
        "created_at": datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
    })

    return {"detail": "user created"}
