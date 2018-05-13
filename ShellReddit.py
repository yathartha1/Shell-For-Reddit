import kivy
kivy.require("1.10.0")
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

LabelBase.register(name = "Capture", fn_regular = "Capture_it_2.ttf")

class ScrollableLabel(BoxLayout):
    stackid=ObjectProperty(None)
    idvalue = StringProperty("  [color=#33cc33][b]guest@reddit:$[/b][/color]")

    def addNew(self, label_id):
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

    def runCommand(self,val):
        label_id = self.ids.labelid
        val.readonly = True
        val.foreground_color = (0.2, 0.8, 0.2, 1)
        self.addNew(label_id)

    def __init__(self, **kwargs):
        super(ScrollableLabel, self).__init__(**kwargs)
        self.stackid.size_hint_y = None
        self.stackid.bind(minimum_height=self.stackid.setter('height'))

class ShellForRedditApp(App):
	def build(self):
		return ScrollableLabel()


if __name__ == "__main__":
	ShellForRedditApp().run()
