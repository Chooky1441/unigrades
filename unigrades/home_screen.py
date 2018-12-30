from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.label import Label
import schedule_loader, schedule_screen, utils

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.sch_names = schedule_loader.get_all_schedule_names()
        self._no_sch_lbl = Label(text = 'You have no schedules', italic = True, color = [1, 1, 1, 0.75])
        self._no_sch_lbl.font_size = self._no_sch_lbl.height * 0.2

        def init_names(*args):
            if len(self.sch_names) == 0:
                self.view_no_sch_lbl(True)
            else:
                for name in self.sch_names:
                    self.add_sch_button(name)

        Clock.schedule_once(init_names)

    def view_no_sch_lbl(self, view: bool) -> None:
        """turns on or off the no schedule message"""
        if view:
            self.ids.sch_box.height = self._no_sch_lbl.height
            self.ids.sch_box.add_widget(self._no_sch_lbl)
        else:
            self.ids.sch_box.remove_widget(self._no_sch_lbl)

    def add_sch_button(self, name: str) -> None:
        """adds one schedule button to the homescreen"""
        if name not in self.sch_names:
            self.sch_names = sorted(self.sch_names + [name], key = lambda x: x.lower())
        self.ids.sch_box.height = len(self.sch_names) * 50
        button = Button(text = name)
        button.font_size = button.height * 0.2

        def load_screen(*args):
            utils.switch_screen(self, 'schedule_screen', 'left')
            utils.SCREENS['schedule_screen'].init(schedule_loader.load_schedule(name))

        button.on_release = load_screen
        self.ids['sch_box'].add_widget(button)

    def launch_create_schedule(self) -> None:
        """switches over to the create schedule screen"""
        utils.switch_screen(self, 'create_schedule', 'left')
