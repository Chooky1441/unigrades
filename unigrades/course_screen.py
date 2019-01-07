from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
import course, utils

class CourseScreen(Screen):

    _name, _units = StringProperty(), StringProperty()

    _a, _aminus = StringProperty(), StringProperty()
    _bplus, _b, _bminus = StringProperty(), StringProperty(), StringProperty()
    _cplus, _c, _cminus = StringProperty(), StringProperty(), StringProperty()
    _dplus, _d, _dminus = StringProperty(), StringProperty(), StringProperty()

    _course = None

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self._clear_fields()                    # this has to be called so that the default percentages for the
                                                # cutpointset are on screen

    def init(self, c: course.Course) -> None:
        """Initalizes the values to the editor"""
        self._course = c
        self._override = True
        self._name = self._course.name
        self._units = str(self._course.units)
        self._p_np = self._course.p_np
        self._a = str(self._course.cutpointset.a)
        self._aminus = str(self._course.cutpointset.aminus)
        self._bplus = str(self._course.cutpointset.bplus)
        self._b = str(self._course.cutpointset.b)
        self._bminus = str(self._course.cutpointset.bminus)
        self._cplus = str(self._course.cutpointset.cplus)
        self._c = str(self._course.cutpointset.c)
        self._cminus = str(self._course.cutpointset.cminus)
        self._dplus = str(self._course.cutpointset.dplus)
        self._d = str(self._course.cutpointset.d)
        self._dminus = str(self._course.cutpointset.dminus)
        self.ids.checkbox_pnp.active = self._course.p_np

    def _clear_fields(self) -> None:
        """clears all of the text fields"""
        self._name = ''
        self._units = ''
        self._p_np = False
        self._a = '93.5'
        self._aminus = '90.0'
        self._bplus = '86.5'
        self._b = '83.5'
        self._bminus = '80.0'
        self._cplus = '76.5'
        self._c = '73.5'
        self._cminus = '70.0'
        self._dplus = '66.5'
        self._d = '63.5'
        self._dminus = '60.0'
        self.ids.checkbox_pnp.active = False
        self._course = None


    def create(self) -> None:
        name = self._name.strip()
        if name.replace(' ', '') != '':                                         # if the name is blank space, show an error
            if self._course is not None or name not in [c.name for c in utils.SCREENS['schedule_screen']._schedule.courses]:
                try:
                    units_f = float(self._units)                                # if the units is not a number, show an error
                except ValueError:
                    utils.default_popup('Units must be a number')
                else:
                    if units_f > 0:
                        cutpointset = {'A': self._a, 'A-': self._aminus, 'B+': self._bplus, 'B': self._b, 'B-': self._bminus, 'C+': self._cplus,
                                       'C': self._c, 'C-':self. _cminus, 'D+': self._dplus, 'D':self. _d, 'D-': self._dminus}

                        cutpointset_items = list(cutpointset.items())
                        for i in range(len(cutpointset)):                       # if any cutpoint is not a number, show an error
                            try:
                                perc_f = float(cutpointset_items[i][1])
                                if perc_f > 100:                                # if any cutpoint number is over 100, show an error
                                    utils.default_popup(f'The percentage for {cutpointset_items[i][0]} must be less than or equal to 100')
                                    break
                                elif i > 0 and perc_f > float(cutpointset_items[i - 1][1]): # if the percentages are not in decending order, show an error
                                    utils.default_popup(f'The percentage of {cutpointset_items[i][0]} ({cutpointset_items[i][1]}) cannot be greater than the percentage of {cutpointset_tiems[i - 1][0]} ({cutpointset_items[i - 1][0]}).')
                            except ValueError:
                                utils.default_popup(f'The percentage for {cutpointset_items[i][0]} must be a number.')
                                break
                        else:
                            cps = course.CutPointSet(float(self._a), float(self._aminus),
                                                     float(self._bplus), float(self._b), float(self._bminus),
                                                     float(self._cplus), float(self._c), float(self._cminus),
                                                     float(self._dplus), float(self._d), float(self._dminus))

                            cats = [] if self._course is None else self._course.categories

                            utils.SCREENS['schedule_screen'].add_course(course.Course(name, units_f, cps, cats, self.ids.checkbox_pnp.active))
                            screen = 'schedule_screen'
                            if self._course is not None:
                                utils.SCREENS['schedule_screen'].remove_course(self._course)
                                self._course = None
                                screen = 'course_view_screen'

                            self._clear_fields()
                            utils.switch_screen(self, screen, 'left')
                    else:
                        utils.default_popup('Units must be a positive number.')
            else:
                utils.default_popup(f'A course with the name "{name}" already exists.')
        else:
            utils.default_popup('Course name cannot be left blank.')


    def back(self) -> None:

        def return_to():
            if self._course is None:
                utils.switch_screen(self, 'schedule_screen', 'right')
            else:
                utils.switch_screen(self, 'course_view_screen', 'right')

        show_warning = False
        cutpointset = [self._a, self._aminus, self._bplus, self._b, self._bminus, self._cplus, self._c, self. _cminus, self._dplus, self. _d, self._dminus]

        if self._course is not None and self._name == self._course.name and self._units == str(self._course.units) and self.ids.checkbox_pnp.active == self._course.p_np and cutpointset == self._course.cutpointset.str_list():
            self._clear_fields()
            utils.switch_screen(self, 'course_view_screen', 'right')
            return

        elif self._name != '' or self._units != '' or self._p_np != False:    # if any of the fields have been modified, show a warning
            show_warning = True
        else:
            defaultset = ['93.5', '90.0', '86.5', '83.5', '80.0', '76.5', '73.5', '70.0', '66.5', '63.5', '60.0']
            for i in range(len(defaultset)):
                if cutpointset[i] != defaultset[i]:
                    show_warning = True
                    break

        if not show_warning:                                        # else just go back
            return_to()
        else:

            def yes_func():
                self._clear_fields()
                return_to()

            utils.yesno_popup('Are you sure you want to go back?  This course will not be added.', yes_func)
