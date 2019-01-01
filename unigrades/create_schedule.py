from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import schedule, utils

class CreateSchedule(Screen):

    _name, _gpa, _units = StringProperty(), StringProperty(), StringProperty()

    def _clear_text_fields(self):
        self._name = ''
        self._gpa = ''
        self._units = ''

    def back(self) -> None:

        if (self._name == '' and self._gpa == '' and self._units == ''):
            utils.switch_screen(self, 'home_screen', 'right')                     # if no changes have been made, then slide back
        else:

            def yes_func():
                self._clear_text_fields()
                utils.switch_screen(self, 'home_screen', 'right')                 # if changes have been made make sure they meant to go back

            utils.yesno_popup('Are you sure you want to go back?\nThis schedule will not be saved.', yes_func)

    def create(self) -> None:
        name = self._name.strip()
        if name != '':                                                      # if the name is not empty space or just spaces
            if name not in utils.SCREENS['home_screen'].sch_names:          # it a schedule of that name does not already exist
                gpa_f = 0
                try:                                                        # make sure the GPA is a number
                    gpa_f = float(self._gpa)
                except ValueError:
                    utils.default_popup('G.P.A. must be a number.')
                else:
                    if gpa_f < 0:                                           # make sure the GPA is >= 0
                        utils.default_popup('G.P.A. must be greater than zero.')
                    else:
                        try:
                            units_f = float(self._units.strip())            # make sure the units is a number
                        except ValueError:
                            utils.default_popup('Previous units taken must be a number.')
                        else:
                            units_i = int(units_f)
                            if (units_f < 0):                               # make sure the units is >= 0
                                utils.default_popup('Previous units taken must be greater than zero.')
                            elif (units_i != units_f):                      # make sure the units is a whole number
                                utils.default_popup('Previous units taken must be a whole number')
                            else:
                                sch = schedule.Schedule(name, gpa_f, units_i, [])
                                sch.save()
                                utils.SCREENS['schedule_screen'].init(sch)
                                utils.switch_screen(self, 'schedule_screen', 'left')

                                utils.SCREENS['home_screen'].add_sch_button(name)
                                utils.SCREENS['home_screen'].check_view_no_sch_lbl()

                                self._clear_text_fields()
            else:
                utils.default_popup(f'A schedule with that name "{name}" already exists.')
        else:
            utils.default_popup('Schedule name cannot be left blank.')
