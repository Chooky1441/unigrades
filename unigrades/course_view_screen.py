from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
import course, utils

class CourseViewScreen(Screen):

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self._course = None
        self._no_assign_lbl = Label(text = 'You have no assignments', italic = True, color = [1, 1, 1, 0.75])
        self._no_assign_lbl.font_size = self._no_assign_lbl.height * 0.2
        self._cat_widgets = []
        self._assign_layouts = dict()

    def init(self, c: course.Course) -> None:
        for fl in self._assign_layouts.values():
            self.ids.assignment_box.remove_widget(fl)
        for w in self._cat_widgets:
            self.ids.assignment_box.remove_widget(w)
        self._assign_layouts = dict()
        self._cat_widgets = []
        self._course = c
        self.ids.course_name.text = c.name
        self.ids.lbl_grade.text = f'Grade: {c.letter_grade()}'
        self.ids.lbl_units.text = f'Units: {c.units}'
        for cat in self._course.categories:
            lbl = Label(text = f'Category: {cat.name}', font_size = 20, size_hint = (1, 0.05), halign = 'center', valign = 'middle')
            self.ids.assignment_box.add_widget(lbl)
            div = utils.Dividor()
            self.ids.assignment_box.add_widget(div)
            self._cat_widgets += [lbl, div]
            for a in cat.assignments:
                self.add_assignment_button(a)
        self.update_assign_box_height()
        self.check_view_no_assign_lbl()

    def check_view_no_assign_lbl(self) -> None:
        """turns on or off the no assignment message"""
        if self._course.amt_of_assignments() == 0:
            if (self._no_assign_lbl not in self.ids.assignment_box.children):
                self.ids.assignment_box.height = self._no_assign_lbl.height
                self.ids.assignment_box.add_widget(self._no_assign_lbl)
        else:
            self.ids.assignment_box.remove_widget(self._no_assign_lbl)

    def add_assignment_button(self, a: course.Assignment) -> None:
        """add the assignment to the screen"""
        fl = FloatLayout(size_hint_y = 0.14, )
        name_lbl = Label(id = 'name_lbl', text = a.name, font_size = 15, size_hint = (1, 0.5), pos_hint = {'x': -0.2, 'y': 0.50}, halign = 'left', valign = 'middle')
        grade_str = f'Grade: N\A' if a.pts_rec is None else f'Grade: {a.pts_rec}/{a.pts_total}'
        grade_lbl = Label(id = 'grade_lbl', text = grade_str, font_size = 15, size_hint = (1, 0.5), pos_hint = {'x': -0.2, 'y': 0.05})
        edit_bttn = Button(text = 'Edit', size_hint = (0.35, 0.4), pos_hint = {'x': 0.6, 'y': 0.50})

        def del_assign(*args):
            self.ids.assignment_box.remove_widget(self._assign_layouts[a.name])
            del self._assign_layouts[a.name]
            self._course.del_assignment(a)
            utils.SCREENS['schedule_screen']._schedule.projected_gpa = utils.SCREENS['schedule_screen']._schedule._calc_projected_gpa()
            self.ids.lbl_grade.text = f'Grade: {self._course.letter_grade()}'
            self.update_assign_box_height()

        delete_bttn = Button(text = 'Delete', size_hint = (0.35, 0.4), pos_hint = {'x': 0.6, 'y': 0.05}, on_release = del_assign)
        fl.add_widget(name_lbl)
        fl.add_widget(grade_lbl)
        fl.add_widget(edit_bttn)
        fl.add_widget(delete_bttn)
        self.ids.assignment_box.add_widget(fl)
        self._assign_layouts[a.name] = fl

    def update_assign_box_height(self) -> None:
        """sets the box inside the scroll view to the appropriate height"""
        self.ids.assignment_box.height = (self._course.amt_of_assignments() + len(self._course.categories)) * utils.DEFAULT_WIDGET_HEIGHT

    def return_to_schedulescreen(self) -> None:
        """switches back to the schedule screen"""
        # clear everything
        utils.SCREENS['schedule_screen']._schedule.save()
        utils.switch_screen(self, 'schedule_screen', 'right')

    def launch_assignment_screen(self) -> None:
        """opens up the assignment editor"""
        utils.SCREENS['assignment_screen'].init_new(self._course)
        utils.switch_screen(self, 'assignment_screen', 'left')

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
