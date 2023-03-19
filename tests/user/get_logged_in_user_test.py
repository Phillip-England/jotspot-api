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

  test_unit.run_tests()


    
