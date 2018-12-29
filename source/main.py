from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

import home_screen
import create_schedule

Builder.load_string('''
#: include home_screen.kv
#: include create_schedule.kv
#: include schedule_screen.kv

<MainScreen>:

    HomeScreen:
    CreateSchedule:
    ScheduleScreen:
''')

class UniGrades(App):
    def build(self):
        return MainScreen()

class MainScreen(ScreenManager):
    home_screen = home_screen.HomeScreen()

if __name__ == '__main__':
    UniGrades().run()
