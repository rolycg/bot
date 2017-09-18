import sys

from output import print_section
from actions.login import Login
from actions.signup import Signup

# Main URL
HOST = 'https://jazwings.com/'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        HOST = sys.argv[1]

    print_section('Login')

    login = Login(HOST)
    login.start()
    print()

    print_section('Sign Up')
    signup = Signup(HOST)
    signup.start()
    print()
