from test_lib import TestUnit

def create_new_user_test(session, print_results=False):

  test_unit = TestUnit(
    session=session, 
    method='POST', 
    path='/user/create', 
    description="creating a new user",
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
    purpose='testing if duplicates are prevented', 
    status_code_expected=400,
    data={
      'username': 'phillip',
      'password': 'password'
    }
  )

  test_unit.build_test(
    purpose='testing for max length errors', 
    status_code_expected=400,
    data={
      'username': 'phillipasdasdasdasdasdasdasdasdasdasdasdas',
      'password': 'password'
    }
  )

  test_unit.build_test(
    purpose='testing for min length errors', 
    status_code_expected=400,
    data={
      'username': 'ph',
      'password': 'password'
    }
  )

  test_unit.build_test(
    purpose='testing whitelist', 
    status_code_expected=400,
    data={
      'username': 'phillip====',
      'password': 'password'
    }
  )

  test_unit.run_tests()



    
