import timeit
import ezsheets
from datetime import datetime
import time
import smtplib, ssl
import PySimpleGUI as sg
from threading import Thread
from time import sleep
import os
from dotenv import load_dotenv
from os.path import exists


class TMS:
    def __init__(self):
        self.SHEET = ezsheets.Spreadsheet('1ndTuG1hOlNoAHHQJy9U1RQ1YbnRfscjaqLYDnlY-nUE')
        self.sh = self.SHEET.sheets[0]
        self.start = 0
        self.stop = 0
        self.start_date = ''
        self.end_date = ''
        self.time_now = datetime.now()
        self.sh.update(1, 1, 'Start time:')
        self.sh.update(2, 1, 'End time:')
        self.row_to_start = self.sh.rowCount + 1
        self.env_file()
        self.smtp_server = ""
        self.port = ""
        self.sender_email = ""
        self.receiver_email = ""
        self.password = ""
        self.kill_the_timer = True
        self.thread = None

    def env_file(self):
        ENV_FILE_EXISTS = exists('.env')
        if ENV_FILE_EXISTS:
            load_dotenv()
        else:
            with open(".env", "w") as f:
                smtp_server = input('Input SMTP server: ')
                port = input('Input port: ')
                sender_email = input('Input sender email: ')
                password = input('Input password: ')
                receiver_email = input('Input receiver email: ')
                f.write(f'smtp_server={smtp_server}\n')
                f.write(f'port={port}\n')
                f.write(f'sender_email={sender_email}\n')
                f.write(f'password={password}\n')
                f.write(f'receiver_email={receiver_email}\n')
            load_dotenv()

    def start_timer(self):
        print('Start initiated.')
        self.start = timeit.default_timer()
        self.start_date = self.time_now
        self.start_date = str(self.start_date).split('.')[0]
        return self.sh.update(1, self.row_to_start, self.start_date)

    def stop_timer(self):
        start_time = time.time()
        while not self.kill_the_timer:
            if time.time() - start_time >= 60:
                sleep(0.5)
                print('Another minute passed, updating the sheet...')
                self.timer_calc()
                start_time = time.time()
        else:
            self.stop = timeit.default_timer()
            print('Finishing work.')
            return self.stop

    def timer_calc(self):
        self.end_date = str(datetime.now()).split('.')[0]
        return self.sh.update(2, self.row_to_start, self.end_date)

    def summary(self):
        print(f'You worked from {self.start_date} to {self.end_date}')

    def send_mail(self):
        context = ssl.create_default_context()
        self.smtp_server = os.getenv('smtp_server')
        self.port = int(os.getenv('port'))
        self.sender_email = os.getenv('sender_email')
        self.password = os.getenv('password')
        self.receiver_email = os.getenv('receiver_email')
        message = f"""\
        Subject: TMS data
        Start: {self.start_date}
        End: {self.end_date}
        This message is sent from Python."""
        print(message)
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, message)
        print('Thanks, email sent!')

    def windowed_mode(self):
        sg.theme('SystemDefault')
        layout = [[sg.Text('This program will track your time, press Start to initiate.')],
                  [sg.Text('To stop in any moment please use Stop button.')],
                  [sg.Text('On exit, your working time will be sent to given email address.')],
                  [sg.Text('In case if you want to change SMTP/Email data, please delete .env file.')],
                  [sg.Button('Start'), sg.Button('Stop'), sg.Button('Exit')]]
        window = sg.Window('TMS ver. 1.0', layout, element_justification='c')
        self.thread = None
        while True:
            event, values = window.read()
            if event == 'Start' and self.thread is None:
                self.start_timer()
                self.kill_the_timer = False
                self.thread = Thread(target=self.stop_timer, daemon=True)
                self.thread.start()
            if event == 'Stop':
                self.kill_the_timer = True
                self.thread = None
                self.timer_calc()
                self.summary()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
        window.close()


timer = TMS()
timer.env_file()
timer.windowed_mode()
timer.send_mail()
