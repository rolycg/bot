import sys

from output import print_section
from actions.login import Login

# Main URL
HOST = 'https://www.jazwings.com/'

if __name__ == '__main__':
    if len(sys.argv):
        HOST = sys.argv[0]

    print_section('Login')

    login = Login(HOST)
    login.start()
