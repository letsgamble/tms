import timeit
import keyboard
import ezsheets
from datetime import timedelta, datetime
import time


class TMS:
    def __init__(self):
        self.SHEET = ezsheets.Spreadsheet('1ndTuG1hOlNoAHHQJy9U1RQ1YbnRfscjaqLYDnlY-nUE')
        self.sh = self.SHEET.sheets[0]
        self.calculator = 0
        self.start = 0
        self.stop = 0
        self.start_date = 0
        self.check_free_row()
        self.time_now = datetime.now()
        self.sh.update(1, 1, 'Start time:')
        self.sh.update(2, 1, 'End time:')
        self.row_to_start = 0
        self.minute_counter = 0

    def check_free_row(self):
        self.row_to_start = self.sh.rowCount + 1
        return

    def start_timer(self):
        print(f'This program will track your time')
        print(f'Please press "S" on keyboard to end')
        self.start = timeit.default_timer()
        self.start_date = self.time_now
        return self.sh.update(1, self.row_to_start, str(self.start_date)[0:18])

    def stop_timer(self):
        start_time = time.time()
        while True:
            if time.time() - start_time >= 60:
                print('Another minute passed, updating the sheet...')
                self.minute_counter += 1
                self.timer_calc()
                start_time = time.time()
            if keyboard.is_pressed("s"):
                self.stop = timeit.default_timer()
                print(f'"S" detected, finishing work.')
                return self.stop

    def timer_calc(self):
        return self.sh.update(2, self.row_to_start, str(datetime.now() + timedelta(minutes=self.minute_counter))[0:18])


timer = TMS()
timer.check_free_row()
timer.start_timer()
timer.stop_timer()
timer.timer_calc()
