import kivy
import webbrowser
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

base_commands = ['cls','search','view','ls']
links = []
listed = False
listofsubmissions = []
listofcomments = []
listofsubreddits = []
countlist = 0
countcomments = 0
tempvar = 0
nextprevious = False
nextpreviousnormal = False
nextprevioussubreddits = False


################################################################################


class ScrollableLabel(BoxLayout):
    stackid=ObjectProperty(None)
    idvalue = StringProperty("[color=#33cc33][b]guest@reddit:$[/b][/color]")


################## Functions to generate new command lines #####################


    def addNew(self):
        l = Label( id = 'labelid',
                    text = "[color=#33cc33][b]guest@reddit:$[/b][/color]",
                    padding_y = 2,
                    padding_x = 10,
                    pos_hint =  {'top': 1},
                    font_size =  13,
                    size_hint_y = None,
                    markup = True)
        l.bind(width=lambda s, w:
                   s.setter('text_size')(s, (w, None)))
        l.bind(texture_size=l.setter('size'))

        t = TextInput( id = 'inputvalue',
                        font_size = 13,
                        padding_x = 10,
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
                    text = "[color=#9B9191][i][b]"+displayText+"[/b][/i][/color]",
                    padding_y = 2,
                    padding_x = 10,
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
                    padding_x = 10,
                    pos_hint =  {'top': 1},
                    font_size =  13,
                    size_hint_y = None,
                    markup = True)
        l.bind(width=lambda s, w:
                   s.setter('text_size')(s, (w, None)))
        l.bind(texture_size=l.setter('size'))
        self.ids.stackid.add_widget(l)


################## Functions to handle operations ##############################


    def runCommand(self,val):
        global base_commands
        global links
        global listed
        global listofsubmissions
        global countlist
        global listofcomments
        global nextprevious
        global nextpreviousnormal
        global nextprevioussubreddits
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
                del listofcomments[:]
                del listofsubreddits[:]
                listed = False
                nextprevious = False
                nextpreviousnormal = False
                nextprevioussubreddits = False
                countlist = 0
                self.addNew()

            elif command[0] == 'ls':
                del listofcomments[:]
                self.runlsCommand(command)

            elif command[0] == 'view':
                self.runviewCommand(command)

            elif command[0] == 'search':
                del listofcomments[:]
                self.runsearchCommand(command)
        else:
            self.addNew()

    def runlsCommand(self,command):
        global links
        global listed
        global listofsubmissions
        global countlist
        global listofsubreddits
        global nextprevious
        global nextpreviousnormal
        global nextprevioussubreddits
        temp = 0
        if len(command) == 1:
            nextpreviousnormal = False
            nextprevious = False
            nextprevioussubreddits = False
            temp = 0
            del links[:]
            del listofsubmissions[:]
            del listofsubreddits[:]
            submissions = reddit.front.hot(limit = 100)

            for listvals in submissions:
                listofsubmissions.append(listvals)

            for i in range(0,len(listofsubmissions)):
                if temp<10:
                    temp = temp + 1
                    self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubmissions[i].title)
                    self.addResults("[color=#9B9191][i]("+listofsubmissions[i].url+")[/color][/i]")
                    self.addResults("[color=#9B9191][i]"+str(listofsubmissions[i].ups)+" Upvotes with "+str(listofsubmissions[i].num_comments)+" Comments[/color][/i]")
                    links.append(listofsubmissions[i].url)
            listed = True
            countlist = temp
            if len(listofsubmissions) >= 10:
                self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]next[/color][color=#9B9191] }[/color][/b]")
                nextpreviousnormal = True
            self.addNew()

        elif command[1] == 'next' or command[1] == 'previous':
            if nextpreviousnormal == True:
                self.handleMoreList(command[1])
            else:
                self.addWrongInput("Nothing to Display")

        elif len(command) == 2 and command[1] != 'subreddits' and (command[1] != 'next' or command[1] != 'previous'):
            nextpreviousnormal = False
            nextprevious = False
            nextprevioussubreddits = False
            temp = 0
            del links[:]
            del listofsubmissions[:]
            del listofsubreddits[:]
            try:
                subreddit = reddit.subreddit(command[1])
                submissions = subreddit.hot(limit = 100)

                for listvals in submissions:
                    listofsubmissions.append(listvals)
            except:
                self.addWrongInput("Invalid Subreddit")
            else:
                for i in range(0,len(listofsubmissions)):
                    if temp<10:
                        temp = temp + 1
                        self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubmissions[i].title)
                        self.addResults("[color=#9B9191][i]("+listofsubmissions[i].url+")[/color][/i]")
                        self.addResults("[color=#9B9191][i]"+str(listofsubmissions[i].ups)+" Upvotes with "+str(listofsubmissions[i].num_comments)+" Comments[/color][/i]")
                        links.append(listofsubmissions[i].url)
                listed = True
                countlist = temp
                if len(listofsubmissions) >= 10:
                    self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]next[/color][color=#9B9191] }[/color][/b]")
                    nextprevious = True
                self.addNew()

        elif len(command) == 2 and command[1] == 'subreddits':
            nextpreviousnormal = False
            nextprevious = False
            nextprevioussubreddits = False
            temp = 0
            del links[:]
            del listofsubmissions[:]
            del listofsubreddits[:]
            subreddits = reddit.subreddits.popular(limit = 100)

            for listvals in subreddits:
                listofsubreddits.append(listvals)

            for i in range(0,len(listofsubreddits)):
                if temp<10:
                    temp = temp + 1
                    self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubreddits[i].display_name_prefixed+ " - "+listofsubreddits[i].title)
                    self.addResults("[color=#9B9191][i]("+listofsubreddits[i].url+")[/color][/i]")
                    self.addResults("[color=#9B9191][i]"+str(listofsubreddits[i].subscribers)+" subscribers[/color][/i]")
            listed = True
            countlist = temp
            if len(listofsubreddits) >= 10:
                self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]next[/color][color=#9B9191] }[/color][/b]")
                nextprevioussubreddits = True
            self.addNew()

        elif len(command) == 3:
            if (command[2] == 'next' or command[2] == 'previous') and command[1] != 'subreddits':
                if nextprevious == True:
                    self.handleMoreList(command[2])
                else:
                    self.addWrongInput("Nothing to Display")

            elif (command[2] == 'next' or command[2] == 'previous') and command[1] == 'subreddits':
                if nextprevioussubreddits == True:
                    self.handleMoreSubreddits(command[2])
                else:
                    self.addWrongInput("Nothing to Display")

            else:
                self.addWrongInput("Command Not Found")

        else:
            self.addWrongInput("Command Not Found")


    def handleMoreList(self,commandval):
        global links
        global listed
        global listofsubmissions
        global countlist
        global nextprevious
        global tempvar
        if commandval == 'next':
            temp = 0
            if listed == True and countlist<len(listofsubmissions):
                for i in range(countlist,len(listofsubmissions)):
                    if temp < 10:
                        temp = temp + 1
                        self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubmissions[i].title)
                        self.addResults("[color=#9B9191][i]("+listofsubmissions[i].url+")[/color][/i]")
                        self.addResults("[color=#9B9191][i]"+str(listofsubmissions[i].ups)+" Upvotes with "+str(listofsubmissions[i].num_comments)+" Comments[/color][/i]")
                        links.append(listofsubmissions[i].url)
                countlist = countlist + temp
                tempvar = temp
                if countlist != len(listofsubmissions):
                    self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]next | previous[/color][color=#9B9191] }[/color][/b]")
                    nextprevious = True
                else:
                    self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]previous[/color][color=#9B9191] }[/color][/b]")
                self.addNew()
            else:
                self.addWrongInput("No More Entries Available")

        elif commandval == 'previous':
            if listed == True and countlist>10:
                countlist = countlist-tempvar
                for i in range(countlist-10,countlist):
                    self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubmissions[i].title)
                    self.addResults("[color=#9B9191][i]("+listofsubmissions[i].url+")[/color][/i]")
                    self.addResults("[color=#9B9191][i]"+str(listofsubmissions[i].ups)+" Upvotes with "+str(listofsubmissions[i].num_comments)+" Comments[/color][/i]")
                    links.append(listofsubmissions[i].url)
                    tempvar = 10
                if countlist>10:
                    self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]next | previous[/color][color=#9B9191] }[/color][/b]")
                    nextprevious = True
                else:
                    self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]next[/color][color=#9B9191] }[/color][/b]")
                self.addNew()
            else:
                self.addWrongInput("No More Entries Available")

    def handleMoreSubreddits(self,commandval):
        global links
        global listed
        global listofsubreddits
        global countlist
        global nextprevious
        global tempvar
        if commandval == 'next':
            temp = 0
            if listed == True and countlist<len(listofsubreddits):
                for i in range(countlist,len(listofsubreddits)):
                    if temp < 10:
                        temp = temp + 1
                        self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubreddits[i].display_name_prefixed+ " - "+listofsubreddits[i].title)
                        self.addResults("[color=#9B9191][i]("+listofsubreddits[i].url+")[/color][/i]")
                        self.addResults("[color=#9B9191][i]"+str(listofsubreddits[i].subscribers)+" subscribers[/color][/i]")
                countlist = countlist + temp
                tempvar = temp
                if countlist != len(listofsubreddits):
                    self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]next | previous[/color][color=#9B9191] }[/color][/b]")
                    nextprevious = True
                else:
                    self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]previous[/color][color=#9B9191] }[/color][/b]")
                self.addNew()
            else:
                self.addWrongInput("No More Entries Available")

        elif commandval == 'previous':
            if listed == True and countlist>10:
                countlist = countlist-tempvar
                for i in range(countlist-10,countlist):
                    self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubreddits[i].display_name_prefixed+ " - "+listofsubreddits[i].title)
                    self.addResults("[color=#9B9191][i]("+listofsubreddits[i].url+")[/color][/i]")
                    self.addResults("[color=#9B9191][i]"+str(listofsubreddits[i].subscribers)+" subscribers[/color][/i]")
                    tempvar = 10
                if countlist>10:
                    self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]next | previous[/color][color=#9B9191] }[/color][/b]")
                    nextprevious = True
                else:
                    self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]next[/color][color=#9B9191] }[/color][/b]")
                self.addNew()
            else:
                self.addWrongInput("No More Entries Available")

    def runviewCommand(self,command):
        global links
        global listed
        global listofsubmissions
        global countlist
        global listofcomments
        global countcomments
        if listed == True and len(links) != 0:
            if len(command) == 2:
                if command[1].isdigit():
                    if int(command[1])<len(links) and int(command[1])>=0:
                        webbrowser.open(links[int(command[1])])
                        self.addNew()
                    else:
                        self.addWrongInput("No Such Index")
                else:
                    self.addWrongInput("Enter an Index")

            elif len(command) == 3:
                if command[1] == 'comments' and command[2].isdigit():
                    if int(command[2])<len(listofsubmissions) and int(command[2])>=0:
                        del listofcomments[:]
                        comments = listofsubmissions[int(command[2])].comments
                        for comment in comments:
                            listofcomments.append(comment)

                        if len(listofcomments)>=10:
                            for i in range(0,10):
                                self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofcomments[i].body)
                                self.addResults("[color=#9B9191][i]Posted By "+str(listofcomments[i].author)+"[/color][/i]")
                                self.addResults("[color=#9B9191][i]"+str(listofcomments[i].ups)+" Upvotes[/color][/i]")
                            self.addNew()
                            countcomments = 10
                        else:
                            for i in range(0,len(listofcomments)):
                                self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofcomments[i].body)
                                self.addResults("[color=#9B9191][i]Posted By "+str(listofcomments[i].author)+"[/color][/i]")
                                self.addResults("[color=#9B9191][i]"+str(listofcomments[i].ups)+" Upvotes[/color][/i]")
                            self.addNew()
                    else:
                        self.addWrongInput("No Such Index")

                elif command[1] == 'more' and command[2] == 'comments':
                    if len(listofcomments) != 0 and countcomments == 10:
                        self.handleMoreComments()
                    else:
                        self.addWrongInput("Nothing to View")
                else:
                    self.addWrongInput("Command Not Found")
            else:
                self.addWrongInput("Command Not Found")
        else:
            self.addWrongInput("Nothing to View")

    def handleMoreComments(self):
        global listofcomments
        global countcomments
        temp = 0
        if countcomments < len(listofcomments):
            for i in range(countcomments,len(listofcomments)):
                if (temp<10):
                    temp = temp + 1
                    self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofcomments[i].body)
                    self.addResults("[color=#9B9191][i]Posted By "+str(listofcomments[i].author)+"[/color][/i]")
                    self.addResults("[color=#9B9191][i]"+str(listofcomments[i].ups)+" Upvotes[/color][/i]")
            countcomments = countcomments + temp
            self.addNew()
        else:
            self.addWrongInput("No More Entries Available")

    def runsearchCommand(self,command):
        global links
        global listed
        global listofsubmissions
        global countlist
        global nextprevious
        global nextpreviousnormal
        global nextprevioussubreddits
        if len(command) == 2:
            nextpreviousnormal = False
            nextprevious = False
            nextprevioussubreddits = False
            temp = 0
            del links[:]
            del listofsubmissions[:]
            del listofsubreddits[:]
            try:
                searchs = reddit.subreddit('all').search(command[1],limit = 100)

                for listvals in searchs:
                    listofsubmissions.append(listvals)
            except:
                self.addWrongInput("Invalid Entry")
            else:
                for i in range(0,len(listofsubmissions)):
                    if temp<10:
                        temp = temp + 1
                        self.addResults("[b][color=#9B9191]{ [/color][color=#33cc33]"+str(i)+"[/color][color=#9B9191] }[/color][/b] "+listofsubmissions[i].title)
                        self.addResults("[color=#9B9191][i]("+listofsubmissions[i].url+")[/color][/i]")
                        self.addResults("[color=#9B9191][i]"+str(listofsubmissions[i].ups)+" Upvotes with "+str(listofsubmissions[i].num_comments)+" Comments[/color][/i]")
                        links.append(listofsubmissions[i].url)
                listed = True
                countlist = temp
                if len(listofsubmissions) >= 10:
                    self.addResults("[b][color=#9B9191]{ [/color][color=#cccc00]next[/color][color=#9B9191] }[/color][/b]")
                    nextpreviousnormal = True
                self.addNew()

        else:
            self.addWrongInput("Enter Something to Search")

    def __init__(self, **kwargs):
        super(ScrollableLabel, self).__init__(**kwargs)
        self.stackid.size_hint_y = None
        self.stackid.bind(minimum_height=self.stackid.setter('height'))


################################################################################


class ShellForRedditApp(App):
	def build(self):
		return ScrollableLabel()


if __name__ == "__main__":
	ShellForRedditApp().run()
