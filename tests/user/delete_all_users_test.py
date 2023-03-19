from test_lib import TestUnit

def delete_all_users_test(session, print_results=False):
  test_unit = TestUnit(
    session=session, 
    method='delete', 
    path='/user/delete/all', 
    description="deleting all users",
    print_results=print_results
  )
  test_unit.build_test(
    purpose='testing if endpoint works', 
    status_code_expected=200
  )
  test_unit.run_tests()


    
