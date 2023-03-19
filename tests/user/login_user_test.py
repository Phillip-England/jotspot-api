import json

from test_lib import TestUnit

def login_user_test(session, print_results=False):
  
  test_unit = TestUnit(
    session=session, 
    method='POST', 
    path='/user/login', 
    description="logging in a user",
    print_results=print_results
  )

  test_unit.build_test(
    purpose='testing if endpoint works', 
    status_code_expected=200,
    data={
      'username': 'phillip',
      'password': 'password'
    }
  )

  test_unit.build_test(
    purpose='testing if non-existent users cannot log in', 
    status_code_expected=400,
    data={
      'username': 'philli',
      'password': 'password'
    }
  )

  test_unit.build_test(
    purpose='testing if correct password is required', 
    status_code_expected=400,
    data={
      'username': 'phillip',
      'password': 'passwor'
    }
  )

  test_unit.run_tests()

    
