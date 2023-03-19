def logout_user_controller(req, res, client):
  token = req.cookies.get("token")
  if token == None:
    res.status_code = 401
    return {'message': 'unauthorized'}
  db = client['jotspot']
  coll = db['sessions']
  coll.delete_one({"token": token})
  res.delete_cookie(key='token')
  return {'message': 'user logged out'}