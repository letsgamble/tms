import timeit
import keyboard
import ezsheets


class TMS:
    def __init__(self):
        self.SHEET = ezsheets.Spreadsheet('1ndTuG1hOlNoAHHQJy9U1RQ1YbnRfscjaqLYDnlY-nUE')
        self.sh = self.SHEET.sheets[0]
        self.calculator = 0
        self.start = 0
        self.stop = 0

    def check_free_row(self):
        ...

    def start_timer(self):
        print(f'This program will track your time')
        print(f'Please press "S" on keyboard to end')
        self.start = timeit.default_timer()
        return self.start

    def stop_timer(self):
        while True:
            if keyboard.is_pressed("s"):
                self.stop = timeit.default_timer()
                return self.stop

    def timer_calc(self):
        self.start_timer()
        self.stop_timer()
        self.calculator = self.stop - self.start
        print(self.calculator)
        return self.sh.update(1, 1, self.calculator)


timer = TMS()
# print(str(timer.timer_calc())[0:1])
timer.timer_calc()
# timer.sh.update(1, 1, )
