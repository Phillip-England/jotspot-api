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
    purpose='testing username for max length errors', 
    status_code_expected=400,
    data={
      'username': 'phillipasdasdasdasdasdasdasdasdasdasdasdas',
      'password': 'password'
    }
  )

  test_unit.build_test(
    purpose='testing username for min length errors', 
    status_code_expected=400,
    data={
      'username': 'ph',
      'password': 'password'
    }
  )

  test_unit.build_test(
    purpose='testing username whitelist', 
    status_code_expected=400,
    data={
      'username': 'phillip====',
      'password': 'password'
    }
  )

  test_unit.build_test(
    purpose='testing password max length', 
    status_code_expected=400,
    data={
      'username': 'jon',
      'password': 'passwordasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasda'
    }
  )

  test_unit.build_test(
    purpose='testing password min length', 
    status_code_expected=400,
    data={
      'username': 'jon',
      'password': 'p'
    }
  )

  test_unit.build_test(
    purpose='testing password whitelist', 
    status_code_expected=400,
    data={
      'username': 'jon',
      'password': 'passwo;;;'
    }
  )

  test_unit.run_tests()



    
