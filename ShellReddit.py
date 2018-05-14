import kivy
import webbrowser
# import pprint
kivy.require("1.10.0")
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import APIAuth

reddit = APIAuth.getAuth()

LabelBase.register(name = "Capture", fn_regular = "Capture_it_2.ttf")

base_commands = ['cls','set','search','view','ls']
links = []
listed = False
listofsubmissions = []
countlist = 0

class ScrollableLabel(BoxLayout):
    stackid=ObjectProperty(None)
    idvalue = StringProperty("  [color=#33cc33][b]guest@reddit:$[/b][/color]")

    def addNew(self):
        l = Label( id = 'labelid',
                    text = "  [color=#33cc33][b]guest@reddit:$[/b][/color]",
                    padding_y = 2,
                    pos_hint =  {'top': 1},
                    font_size =  13,
                    size_hint_y = None,
                    markup = True)
        l.bind(width=lambda s, w:
                   s.setter('text_size')(s, (w, None)))
        l.bind(texture_size=l.setter('size'))

        t = TextInput( id = 'inputvalue',
                        font_size = 13,
                        pos_hint =  {'top': 1},
                        size_hint_y =  None,
                        height =  25,
                        cursor_width = '7sp',
                        cursor_color = (0.6, 0.56, 0.56, 1),
                        background_color = (0, 0, 0, 0),
                        foreground_color = (1, 1, 1, 1),
                        multiline = False)
        self.ids.stackid.add_widget(l)
        self.ids.stackid.add_widget(t)
        t.focus = True
        t.bind(on_text_validate = self.runCommand)

    def addWrongInput(self, displayText):
        l = Label( id = 'wrong',
                    text = "  [color=#9B9191][i][b]"+displayText+"[/b][/i][/color]",
                    padding_y = 2,
                    pos_hint =  {'top': 1},
                    font_size =  13,
                    size_hint_y = None,
                    markup = True)
        l.bind(width=lambda s, w:
                   s.setter('text_size')(s, (w, None)))
        l.bind(texture_size=l.setter('size'))
        self.ids.stackid.add_widget(l)
        self.addNew()

    def addResults(self,textval):
        l = Label( id = 'result',
                    text = textval,
                    padding_y = 2,
                    pos_hint =  {'top': 1},
                    font_size =  13,
                    size_hint_y = None,
                    markup = True)
        l.bind(width=lambda s, w:
                   s.setter('text_size')(s, (w, None)))
        l.bind(texture_size=l.setter('size'))
        self.ids.stackid.add_widget(l)

    def runCommand(self,val):
        global base_commands
        global links
        global listed
        global listofsubmissions
        global countlist
        val.readonly = True
        val.foreground_color = (0.2, 0.8, 0.2, 1)
        command = val.text.split()
        if len(command)>0:

            if command[0] not in base_commands:
                self.addWrongInput("Command Not Found")

            elif command[0] == 'cls':
                self.ids.stackid.clear_widgets()
                del links[:]
                del listofsubmissions[:]
                listed = False
                countlist = 0
                self.addNew()

            elif command[0] == 'ls':
                del listofsubmissions[:]
                submissions = reddit.front.hot(limit = 100)

                for listvals in submissions:
                    listofsubmissions.append(listvals)

                if len(command) == 1:
                    del links[:]
                    for i in range(0,len(listofsubmissions)-90):
                        self.addResults("  [b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubmissions[i].title)
                        self.addResults("  [color=#9B9191][i]("+listofsubmissions[i].url+")[/color][/i]")
                        self.addResults("  [color=#9B9191][i]"+str(listofsubmissions[i].ups)+" Upvotes with "+str(listofsubmissions[i].num_comments)+" Comments[/color][/i]")
                        links.append(listofsubmissions[i].url)
                        # pprint.pprint(vars(listvals))
                    listed = True
                    countlist = 10
                    self.addResults("  [b][color=#9B9191]{ [/color][color=#cccc00]next[/color][color=#9B9191] }[/color][/b]")
                    self.addNew()

                elif command[1] == 'next':
                    if listed == True and countlist<100:
                        for i in range(countlist,(len(listofsubmissions)-90+countlist)):
                            self.addResults("  [b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubmissions[i].title)
                            self.addResults("  [color=#9B9191][i]("+listofsubmissions[i].url+")[/color][/i]")
                            self.addResults("  [color=#9B9191][i]"+str(listofsubmissions[i].ups)+" Upvotes with "+str(listofsubmissions[i].num_comments)+" Comments[/color][/i]")
                            links.append(listofsubmissions[i].url)
                        countlist = countlist + 10
                        if countlist!=100:
                            self.addResults("  [b][color=#9B9191]{ [/color][color=#cccc00]next | previous[/color][color=#9B9191] }[/color][/b]")
                        else:
                            self.addResults("  [b][color=#9B9191]{ [/color][color=#cccc00]previous[/color][color=#9B9191] }[/color][/b]")
                        self.addNew()
                    else:
                        self.addWrongInput("No More Entries Available")

                elif command[1] == 'previous':
                    if listed == True and countlist>10:
                        countlist = countlist-10
                        for i in range(countlist-10,countlist):
                            self.addResults("  [b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubmissions[i].title)
                            self.addResults("  [color=#9B9191][i]("+listofsubmissions[i].url+")[/color][/i]")
                            self.addResults("  [color=#9B9191][i]"+str(listofsubmissions[i].ups)+" Upvotes with "+str(listofsubmissions[i].num_comments)+" Comments[/color][/i]")
                            links.append(listofsubmissions[i].url)
                        if countlist>10:
                            self.addResults("  [b][color=#9B9191]{ [/color][color=#cccc00]next | previous[/color][color=#9B9191] }[/color][/b]")
                        else:
                            self.addResults("  [b][color=#9B9191]{ [/color][color=#cccc00]next[/color][color=#9B9191] }[/color][/b]")
                        self.addNew()
                    else:
                        self.addWrongInput("No More Entries Available")

                else:
                    self.addWrongInput("Command Not Found")


            elif command[0] == 'view':
                if listed == True:
                    if len(command)>1:
                        if command[1].isdigit():
                            if int(command[1])<len(links) and int(command[1])>=0:
                                webbrowser.open(links[int(command[1])])
                                self.addNew()
                            else:
                                self.addWrongInput("No Such Index")
                        else:
                            self.addWrongInput("Enter an Index")
                    else:
                        self.addWrongInput("Command Not Found")
                else:
                    self.addWrongInput("Nothing to View")
        else:
            self.addNew()

    def __init__(self, **kwargs):
        super(ScrollableLabel, self).__init__(**kwargs)
        self.stackid.size_hint_y = None
        self.stackid.bind(minimum_height=self.stackid.setter('height'))

class ShellForRedditApp(App):
	def build(self):
		return ScrollableLabel()


if __name__ == "__main__":
	ShellForRedditApp().run()
