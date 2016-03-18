
import kivy
from kivy.app import App
from kivy.uix.listview import ListView, ListItemLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
import rethinkdb
from kivy.properties import ListProperty, StringProperty
from kivy.adapters.listadapter import ListAdapter
import webbrowser

from kivy.clock import Clock

class LobsterListItem(BoxLayout):
    title = StringProperty()
    link = StringProperty()
    timestamp = StringProperty()
    def __init__(self,*args,**kwargs):
        self.title = kwargs['title'] if 'title' in kwargs else '???' 
        self.link = kwargs['link'] if 'link' in kwargs else '' 
        self.timestamp = kwargs['timestamp'] if 'timestamp' in kwargs else "???? ?? ?? ??:?? : " 
        del kwargs['title']
        del kwargs['link']
        del kwargs['timestamp']
        if 'orientation' in kwargs:
            if kwargs['orientation'] == 'vertical':
                print("fuck you, it's horizontal")
        kwargs['orientation'] = 'horizontal'

        title = Label(text=self.title,valign='top', size_hint=(.7, 1))
        timestamp = Label(text=self.timestamp,valign='top',halign='right', size_hint=(.3, 1))
        kwargs['height']=70
        super(LobsterListItem,self).__init__(*args,**kwargs)
        self.add_widget(timestamp)
        self.add_widget(title)
        Clock.schedule_interval(self.resetTextSizeTest, .1)# omg this is the worst solution, I can't believe I'm doing this even temporarily, ulg.
    def resetTextSizeTest(self, wut):
        self.children[0].text_size=self.children[0].size
        self.children[1].text_size=self.children[1].size


    def on_touch_up(self,touch):
        if self.collide_point(*touch.pos):
            webbrowser.get('firefox').open_new_tab(self.link)
            print("A silly monkey says: {}".format(self.link))

class LobsterList(ListView):
    def __init__(self, *args, **kwargs):
        #connect to db and get data
        conn = rethinkdb.connect(host='localhost',port=28018)
        db = rethinkdb.db('lobsters')
        table = db.table('feeditems')
        posts = table.order_by(rethinkdb.desc('updated')).run(conn)
        #convert data for presentation
        def args_converter(row_index,text):
            if 'updated_parsed' in text.keys():
                updated = '{:0>2} {:0>2} {:0>2} {:0>2}:{:0>2} : '.format(*text['updated_parsed'][:5])
            else:
                updated = "???? ?? ?? ??:??: "
            return {'title': text['title'],
                    'link':text['link'],
                    'timestamp':updated,
                    'size_hint_y': None,
                    'height': 50,#len(text)/3+20,
                    'valign':'middle',
                    'text_size':(650,50)}#len(text)/3+10)}
        list_adapter = ListAdapter(data=posts,
            args_converter=args_converter,
            cls=LobsterListItem
                )
        #put data into scrollable list
        super(LobsterList, self).__init__(
                adapter=list_adapter)

class LobsterApp(App):
    def build(self):
        lisst = LobsterList()
        return lisst

if __name__=="__main__":
    LobsterApp().run()

