import datetime

from bson.objectid import ObjectId

def get_logged_in_user_controller(req, res, client):

  # getting the session token from the request
  token = req.cookies.get('token')

  # if we dont find a token, user is unauthorized
  if token == None:
    res.status_code = 401
    return {'message': 'unauthorized'}
  
  # setting up db and pulling the current session
  db = client['jotspot']
  coll = db['sessions']
  session = coll.find_one({'token': token})

  # checking if the current session is expired
  session_is_expired = True if session['expires_at'] < datetime.datetime.now() else False
  if session_is_expired:
    res.status_code = 401
    coll.delete_one({'_id': ObjectId(session['_id'])})
    return {'message': 'session expired'}

  # setting up db and pulling the current user
  coll = db['users']
  user = coll.find_one({'_id': ObjectId(session['user'])})

  # if we dont find a user associated with the session, unauth
  if user == None:
    res.status_code = 401
    return {'message': 'unauthorized'}
  
  # on success, send the current user to the client
  return {
    '_id': str(user['_id']),
    'username': user['username'],
  }