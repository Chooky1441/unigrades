from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.clock import Clock
import course, utils

class AssignmentScreen(Screen):
    _name, _pts_rec, _pts_total = StringProperty(), StringProperty(), StringProperty()
    _category = None # need to be dropdown menus
    _course, _assignment = None, None

    def init_new(self, c: course.Course) -> None:
        self.set_course(c)
        self.ids.cat_spinner.values = tuple(c.name for c in self._course.categories)

    def clear_fields(self) -> None:
        """resets all of the input fields"""
        self._name = ''
        self._pts_rec = ''
        self._pts_total = ''
        self.ids.checkbox_graded.active = True
        self.ids.cat_spinner.text = 'Choose a category'
        
        self._course = None
        self._assignment = None

    def set_course(self, c: course.Course) -> None:
        self._course = c

    def add_assignment(self) -> None:
        """adds the assignment to the course"""
        name = self._name.strip()
        if name.replace(' ', '') != '':                     # if the name is empty space, show an error
            if self._assignment is None or name not in [a.name for a in self._course.assignments]:
                pts_rec_f = None
                if self.ids.checkbox_graded.active:
                    try:
                        pts_rec_f = float(self._pts_rec)
                    except ValueError:
                        utils.default_popup('Points recieved must be a number.')
                        return
                try:
                    pts_total_f = float(self._pts_total)
                except ValueError:
                    utils.default_popup('Points total must be a number.')
                else:
                    if self.ids.cat_spinner.text in self.ids.cat_spinner.values: # if the category has not been chosen, show an error
                        self._course.add_assignment(self._course.get_category(self.ids.cat_spinner.text), course.Assignment(name, pts_rec_f, pts_total_f))
                        utils.SCREENS['course_view_screen'].init(self._course)
                        utils.SCREENS['schedule_screen'].update_gpa()
                        utils.SCREENS['schedule_screen']._schedule.save()
                        utils.switch_screen(self, 'course_view_screen', 'right')
                        self.clear_fields()
                    else:
                        utils.default_popup('You must chose a category for the assignment to be in.')
            else:
                utils.default_popup(f'An assignment with the name {name} already exists.')
        else:
            utils.default_popup('Assignment name cannot be blank.')

    def return_to_course(self) -> None:
        """returns to the course screen"""
        if self._name == '' and self._pts_rec == '' and self._pts_total == '' and self.ids.checkbox_graded.active:
            utils.switch_screen(self, 'course_view_screen', 'right')
        else:
            def yes_func():
                self.clear_fields()
                utils.switch_screen(self, 'course_view_screen', 'right')

            utils.yesno_popup('Are you sure you want to go back?  This assignment will not be added.', yes_func)
