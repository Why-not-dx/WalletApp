from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty


class MainPage(Screen):
    ...

class MyGroups(Screen):
    def __init__(self, **kwargs):
        super(MyGroups, self).__init__(**kwargs)
        self.back_grid = BoxLayout(orientation = 'horizontal')
        self.add_widget(self.back_grid)
        self.back_grid.add_widget(Label( size_hint = (.15,1)))
        self.subgrid = BoxLayout(orientation= "vertical", spacing = "10dp")
        self.subgrid.add_widget(Image(source = "logo.jpg"))
        self.subgrid.add_widget(Label(text = "My wallets"))
        for i in range(5):
            self.subgrid.add_widget(Button(text = "Wallet " + str(i)))

        self.backButton = Button( 
                text = "Back",
                size_hint = (.5, .5),
                pos_hint = {"center_x": .5 },
                bold = True,
                background_color = "#00FFCE",
            )
        self.backButton.bind(on_press = lambda x: self.change_screen())
# check on padding_x and padding_y

        self.subgrid.add_widget(self.backButton)
        self.subgrid.add_widget(Label(size_hint = (1, .5)))
        self.back_grid.add_widget(self.subgrid)
        self.back_grid.add_widget(Label(size_hint = (.15,1)))
        print(self.manager, self.parent)
    
    def change_screen(self):
        if self.manager.current == "MyGroups":
            self.manager.transition.direction = "right"
            self.manager.current = "MainPage"

        else:
            self.manager.current = "MyGroups"
            self.manager.transition.direction = "right"

class GroupPage(Screen):
    ...


class MyContacts(Screen):
    ...


class WalletApp(App):

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Builder.load_file('MyContacts.kv')
        Builder.load_file('GroupPage.kv')

        sm = ScreenManager()
        app_pages = (MainPage, MyGroups, GroupPage, MyContacts)
        for i in app_pages:
            sm.add_widget(i(name = i.__name__))
        
        return sm

if __name__ == "__main__":
    WalletApp().run()
    