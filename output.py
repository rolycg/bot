import smtplib

Server = 'smtp.gmail.com'
username = 'towpebsmtp2@gmail.com'
password = 'Gerr@rd4'
PORT = 465


SUCCESS = 'Succeed'
FAIL = 'Fail'


def print_section(msg):
    print('##### ' + msg + ' #####')


def print_task(msg):
    print('--- ' + msg + ' ---')


def print_result(msg):
    print('*** ' + msg + ' ***')


def print_error(msg):
    print('!!! ' + msg + ' !!!')


def send_email(msg, address='rolycg89@gmail.com'):
    message = """\
    From: %s
    To: %s
    Subject: %s
    %s
    """ % (username, ", ".join(address), 'Website testing results', msg)

    server = smtplib.SMTP_SSL('smtp.gmail.com:465')
    server.login(username, password)
    server.sendmail(username, address, message)
    server.quit()
