from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.clock import Clock
import course, utils

class AssignmentScreen(Screen):
    _name, _pts_rec, _pts_total = StringProperty(), StringProperty(), StringProperty()
    _course, _assignment = None, None

    def init(self, c: course.Course, a: course.Assignment) -> None:
        """must be called when editing an assignment"""
        self.init_new(c)
        self._assignment = a
        self._name = a.name
        self.ids.checkbox_graded.active = a.is_graded()
        self._pts_rec = str(a.pts_rec) if a.pts_rec is not None else ''
        self._pts_total = str(a.pts_total)
        self.ids.cat_spinner.text = self._course.get_cateogry_from_assign(a).name

    def init_new(self, c: course.Course) -> None:
        """must be called when adding a new assignment"""
        self._course = c
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


    def add_assignment(self) -> None:
        """adds the assignment to the course"""
        name = self._name.strip()
        if name.replace(' ', '') != '':                     # if the name is empty space, show an error
            pts_rec_f = None
            if self.ids.checkbox_graded.active:
                try:
                    pts_rec_f = float(self._pts_rec)
                    if pts_rec_f < 0:
                        utils.default_popup('Points recieved must be greater than 0.')
                        return
                except ValueError:
                    utils.default_popup('Points recieved must be a number.')
                    return
            try:
                pts_total_f = float(self._pts_total)
                if pts_total_f < 0:
                    utils.default_popup('Poins total must be greater than 0.')
                    return
            except ValueError:
                utils.default_popup('Points total must be a number.')
            else:
                if self.ids.cat_spinner.text in self.ids.cat_spinner.values: # if the category has not been chosen, show an error
                    if self._assignment is not None:                         # if you are editing an assignment, first remove the old one, then
                        self._course.del_assignment(self._assignment)            # add in the new one, otherwise just add the new one
                    self._course.add_assignment(self._course.get_category(self.ids.cat_spinner.text), course.Assignment(name, pts_rec_f, pts_total_f))
                    utils.SCREENS['course_view_screen'].init(self._course)
                    utils.SCREENS['schedule_screen'].update_gpa()
                    utils.SCREENS['schedule_screen']._schedule.save()
                    utils.switch_screen(self, 'course_view_screen', 'right')
                    self.clear_fields()
                else:
                    utils.default_popup('You must chose a category for the assignment to be in.')
        else:
            utils.default_popup('Assignment name cannot be blank.')

    def return_to_course(self) -> None:
        """returns to the course screen"""
        def yes_func():
            self.clear_fields()
            utils.switch_screen(self, 'course_view_screen', 'right')

        if self._assignment is not None:
            str_pts_rec = '' if self._assignment.pts_rec is None else str(self._assignment.pts_rec)
            if self._name != self._assignment.name or self.ids.checkbox_graded.active != self._assignment.is_graded() or self._pts_rec != str_pts_rec or self._pts_total != str(self._assignment.pts_total) or self.ids.cat_spinner.text != self._course.get_cateogry_from_assign(self._assignment).name:
                utils.yesno_popup('Are you sure you want to go back?  This assignment will not be updated.', yes_func)
            else:
                yes_func()

        elif self._name == '' and self._pts_rec == '' and self._pts_total == '' and self.ids.checkbox_graded.active:
            utils.switch_screen(self, 'course_view_screen', 'right')
        else:
            utils.yesno_popup('Are you sure you want to go back?  This assignment will not be added.', yes_func)
