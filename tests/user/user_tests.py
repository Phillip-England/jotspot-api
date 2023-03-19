
from .delete_all_users_test import delete_all_users_test
from .create_new_user_test import create_new_user_test
from .login_user_test import login_user_test
from .get_logged_in_user_test import get_logged_in_user_test
from .logout_user_test import logout_user_test

from test_lib import TestUnit

def user_tests(session):

  delete_all_users_test(session=session, print_results=False)
  create_new_user_test(session=session, print_results=True)
  # login_user_test(session=session, print_results=True)
  # get_logged_in_user_test(session=session, print_results=True)
  # logout_user_test(session=session, print_results=True)