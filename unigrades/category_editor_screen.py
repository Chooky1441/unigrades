import kivy.uix.screenmanager import Screen
import course, utils

class CategoryEditorScreen(Screen):

    _course = None

    def clear_fields(self) -> None:
        pass

    def return_to_course(self) -> None:
        """switches back to the course screen"""
        utils.switch_screen(self, 'course_view_screen', 'right')
