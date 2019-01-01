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
        self.sch_buttons = dict()
        self._no_sch_lbl = Label(text = 'You have no schedules', italic = True, color = [1, 1, 1, 0.75])
        self._no_sch_lbl.font_size = self._no_sch_lbl.height * 0.2

        def init_names(*args):
            self.check_view_no_sch_lbl()
            for name in self.sch_names:
                self.add_sch_button(name)

        Clock.schedule_once(init_names)

    def check_view_no_sch_lbl(self) -> None:
        """turns on or off the no schedule message"""
        if len(self.sch_names) == 0:
            if (self._no_sch_lbl not in self.ids.sch_box.children):
                self.ids.sch_box.height = self._no_sch_lbl.height
                self.ids.sch_box.add_widget(self._no_sch_lbl)
        else:
            self.ids.sch_box.remove_widget(self._no_sch_lbl)

    def add_sch_button(self, name: str) -> None:
        """adds one schedule button to the homescreen"""
        if name not in self.sch_names:                          # if it is a new schedule, add it to the names and sort it
            self.sch_names = sorted(self.sch_names + [name], key = lambda x: x.lower())
        self.ids.sch_box.height = len(self.sch_names) * utils.DEFAULT_WIDGET_HEIGHT

        button = Button(text = name)
        button.font_size = button.height * 0.2

        def load_screen(*args):                                 # function that is custom to each button schedule
            utils.switch_screen(self, 'schedule_screen', 'left')
            utils.SCREENS['schedule_screen'].init(schedule_loader.load_schedule(name))

        button.on_release = load_screen
        self.ids.sch_box.add_widget(button)
        self.sch_buttons.update({name: button})

    def remove_schedule(self, name: str) -> None:
        """removes the schedule from the Schedule list"""
        self.ids.sch_box.remove_widget(self.sch_buttons[name])  # remove it from the screen
        del self.sch_buttons[name]                              # remove it from the dict
        self.sch_names.remove(name)
        self.check_view_no_sch_lbl()

    def launch_create_schedule(self) -> None:
        """switches over to the create schedule screen"""
        utils.switch_screen(self, 'create_schedule', 'left')
