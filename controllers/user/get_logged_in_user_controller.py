from bson.objectid import ObjectId

def get_logged_in_user_controller(req, res, client):
  token = req.cookies.get('token')
  if token == None:
    res.status_code = 401
    return {'message': 'unauthorized'}
  db = client['jotspot']
  coll = db['sessions']
  session = coll.find_one({'token': token})
  coll = db['users']
  user = coll.find_one({'_id': ObjectId(session['user'])})
  if user == None:
    res.status_code = 401
    return {'message': 'unauthorized'}
  return {
    '_id': str(user['_id']),
    'username': user['username'],
  }