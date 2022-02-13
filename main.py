from msilib import change_sequence
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
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from db import backEnd
from kivy import Config


# see how to get to those groups a-> new page or object beeing updated with group data ? 
# Check kivy lists system


darkBG = (13/255, 12/255, 29/255, 1)
oxfordBlue = (22/255, 27/255, 51/255, 1)
purpleNavy = (71/255, 73/255, 115/255, 1)
violetGrey = (166/255, 156/255, 172/255, 1)
almondWhite = (241/255, 218/255, 196/255, 1)

data = backEnd()

class customButton(Button):
    """Create a custom instance of the button to link it to the RecycleView's functions
    why can't I just define a on_press directly ? I don't know"""
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
        super().on_release(**kwargs)
        self.root_widget.goToUpdate(self.text)

class scrollerPage(RecycleView):
    """Display all the payment groups existing in the database"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.myGroups = data.getGroups()
        self.scrollerName = ObjectProperty()
    
    def refreshView(self):
        """At load, the list of wallets will be updated"""
        myGroups = data.getGroups()
        self.data = [{"text": item[0], \
            "root_widget": self } \
            for item in myGroups ]
    
    def goToUpdate(self, groupName):
        app = App.get_running_app()
        #TODO change screen accordingly
        groupInfo = data.readWallet(groupName)
        app.curr_group = groupName
        app.curr_group_info = groupInfo
        app.root.current = "WalletUpdate"


class MainPage(Screen):
    def on_enter(self, *args):
        """
        updates the scroll view in main page every time we get in
        """
        self.ids.scrollerController.refreshView()
    
    def updatePage(self, page):
        ...

class WalletUpdate(Screen):
    walletTitle = ObjectProperty()
    walletBalance = ObjectProperty()
    def on_enter(self, *args):
        """
        Match values from the selected wallet
        """

        app = App.get_running_app()
        infos = app.curr_group_info
        title = app.curr_group
        contacts = list(infos)
        print(contacts)
        self.walletTitle.text = title
        self.walletBalance.text = f"Summary of the wallet : \n {contacts[0]} spent {infos[contacts[0]][0]} €, {contacts[1]} spent {infos[contacts[1]][0]} €. \n  Balance {infos[contacts[0]][0] - infos[contacts[1]][0] € } "

class addGroups(Screen):
    """
    Will handle the creation of new groups in your database
    """

    groupName = StringProperty()
    commandState = ObjectProperty()

    def checkUp(self):
        """ Prevent user from using the same group name twice"""
        self.myGroups = [item[0] for item in data.getGroups()]
        if self.groupName in self.myGroups:
            self.commandState.text = f"This name is already in use !"
            return

        self.commandState.text = f"The data base was created !"
        data.addValue(self.groupName, None, None, "create")
    
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.commandState.text = ""


class WalletApp(App):
    def build(self):
        Window.clearcolor = darkBG
        # Window.size =(400, 600)
        # Config.set('graphics', 'width', '200')
        # Config.set('graphics', 'height', '600')
        Builder.load_file('addGroups.kv')
        Builder.load_file('WalletUpdate.kv')
        self.sm = ScreenManager()

        app_pages = (MainPage, addGroups, WalletUpdate)
        for i in app_pages:
            self.sm.add_widget(i(name = i.__name__))
        
        curr_group = None
        cuur_group_info = None
        return self.sm

if __name__ == "__main__":
    WalletApp().run() 