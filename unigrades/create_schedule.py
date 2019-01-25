from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import schedule, schedule_loader, utils

class CreateSchedule(Screen):

    _name, _gpa, _units = StringProperty(), StringProperty(), StringProperty()
    _schedule = None

    def _clear_text_fields(self):
        self._name = ''
        self._gpa = ''
        self._units = ''

    def init(self, s: schedule.Schedule) -> None:
        """initalizes the text inputs with the given schedule's values"""
        self._schedule = s
        self._name = self._schedule.name
        self._gpa = str(self._schedule.current_gpa)
        self._units = str(self._schedule.current_units)

    def back(self) -> None:
        if (self._schedule is not None and self._name == self._schedule.name and
            self._gpa == str(self._schedule.current_gpa) and self._units == str(self._schedule.current_units)):
            self._clear_text_fields()
            utils.switch_screen(self, 'schedule_screen', 'right')
            return

        elif (self._name == '' and self._gpa == '' and self._units == ''):
            utils.switch_screen(self, 'home_screen', 'right')                     # if no changes have been made, then slide back
        else:

            def yes_func():
                self._clear_text_fields()
                utils.switch_screen(self, 'home_screen', 'right')                 # if changes have been made make sure they meant to go back

            utils.yesno_popup('Are you sure you want to go back?  This schedule will not be saved.', yes_func)

    def create(self) -> None:
        name = self._name.strip()
        if name != '':                                                      # if the name is not empty space or just spaces
            if self._schedule is not None or name not in utils.SCREENS['home_screen'].sch_names:          # it a schedule of that name does not already exist
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
                                if self._schedule is None:                  # if there is no schedule, it is a new schedule
                                    self._schedule = schedule.Schedule(name, gpa_f, units_i, [])
                                else:                                       # otherwise update the current one and save it
                                    schedule_loader.delete_schedule(self._schedule.name)
                                    utils.SCREENS['home_screen'].remove_schedule(self._schedule.name)
                                    self._schedule.name = name
                                    self._schedule.current_gpa = gpa_f
                                    self._schedule.current_units = units_i
                                    self._schedule.save()

                                self._schedule.save()
                                utils.SCREENS['schedule_screen'].init(self._schedule)
                                self._schedule = None
                                utils.switch_screen(self, 'schedule_screen', 'left')

                                utils.SCREENS['home_screen'].add_sch_button(name)
                                utils.SCREENS['home_screen'].check_view_no_sch_lbl()
                                self._clear_text_fields()
            else:
                utils.default_popup(f'A schedule with that name "{name}" already exists.')
        else:
            utils.default_popup('Schedule name cannot be left blank.')
