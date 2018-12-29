from kivy.uix.screenmanager import Screen, SlideTransition
import schedule, utils

class ScheduleScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self._schedule = None

    def init(self, schedule):
        pass

    def return_to_homescreen(self) -> None:
        """sets the screen to the homescreen"""
        utils.switch_screen(self, 'home_screen', 'right')
