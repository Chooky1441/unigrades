from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import course, utils

class CategoryScreen(Screen):

    _name = StringProperty()

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self._course = None

    def set_course(self, c: course.Course) -> None:
        self._course = c

    def clear_fields(self) -> None:
        """resets the text inputs"""
        self._name = ''
        self._course = None

    def add_category(self) -> None:
        """adds the category to the course"""
        name = self._name.strip()
        if name.replace(' ', '') != '':                                 # if the name is blank space, show an error
            if name not in [c.name for c in self._course.categories]:
                self._course.add_category(course.Category(name, 0))
                utils.SCREENS['schedule_screen']._schedule.save()
                utils.SCREENS['course_view_screen'].init(self._course)
                self.clear_fields()
                utils.switch_screen(self, 'course_view_screen', 'right')
            else:
                utils.default_popup(f'A category with name {name} already exists.')
        else:
            utils.default_popup('Category name cannot be left blank.')

    def return_to_course(self) -> None:
        """returns to the course screen"""
        def yes_func():
            self.clear_fields()
            utils.switch_screen(self, 'course_view_screen', 'right')

        if self._name == '':
            utils.switch_screen(self, 'course_view_screen', 'right')
        else:
            utils.yesno_popup('Are you sure you want to go back?  This category will not be added to the course.', yes_func)
