
async def delete_all_users_controller(client):

    # setting up db
    db = client['jotspot']

    # deleting all users
    coll = db['users']
    coll.delete_many({})

    # deleting all sessions
    coll = db['sessions']
    coll.delete_many({})

    # json response
    return {"detail": "deleted all users"}
