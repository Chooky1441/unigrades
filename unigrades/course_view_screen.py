from kivy.uix.screenmanager import Screen
import course, utils

class CourseViewScreen(Screen):

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self._course = None

    def init(self, c: course.Course) -> None:
        self._course = c
        self.ids.course_name.text = c.name
        self.ids.lbl_grade.text = f'Grade: {c.letter_grade()}'
        self.ids.lbl_units.text = f'Units: {c.units}'

    def return_to_schedulescreen(self) -> None:
        """switches back to the schedule screen"""
        # clear everything
        utils.SCREENS['schedule_screen']._schedule.save()
        utils.switch_screen(self, 'schedule_screen', 'right')

    def launch_category_screen(self) -> None:
        """opens up the add category screen"""
        utils.SCREENS['category_screen'].set_course(self._course)
        utils.switch_screen(self, 'category_screen', 'left')

    def launch_edit_course(self) -> None:
        """opens up the course editor"""
        utils.SCREENS['course_screen'].init(self._course)
        utils.switch_screen(self, 'course_screen', 'left')

    def delete_course(self) -> None:
        """deletes the course from the schedule, and returns to the schedule screen"""
        def yes_func():
            utils.SCREENS['schedule_screen'].remove_course(self._course)
            self.return_to_schedulescreen()

        utils.yesno_popup('Are you sure you want to delete this course', yes_func)
