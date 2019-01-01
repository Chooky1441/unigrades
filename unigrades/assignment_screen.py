from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import course, utils

class AssignmentScreen(Screen):
    _name, _pts_rec, _pts_total = StringProperty(), StringProperty(), StringProperty()
    _is_graded = True
    _course, _category = None, None # need to be dropdown menus


    def _clear_fields(self) -> None:
        """resets all of the input fields"""
        self._name = ''
        self._pts_rec = ''
        self._pts_total = ''
        self._is_graded = True
        # something here???

    
