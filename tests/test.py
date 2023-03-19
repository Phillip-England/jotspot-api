import requests

from dotenv import load_dotenv

from user import user_tests

if __name__ == '__main__':
  load_dotenv()
  session = requests.Session()
  user_tests(session)