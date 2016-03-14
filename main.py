
import kivy
from kivy.app import App
from kivy.uix.listview import ListView, ListItemLabel
from kivy.uix.widget import Widget
import rethinkdb
from kivy.properties import ListProperty
from kivy.adapters.listadapter import ListAdapter

class BetterLIL(ListItemLabel):
    def __init__(self,*args,**kwargs):
        super(BetterLIL,self).__init__(*args,halign='left',**kwargs)

class LobsterList(ListView):
    def __init__(self, *args, **kwargs):
        conn = rethinkdb.connect(host='localhost',port=28018)
        posts = [post['title'] for post in \
                    rethinkdb.db('lobsters').table('feeditems').run(conn) \
                        ]
        list_adapter = ListAdapter(data=posts,
            cls=BetterLIL
                )
        super(LobsterList, self).__init__(
                item_strings=posts,adapter=list_adapter)
        print(self.__dict__)

class LobsterApp(App):
    def build(self):
        lisst = LobsterList()
        return lisst

#connect to db and get data
#put data into scrollable list

if __name__=="__main__":
    LobsterApp().run()

