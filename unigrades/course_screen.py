from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import course, utils

class CourseScreen(Screen):

    _name, _units = StringProperty(), StringProperty()

    _a, _aminus = StringProperty(), StringProperty()
    _bplus, _b, _bminus = StringProperty(), StringProperty(), StringProperty()
    _cplus, _c, _cminus = StringProperty(), StringProperty(), StringProperty()
    _dplus, _d, _dminus = StringProperty(), StringProperty(), StringProperty()

    _p_np = False

    _categories = {'General': 100}

    def _clear_fields(self) -> None:
        """clears all of the text fields"""
        self._name = ''
        self._units = ''

        self._p_np = False
        self._categories = {'General': 100}

    def create(self) -> None:
        name = self._name.strip()
        if name.replace(' ', '') != '':                                         # if the name is blank space, show an error
            if name not in [c.name for c in utils.SCREENS['schedule_screen']._schedule.courses]:
                try:
                    units_f = float(self._units)                                # if the units is not a number, show an error
                except ValueError:
                    utils.default_popup('Units must be a number')
                else:
                    if units_f > 0:
                        cutpointset = {'A': self._a, 'A-': self._aminus, 'B+': self._bplus, 'B': self._b, 'B-': self._bminus, 'C+': self._cplus,
                                       'C': self._c, 'C-':self. _cminus, 'D+': self._dplus, 'D':self. _d, 'D-': self._dminus}

                        cutpointset_items = list(cutpointset.items())
                        for i in range(len(cutpointset)):                           # if any cutpoint is not a number or if they are not in order, show an error
                            try:
                                perc_f = float(cutpointset_items[i][1])
                                if perc_f > 100:
                                    utils.default_popup(f'The percentage for {cutpointset_items[i][0]} must be less than or equal to 100')
                                    break
                            except ValueError:
                                utils.default_popup(f'The percentage for {cutpointset_items[i][0]} must be a number.')
                                break
                        else:
                            total_perc = 0
                            for k, v in self._categories.items():                   # if any category does not have a percentage value or if they add up to more
                                try:                                                # than 100%, show an error
                                    percent = float(v)
                                    total_perc += percent
                                except ValueError:
                                    utils.default_popup(f"{k}'s value '{v}' is not a valid number.")
                                    break
                                if total_perc > 100:
                                    utils.default_popup(f'The total percents of all the categories add up to more than 100: {total_perc}')
                                    break
                            else:
                                cps = course.CutPointSet(float(self._a), float(self._aminus),
                                                         float(self._bplus), float(self._b), float(self._bminus),
                                                         float(self._cplus), float(self._c), float(self._cminus),
                                                         float(self._dplus), float(self._d), float(self._dminus))

                                cats = [course.Category(name, weight) for name, weight in self._categories.items()]
                                c = course.Course(name, units_f, cps, cats, self._p_np)
                                utils.SCREENS['schedule_screen']._schedule.add_course(c)
                                self._clear_fields()
                                utils.switch_screen(self, 'schedule_screen', 'left')
                    else:
                        utils.default_popup('Units must be a positive number.')
            else:
                utils.default_popup(f'A course with the name "{name}" already exists.')
        else:
            utils.default_popup('Course name cannot be left blank.')

    def back(self) -> None:

        show_warning = False
        if self._name != '' or self._units != '' or self._p_np != False:    # if any of the fields have been modified, show a warning
            show_warning = True
        else:
            cutpointset = {'A': self._a, 'A-': self._aminus, 'B+': self._bplus, 'B': self._b, 'B-': self._bminus, 'C+': self._cplus,
                           'C': self._c, 'C-':self. _cminus, 'D+': self._dplus, 'D':self. _d, 'D-': self._dminus}
            for value in cutpointset.values():
                if value != '':
                    show_warning = True
                    print("HERE", value)
                    break
            else:
                if self._categories != {'General': 100}:
                    show_warning = True
                    print("HRHEHRER")

        if not show_warning:                                        # else just go back
            utils.switch_screen(self, 'schedule_screen', 'right')
        else:

            def yes_func():
                self._clear_fields()
                utils.switch_screen(self, 'schedule_screen', 'right')

            utils.yesno_popup('Are you sure you want to go back?\nThis course will not be added.', yes_func)
