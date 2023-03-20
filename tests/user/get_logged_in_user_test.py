import os
import datetime

import pymongo
from test_lib import TestUnit


def get_logged_in_user_test(session, print_results=True):

  test_unit = TestUnit(
    session=session, 
    method='GET', 
    path='/user', 
    description="getting the current user",
    print_results=print_results
  )

  test_unit.build_test(
    purpose='testing if endpoint works', 
    status_code_expected=200,
  )

  test_unit.build_test(
    purpose='testing if logged in user is required', 
    status_code_expected=401,
    empty_session=True
  )

  def make_current_session_expire():
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client['jotspot']
    coll = db['sessions']
    doc_filter = {"token": session.cookies['token']}
    update = {"$set": {'expires_at': datetime.datetime.now() - datetime.timedelta(days=1)}}
    coll.update_one(doc_filter, update)
    session_doc = coll.find_one(doc_filter)
    return True if session_doc['expires_at'] < datetime.datetime.now() else False
  
  def attempt_to_get_deleted_session():
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client['jotspot']
    coll = db['sessions']
    doc_filter = {"token": session.cookies['token']}
    session_doc = coll.find_one(doc_filter)
    return True if session_doc == None else False
  

  test_unit.build_test(
    purpose='testing with an expired session', 
    status_code_expected=401,
    pre_execution_callback=test_unit.inject_function(make_current_session_expire, True, "to make current session expire"),
    post_execution_callback=test_unit.inject_function(attempt_to_get_deleted_session, True, 'to check if current session has been deleted')
  )

  test_unit.run_tests()





    
