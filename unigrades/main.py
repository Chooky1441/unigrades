from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock

import home_screen, create_schedule, schedule_screen, course_screen, assignment_screen, course_view_screen, category_screen, category_edit_screen, utils

class UniGrades(App):
    def build(self):
        return MainScreen()

class MainScreen(ScreenManager):
    def __init__(self, **kwargs):
        ScreenManager.__init__(self, **kwargs)
        Builder.load_file('home_screen.kv')
        Builder.load_file('create_schedule.kv')
        Builder.load_file('schedule_screen.kv')
        Builder.load_file('course_screen.kv')
        Builder.load_file('assignment_screen.kv')
        Builder.load_file('course_view_screen.kv')
        Builder.load_file('category_screen.kv')
        Builder.load_file('category_edit_screen.kv')

        self._home_screen = home_screen.HomeScreen()
        self.add_widget(self._home_screen)
        self._create_screen = create_schedule.CreateSchedule()
        self.add_widget(self._create_screen)
        self._schedule_screen = schedule_screen.ScheduleScreen()
        self.add_widget(self._schedule_screen)
        self._course_screen = course_screen.CourseScreen()
        self.add_widget(self._course_screen)
        self._assignment_screen = assignment_screen.AssignmentScreen()
        self.add_widget(self._assignment_screen)
        self._course_view_screen = course_view_screen.CourseViewScreen()
        self.add_widget(self._course_view_screen)
        self._category_screen = category_screen.CategoryScreen()
        self.add_widget(self._category_screen)
        self._category_edit_screen = category_edit_screen.CategoryEditScreen()
        self.add_widget(self._category_edit_screen)

        utils.SCREENS = {'home_screen': self._home_screen, 'create_screen': self._create_screen, 'schedule_screen': self._schedule_screen,
                         'course_screen': self._course_screen, 'assignment_screen': self._assignment_screen, 'course_view_screen': self._course_view_screen,
                         'category_screen': self._category_screen, 'category_edit_screen': self._category_edit_screen}

if __name__ == '__main__':
    UniGrades().run()
