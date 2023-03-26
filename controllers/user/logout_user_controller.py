from fastapi import HTTPException


async def logout_user_controller(request, response, client):

    # getting the token from http cookie
    token = request.cookies.get("token")
    if token == None:
        print('hit')
        raise HTTPException(status_code=401, detail="unauthorized")

    # setting up db
    db = client['jotspot']
    coll = db['sessions']

    # deleting the token and cookie
    coll.delete_one({"token": token})
    response.delete_cookie(key='token')

    # 200 response
    return {'detail': 'user logged out'}
