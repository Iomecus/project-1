from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem



Window.size = (360, 792)

class MyLayout(FloatLayout):
    screen_manager = ObjectProperty(None)
    activeWindow = None #save popup to close them with button
    trainingsList = [] #[[name1, duration1, [activity1.1, activity1.2, ...]], [name2, duration 2,[activity2.1, activity2.2, ...]], ...]
    inCreationTraining = [] #[id, [activity1, activity2, ...]] activity1 = [name, duration in second]
    currentTraining =  None #index of the current training in trainingsList

    def switch_screen(self, screen):
        self.screen_manager.current = screen

    def open_new_training_popup(self):
        show = NewTrainingPopup(layout=self)
        self.show_popup(show=show, size=(300,300))

    def open_new_activity_popup(self):
        show = NewActivityPopup(layout=self)
        self.show_popup(show=show, size=(300,300))

    def show_popup(self, show, size=(0,0)):
        popupWindow = Popup(
            title = 'Create a training',
            content = show,
            size_hint = (None,None),
            size = size
        )
        self.activeWindow = popupWindow
        popupWindow.open()

    def training_creation_finished(self):
        self.activity_list.clear_widgets()
        trainingLength = ''
        duration = self.trainingsList[-1][1]
        if duration//3600 > 0:
            nbHour = duration//3600
            trainingLength += str(nbHour) + 'h'
            duration -= nbHour * 3600
            nbMinute = duration//60
            trainingLength += str(nbMinute) + 'm'
            duration -= nbMinute * 60
            trainingLength += str(duration) + 's'
        elif duration//60 > 0:
            nbMinute = duration//60
            trainingLength += str(nbMinute) + 'm'
            duration -= nbMinute * 60
            trainingLength += str(duration) + 's'
        else:
            trainingLength += str(duration) + 's'

        self.trainings_list.add_widget(OneLineListItem(
                    text = self.trainingsList[-1][0] + ' (' + trainingLength + ')',
                    on_release = lambda x: self.switch_screen('screen2')
                ))
        self.switch_screen('home_screen')

class NewTrainingPopup(FloatLayout):
    def __init__(self, layout: None, **kwargs):
        super().__init__(**kwargs)
        self.layout = layout
    
    def exit(self):
        self.layout.activeWindow.dismiss()
    
    def create_new_training(self):
        if self.training_name.text != '':
            self.exit()
            name = self.training_name.text
            self.layout.trainingsList.append([name, 0, []])
            self.layout.inCreationTraining = [len(self.layout.trainingsList)-1, []]
            self.layout.switch_screen('creation_screen')
            self.layout.in_creation_training_name.text = name
        else:
            self.error_message.text = 'You have to enter a name'

class NewActivityPopup(FloatLayout):
    def __init__(self, layout: None, **kwargs):
        super().__init__(**kwargs)
        self.layout = layout
    
    def exit(self):
        self.layout.activeWindow.dismiss()
    
    def create_new_activity(self):
        if self.name_input.text != '':
            if self.hour_input.text != '00' or self.minute_input.text != '00' or self.second_input.text != '00':
                duration = 0
                if self.hour_input.text != '00':
                    activityLength = self.hour_input.text + 'h' + self.minute_input.text + 'm' + self.second_input.text + 's'
                    duration += int(self.hour_input.text) * 3600
                elif self.minute_input.text != '00':
                    activityLength = self.minute_input.text + 'm' + self.second_input.text + 's'
                    duration += int(self.minute_input.text) * 60
                else:
                    activityLength = self.second_input.text + 's'
                    duration += int(self.second_input.text)
                self.layout.inCreationTraining[1].append([self.name_input.text, duration])
                self.layout.trainingsList[self.layout.inCreationTraining[0]][1] += duration
                self.layout.activity_list.add_widget(OneLineListItem(
                    text = self.name_input.text + ' (' +activityLength + ')'
                ))
                self.exit()


class App(MDApp):
    title = "Sport APP"
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette= "Red"
        return Builder.load_file('app.kv')

App().run()
