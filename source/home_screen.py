from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.button import Button
from kivy.clock import Clock
import schedule_loader, schedule_screen, utils

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self._sch_names = schedule_loader.get_all_schedule_names()

        def init_names(*args):
            for name in self._sch_names:
                self._add_sch_button(name)

        Clock.schedule_once(init_names)

    def _add_sch_button(self, name: str) -> None:
        """adds one schedule button to the homescreen"""
        self.ids['sch_box'].height = len(self._sch_names) * 50
        button = Button(text = name)
        button.font_size = button.height * 0.2
        button.on_release = lambda: utils.switch_screen(self, 'schedule_screen', 'left')
        self.ids['sch_box'].add_widget(button)

    def launch_create_schedule(self) -> None:
        """switches over to the create schedule screen"""
        utils.switch_screen(self, 'create_schedule', 'left')
