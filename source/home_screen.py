from kivy.uix.screenmanager import Screen, SlideTransition
import utils

class HomeScreen(Screen):

    def launch_create_schedule(self) -> None:
        self.parent.transition = SlideTransition(direction = 'left', duration = utils.DEFAULT_TRANSITION_LENGTH)
        self.parent.current = 'create_schedule'
