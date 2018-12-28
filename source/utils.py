from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

DG = 0.13
G = 0.18
LG = 0.26

DEFAULT_TRANSITION_LENGTH = 0.15

TO_GPA = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}

def to_gpa(grade: str) -> float:
    """returns the gpa the student has based on the letter grade (4.0 scale)"""
    return TO_GPA[grade]

def default_popup(text: str, title: str = 'Warning') -> None:
    err_box = BoxLayout(orientation = 'vertical', padding = (10))

    err_txt = Label(text = text, font_size = 15)
    err_box.add_widget(err_txt)

    close_button = Button(text = "Close")
    err_box.add_widget(close_button)
    err = Popup(title = title, content = err_box, size_hint = (0.6, 0.4))
    close_button.bind(on_release = err.dismiss)
    err.open()

def yesno_popup(text: str, yes_func: 'function') -> None:
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = text))

    button_box = BoxLayout(orientation = 'horizontal')
    box.add_widget(button_box)

    yes_button = Button(text = 'Yes')
    no_button = Button(text = 'No')

    button_box.add_widget(yes_button)
    button_box.add_widget(no_button)

    popup = Popup(title = 'Warning', content = box, size_hint = (0.6, 0.4))

    def new_yes_func(*args):
        yes_func()
        popup.dismiss()

    yes_button.bind(on_release = new_yes_func)
    no_button.bind(on_release = popup.dismiss)

    popup.open()

# custom exceptions
class InvalidCutPointException(Exception):
    def __init__(self, key: str):
        print(f'Invalid CutPointSet key: {key}')

class InvalidCategoryException(Exception):
    def __init__(self, c: str):
        print(f'Invalid category {c}.')

class ScheduleLoadError(Exception):
    def __init__(self, message: str):
        self.message = message

class ScheduleSaveError(Exception):
    def __init__(self, message: str):
        self.message = message
