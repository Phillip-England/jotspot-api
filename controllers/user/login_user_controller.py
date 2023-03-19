import datetime
import secrets

from fastapi.responses import JSONResponse

from lib import decrypt

def login_user_controller(client, body, res):
  db = client['jotspot']
  coll = db['users']
  user_doc = coll.find_one({"username": body.username})
  decrypted_password = decrypt(user_doc['password'])
  if body.password != decrypted_password:
    res.status_code = 400
    return {"message": "invalid credentials"}
  coll = db['sessions']
  deleted_session = coll.delete_one({"user": user_doc['_id']})
  session_token = secrets.token_hex(128)
  coll.insert_one({
    'user': user_doc['_id'],
    'token': session_token,
    'created_at': datetime.datetime.now(),
    'expires_at': datetime.datetime.now() + datetime.timedelta(minutes=30)
  })
  response = JSONResponse(content={"message": "user logged in"})
  response.set_cookie(key='token', value=session_token, httponly=True)
  return response