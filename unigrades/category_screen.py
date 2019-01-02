from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import course, utils

class CategoryScreen(Screen):

    _name, _weight = StringProperty(), StringProperty()

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self._course = None

    def set_course(self, c: course.Course) -> None:
        self._course = c

    def clear_fields(self) -> None:
        """resets the text inputs"""
        self._name = ''
        self._weight = ''
        self._course = None

    def add_category(self) -> None:
        """adds the category to the course"""
        name = self._name.strip()
        if name.replace(' ', '') != '':                                 # if the name is blank space, show an error
            if name in [c.name for c in self._course.categories]:
                try:
                    weight_f = float(self._weight)                          # if the weight is not a number, show an error
                    if weight_f < 100:                                      # if the weight is over 100%, show an error
                        s = sum([c.weight for c in self._course.categories]) + weight_f
                        if s == 100:                                        # if all the weights added together is not equal to 100, show an error
                            self._course.add_category(course.Category(name, weight_f))
                            self.clear_fields()
                            utils.SCREENS['schedule_screen']._schedule.save()
                            utils.switch_screen(self, 'course_view_screen', 'right')
                        else:
                            utils.default_popup(f'The sum of all categories must total to 100%.  They currently total to {s}%.')
                    else:
                        utils.default_popup('Category weight must be 100 or less')
                except ValueError:
                    utils.default_popup('Category weight must be a number.')
            else:
                utils.default_popup(f'A category with name {name} already exists.')
        else:
            utils.default_popup('Category name cannot be left blank.')

    def return_to_course(self) -> None:
        """returns to the course screen"""
        def yes_func():
            self.clear_fields()
            utils.switch_screen(self, 'course_view_screen', 'right')

        if self._name == '' and self._weight == '':
            utils.switch_screen(self, 'course_view_screen', 'right')
        else:
            utils.yesno_popup('Are you sure you want to go back?  This category will not be added to the course.', yes_func)
