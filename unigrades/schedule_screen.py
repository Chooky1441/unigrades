from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
import course, schedule, schedule_loader, utils

class ScheduleScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self._schedule = None
        self._no_course_lbl = Label(text = 'You have no courses', italic = True, color = [1, 1, 1, 0.75])
        self._no_course_lbl.font_size = self._no_course_lbl.height * 0.2
        self._course_buttons = dict()

    def init(self, schedule):
        """whenever a schedule is loaded this must be called so the screen can be updated"""
        if self._course_buttons != dict():
            for c in self._schedule.courses:
                self.remove_course_button(c, False)
        self._schedule = schedule
        self.ids.schedule_name.text = self._schedule.name
        self.ids.current_gpa.text = f'Current GPA: {round(self._schedule.current_gpa, 2)}'
        self.ids.current_units.text = f'Completed Units: {self._schedule.current_units}'
        self.ids.projected_gpa.text = f'Projected GPA: {round(self._schedule.projected_gpa, 2)}'
        self.ids.projected_units.text = f'Enrolled Units: {self._schedule.projected_units}'
        self.check_view_no_sch_lbl()
        for c in self._schedule.courses:
            self.add_course_button(c)

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

    def add_course_button(self, c: course.Course) -> None:
        """adds a course button to the screen"""
        self.update_view_height()
        self.check_view_no_sch_lbl()
        button = Button(text = c.name)
        button.font_size = button.height * 0.2

        def load_course(c: course.Course):
            utils.switch_screen(self, 'course_view_screen', 'left')
            utils.SCREENS['course_view_screen'].init(c)

        button.on_release = lambda: load_course(c)
        self.ids.course_box.add_widget(button)
        self._course_buttons[c.name] = button

    def update_gpa(self) -> None:
        self._schedule.projected_gpa = self._schedule._calc_projected_gpa()
        self.ids.projected_gpa.text = f'Projected GPA: {round(self._schedule.projected_gpa, 2)}'

    def add_course(self, c: course.Course) -> None:
        """adds a course to the schedule and updates the relevant info on the screen"""
        self._schedule.add_course(c)
        self.add_course_button(c)
        self.ids.projected_units.text = f'Enrolled Units: {self._schedule.projected_units}'
        self._schedule.save()

    def remove_course_button(self, c: course.Course, do_checks = True) -> None:
        """removes a course form the screen"""
        self.ids.course_box.remove_widget(self._course_buttons[c.name])
        if do_checks:
            del self._course_buttons[c.name]
            self.update_view_height()
            self.check_view_no_sch_lbl()

    def remove_course(self, c: course.Course) -> None:
        """removes the course from the schedule and updates the relevant info on the screen"""
        self._schedule.remove_course(c)
        self.update_view_height()
        self.remove_course_button(c)
        self.ids.projected_gpa.text = f'Projected GPA: {round(self._schedule.projected_gpa, 2)}'
        self.ids.projected_units.text = f'Enrolled Units: {self._schedule.projected_units}'

    def launch_edit_schedule(self) -> None:
        """opens up the schedule editor with all of the info in the schedule already displayed"""
        utils.SCREENS['create_screen'].init(self._schedule)
        utils.switch_screen(self, 'create_schedule', 'left')

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

    def update_view_height(self) -> None:
        self.ids.course_box.height = len(self._schedule.courses) * utils.DEFAULT_WIDGET_HEIGHT

    def return_to_homescreen(self) -> None:
        """sets the screen to the homescreen"""
        self._schedule.save()
        utils.switch_screen(self, 'home_screen', 'right')
