from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import copy

import course, utils

class CategoryEditScreen(Screen):

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self._course = None
        self._category_layouts = dict()
        self._org_categories = None

    def init(self, c: course.Course) -> None:
        self._course = c
        self._category_layouts = dict()
        self._org_categories = copy.copy(self._course.categories)
        for c in self._course.categories:
            self.add_category_box(c, False)
        self.update_cat_box_height()

    def add_category_box(self, c: course.Category, update_height = True) -> None:
        """adds a category to the screen"""
        fl = FloatLayout(size_hint_y = 0.14)

        name_lbl = Label(text = 'Name', font_size = 15, size_hint = (0.4, 0.28), pos_hint = {'x': 0.05, 'y': 0.67})
        name_input = TextInput(id = '_name', text = c.name, font_size = 15, size_hint = (0.4, 0.30), pos_hint = {'x': 0.50, 'y': 0.67})

        weight_lbl = Label(text = 'Weight', font_size = 15, size_hint = (0.4, 0.28), pos_hint = {'x': 0.05, 'y': 0.33})
        weight_input = TextInput(id = '_weight', text = str(c.weight), font_size = 15, size_hint = (0.4, 0.30), pos_hint = {'x': 0.50, 'y': 0.33})

        def del_button_func(*args):
            def yes_func():
                self._course.del_category(c)
                print('removing', c.name)
                utils.SCREENS['schedule_screen']._schedule.projected_gpa = utils.SCREENS['schedule_screen']._schedule._calc_projected_gpa()
                utils.SCREENS['schedule_screen']._schedule.projected_gpa = utils.SCREENS['schedule_screen']._schedule.save()
                self.ids.cat_edit_box.remove_widget(fl)
                self.update_cat_box_height()

            utils.yesno_popup(f'Are you sure you want to delete "{c.name}"?  Any assignments left in the category will also be removed.', yes_func)


        del_button = Button(text = 'Delete', font_size = 15, size_hint = (0.4, 0.25), pos_hint = {'x': 0.50, 'y': 0.05}, on_release = del_button_func)

        fl.add_widget(name_lbl)
        fl.add_widget(name_input)
        fl.add_widget(weight_lbl)
        fl.add_widget(weight_input)
        fl.add_widget(del_button)

        if c.name == 'General':
            name_input.disabled = True
            fl.remove_widget(del_button)

        self._category_layouts[c.name] = [c, fl, name_input, weight_input]
        self.ids.cat_edit_box.add_widget(fl)

        if update_height:
            update_cat_box_height()

    def save_categories(self) -> None:
        """saves all of the changes made to the categories"""
        cats = []
        for cat, fl, n, w in self._category_layouts.values():
            name = n.text.strip()
            if name.replace(' ', '') != '':                 # if all categories have a name, continue
                try:
                    weight_f = float(w.text)   # if all weights are valid
                except ValueError:
                    utils.default_popup(f'The weight of {name} must be a number.')
                    break
                else:
                    cats.append((name, weight_f))
            else:
                utils.default_popup('All categories must have a name.')
                break
        else:
            s = sum([i[1] for i in cats])
            if s == 100:
                for i in range(len(self._course.categories)):
                    self._course.categories[i].name = cats[i][0]
                    self._course.categories[i].weight = cats[i][1]
                utils.SCREENS['course_view_screen'].init(self._course)
                utils.SCREENS['schedule_screen']._schedule.save()
                utils.switch_screen(self, 'course_view_screen', 'right')
                self.clear_fields()
            else:
                utils.default_popup(f'The sum of all weights must be 100%, it is currently {s}%')

    def update_cat_box_height(self) -> None:
        """updates the cateogry scroll view height"""
        self.ids.cat_edit_box.height = len(self._course.categories) * utils.DEFAULT_WIDGET_HEIGHT * 2

    def clear_fields(self) -> None:
        for w in self._category_layouts.values():
            self.ids.cat_edit_box.remove_widget(w[1])
        self._course = None

    def return_to_course(self) -> None:
        """switches back to the course screen"""
        def yes_func():
            self._course.categories = self._org_categories
            utils.SCREENS['course_view_screen'].init(self._course)
            utils.SCREENS['schedule_screen']._schedule.save()
            utils.switch_screen(self, 'course_view_screen', 'right')
            self.clear_fields()
        utils.yesno_popup('Are you sure you want to go back?  Any changes made will not be saved.', yes_func)
