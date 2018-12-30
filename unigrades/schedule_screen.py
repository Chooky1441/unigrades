from kivy.uix.screenmanager import Screen, SlideTransition
import schedule, utils

class ScheduleScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self._schedule = None

    def init(self, schedule):
        """whenever a schedule is loaded this must be called so the screen can be updated"""
        self._schedule = schedule
        self.ids.schedule_name.text = self._schedule.name
        self.ids.current_gpa.text = f'Current GPA: {round(self._schedule.current_gpa, 2)}'
        self.ids.current_units.text = f'Completed Units: {self._schedule.current_units}'
        self.ids.projected_gpa.text = f'Projected GPA: {round(self._schedule.projected_gpa, 2)}'
        self.ids.projected_units.text = f'Enrolled Units: {self._schedule.projected_units}'

    def return_to_homescreen(self) -> None:
        """sets the screen to the homescreen"""
        self._schedule.save()
        print(self._schedule.to_dict())
        utils.switch_screen(self, 'home_screen', 'right')

    def remove_schedule(self) -> None:
        """removes the schedule from the schedule list after confirming deletion"""
        def yes_func():
            pass
        utils.yesno_popup
