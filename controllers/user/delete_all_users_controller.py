
def delete_all_users_controller(client):
  db = client['jotspot']
  coll = db['users']
  coll.delete_many({})
  coll = db['sessions']
  coll.delete_many({})
  return {"message": "deleted all users"}