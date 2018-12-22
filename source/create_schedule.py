from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, NumericProperty
import utils

class CreateSchedule(Screen):

    def __init__(self, **kwargs):
        self._name = StringProperty('')
        self._gpa = NumericProperty(0)
        self._units = NumericProperty(0)
        super(Screen, self).__init__(**kwargs)

    def back(self) -> None:
        self.parent.transition = SlideTransition(direction = 'right', duration = utils.DEFAULT_TRANSITION_LENGTH)
        self.parent.current = 'home_screen'

    def create(self):
        pass
