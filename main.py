import timeit
import keyboard
import ezsheets
from datetime import datetime
import time
import smtplib, ssl


class TMS:
    def __init__(self):
        self.SHEET = ezsheets.Spreadsheet('1ndTuG1hOlNoAHHQJy9U1RQ1YbnRfscjaqLYDnlY-nUE')
        self.sh = self.SHEET.sheets[0]
        self.start = 0
        self.stop = 0
        self.start_date = ''
        self.end_date = ''
        self.check_free_row()
        self.time_now = datetime.now()
        self.sh.update(1, 1, 'Start time:')
        self.sh.update(2, 1, 'End time:')
        self.row_to_start = 0
        self.port = 465
        self.smtp_server = ""
        self.sender_email = ""
        self.receiver_email = ""
        self.password = ''
        self.message = ''

    def check_free_row(self):
        self.row_to_start = self.sh.rowCount + 1
        return

    def start_timer(self):
        print(f'This program will track your time')
        print(f'Please press "S" on keyboard to end')
        self.start = timeit.default_timer()
        self.start_date = self.time_now
        self.start_date = str(self.start_date).split('.')[0]
        return self.sh.update(1, self.row_to_start, self.start_date)

    def stop_timer(self):
        start_time = time.time()
        while True:
            if time.time() - start_time >= 60:
                print('Another minute passed, updating the sheet...')
                self.timer_calc()
                start_time = time.time()
            if keyboard.is_pressed("s"):
                self.stop = timeit.default_timer()
                print(f'"S" detected, finishing work.')
                return self.stop

    def timer_calc(self):
        self.end_date = str(datetime.now()).split('.')[0]
        return self.sh.update(2, self.row_to_start, self.end_date)

    def send_mail(self):
        context = ssl.create_default_context()
        self.password = input("Type SMTP server password and press enter: ")
        self.sender_email = input("Please type sender email address and press enter: ")
        self.receiver_email = input("Please type email address where to send todays information: ")
        self.message = f"""\
        Subject: TMS data
        Start: {self.start_date}
        End: {self.end_date}
        This message is sent from Python."""
        print(self.message)
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, self.message)
        print('Thanks, email sent!')


timer = TMS()
timer.check_free_row()
timer.start_timer()
timer.stop_timer()
timer.timer_calc()
timer.send_mail()
