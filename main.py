
import kivy
from kivy.app import App
from kivy.uix.listview import ListView, ListItemLabel
from kivy.uix.widget import Widget
import rethinkdb
from kivy.properties import ListProperty
from kivy.adapters.listadapter import ListAdapter

class BetterLIL(ListItemLabel):
    def __init__(self,*args,**kwargs):
        if not 'halign' in kwargs:
            kwargs['halign']='left'
        kwargs['text_size']=(500,20)
        super(BetterLIL,self).__init__(*args,**kwargs)

class LobsterList(ListView):
    def __init__(self, *args, **kwargs):
        #connect to db and get data
        conn = rethinkdb.connect(host='localhost',port=28018)
        posts = [post['title'] for post in \
                    rethinkdb.db('lobsters').table('feeditems').run(conn) \
                        ]
        #put data into scrollable list
        def args_converter(row_index,text):
            if len(text) > 70:
                text = text[:67]+"..."
            return {'text': text,
                'size_hint_y': None,
                'height': 25,
                'text_size':(600,20)}
        list_adapter = ListAdapter(data=posts,
            args_converter=args_converter,
            cls=ListItemLabel
                )
        super(LobsterList, self).__init__(
                adapter=list_adapter)

class LobsterApp(App):
    def build(self):
        lisst = LobsterList()
        return lisst

if __name__=="__main__":
    LobsterApp().run()

