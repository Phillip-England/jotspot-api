

async def create_note_controller(body, response, client):

    # setting up db
    db = client["jotspot"]
    coll = db["users"]

    print('hit')
    return {'message': 'success'}
