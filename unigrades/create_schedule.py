from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty
import schedule, utils

class CreateSchedule(Screen):

    _name, _gpa, _units = StringProperty(), StringProperty(), StringProperty()

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
        name = self._name.strip()
        if name != '':         # if the name is not empty space or just spaces
            if name not in utils.SCREENS['home_screen'].sch_names:
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
                            units_f = float(self._units.strip())    # make sure the units is a number
                        except ValueError:
                            utils.default_popup('Previous units taken must be a number.')
                        else:
                            units_i = int(units_f)
                            if (units_f < 0):               # make sure the units is >= 0
                                utils.default_popup('Previous units taken must be greater than zero.')
                            elif (units_i != units_f): # make sure the units is a whole number
                                utils.default_popup('Previous units taken must be a whole number')
                            else:
                                sch = schedule.Schedule(name, gpa_f, units_i, [])
                                sch.save()
                                utils.SCREENS['schedule_screen'].init(sch)
                                utils.switch_screen(self, 'schedule_screen', 'left')

                                if len(utils.SCREENS['home_screen'].sch_names) == 0:
                                    utils.SCREENS['home_screen'].view_no_sch_lbl(False)
                                utils.SCREENS['home_screen'].add_sch_button(name)

                                self._clear_text_fields()
            else:
                utils.default_popup(f'A schedule with that name "{name}" already exists.')
        else:
            utils.default_popup('Schedule name cannot be left blank.')
