from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
import schedule, schedule_loader, utils

class ScheduleScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self._schedule = None
        self._no_course_lbl = Label(text = 'You have no courses', italic = True, color = [1, 1, 1, 0.75])
        self._no_course_lbl.font_size = self._no_course_lbl.height * 0.2

    def init(self, schedule):
        """whenever a schedule is loaded this must be called so the screen can be updated"""
        self._schedule = schedule
        self.ids.schedule_name.text = self._schedule.name
        self.ids.current_gpa.text = f'Current GPA: {round(self._schedule.current_gpa, 2)}'
        self.ids.current_units.text = f'Completed Units: {self._schedule.current_units}'
        self.ids.projected_gpa.text = f'Projected GPA: {round(self._schedule.projected_gpa, 2)}'
        self.ids.projected_units.text = f'Enrolled Units: {self._schedule.projected_units}'
        self.check_view_no_sch_lbl()

    def check_view_no_sch_lbl(self) -> None:
        """turns on or off the no course message"""
        if len(self._schedule.courses) == 0:
            if (self._no_course_lbl not in self.ids.course_box.children):
                self.ids.course_box.height = self._no_course_lbl.height
                self.ids.course_box.add_widget(self._no_course_lbl)
        else:
            self.ids.course_box.remove_widget(self._no_course_lbl)

    def launch_add_course(self) -> None:
        """switches the screen to add course"""
        utils.switch_screen(self, 'course_screen', 'right')

    def launch_add_assignment(self) -> None:
        """switches the screen to add assignment"""
        utils.switch_screen(self, 'assignment_screen', 'right')

    def delete_schedule(self) -> None:
        """delete the schedule from the schedule list after confirming deletion"""
        def yes_func():
            try:
                schedule_loader.delete_schedule(self._schedule.name)
            except utils.ScheduleDeleteError as e:
                utils.default_popup(f'{e.message}\nTry reloading the schedule and then deleting it.')
            else:
                utils.SCREENS['home_screen'].remove_schedule(self._schedule.name)
                self._schedule = None
                utils.switch_screen(self, 'home_screen', 'right')

        utils.yesno_popup(f'Are you sure you want to delete "{self._schedule.name}"?', yes_func)

    def return_to_homescreen(self) -> None:
        """sets the screen to the homescreen"""
        self._schedule.save()
        utils.switch_screen(self, 'home_screen', 'right')
