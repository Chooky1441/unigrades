from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty
import utils

class CreateSchedule(Screen):

    _name, _gpa, _units = StringProperty(), StringProperty(), StringProperty()

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def _clear_text_fields(self):
        self._name = ''
        self._gpa = ''
        self._units = ''

    def back(self) -> None:

        def slide_back():
            self.parent.transition = SlideTransition(direction = 'right', duration = utils.DEFAULT_TRANSITION_LENGTH)
            self.parent.current = 'home_screen'

        if (self._name == '' and self._gpa == '' and self._units == ''):
            slide_back()
        else:

            def yes_func():
                self._clear_text_fields()
                slide_back()

            utils.yesno_popup('Are you sure you want to go back?\nThis schedule will not be saved.', yes_func)

    def create(self) -> None:

        if self._name.replace(' ', '') != '':         # if the name is not empty space or just spaces
            gpa_f = 0
            try:                                        # make sure the GPA is a number
                gpa_f = float(self._gpa)
            except ValueError:
                utils.default_popup('G.P.A. must be a number.')
            else:
                if gpa_f < 0:                           # make sure the GPA is >= 0
                    utils.default_popup('G.P.A. must be greater than zero.')
                else:
                    try:
                        units_f = float(self._units)    # make sure the units is a number
                    except ValueError:
                        utils.default_popup('Previous units taken must be a number.')
                    else:
                        if (units_f < 0):               # make sure the units is >= 0
                            utils.default_popup('Previous units taken must be greater than zero.')
                        elif (int(units_f) != units_f): # make sure the units is a whole number
                            utils.default_popup('Previous units taken must be a whole number')
                        else:
                            self._clear_text_fields()
                            pass # create a new schedule
        else:
            utils.default_popup('Schedule name cannot be left blank.')
