from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

DG = 0.13
G = 0.18
LG = 0.26

scale = 40
Window.size = (9 * scale, 16 * scale)

DEFAULT_TRANSITION_LENGTH = 0.15
DEFAULT_WIDGET_HEIGHT = Window.size[1] * 0.1


TO_GPA = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}

SCREENS = dict()

def to_gpa(grade: str) -> float:
    """returns the gpa the student has based on the letter grade (4.0 scale)"""
    return TO_GPA[grade]

def switch_screen(self, screen_name: str, slide_dir: str) -> None:
    """switches the screen to the given one"""
    self.parent.transition = SlideTransition(direction = slide_dir, duration = DEFAULT_TRANSITION_LENGTH)
    self.parent.current = screen_name

Builder.load_string('''
#: import utils utils
<Dividor>:
    size_hint_y: 0.0001
    canvas:
        Color:
            rgba: utils.LG, utils.LG, utils.LG, 1
        Rectangle:
            size: self.width, 2
            pos: self.pos
''')

class Dividor(BoxLayout):
    pass

Builder.load_string('''
<ScrollableLabel>:
    Label:
        text: root.text
        font_size: 15
        text_size: self.width, None
        size_hint_y: None
        halign: 'center'
        height: self.texture_size[1]
''')

class ScrollableLabel(ScrollView):
    text = StringProperty()

def default_popup(text: str, title: str = 'Warning') -> None:
    err_box = BoxLayout(orientation = 'vertical')
    err_txt = ScrollableLabel()
    err_txt.text = text
    err_box.add_widget(err_txt)

    close_button = Button(text = 'Close', size_hint_y = 0.35)
    err_box.add_widget(close_button)
    err = Popup(title = title, content = err_box, size_hint = (0.9, 0.4))

    close_button.bind(on_release = err.dismiss)
    err.open()


def yesno_popup(text: str, yes_func: 'function') -> None:
    box = BoxLayout(orientation = 'vertical', padding = (10))
    err_txt = ScrollableLabel()
    err_txt.text = text
    box.add_widget(err_txt)
    button_box = BoxLayout(orientation = 'horizontal')
    box.add_widget(button_box)

    yes_button = Button(text = 'Yes', size_hint_y = 0.35)
    no_button = Button(text = 'No', size_hint_y = 0.35)

    button_box.add_widget(yes_button)
    button_box.add_widget(no_button)

    popup = Popup(title = 'Warning', content = box, size_hint = (0.9, 0.4))

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

class ScheduleDeleteError(Exception):
    def __init__(self, message: str):
        self.message = message
