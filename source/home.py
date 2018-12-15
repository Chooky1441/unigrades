from kivy.uix.boxlayout import BoxLayout

import random
class HomePage(BoxLayout):

    def change_color(self, *args):
        color = [random.random() for i in range(3)] + [1]
        label = self.ids['my_label']
        label.color = color
