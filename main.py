
import kivy
from kivy.app import App
from kivy.uix.listview import ListView, ListItemLabel
from kivy.uix.widget import Widget
import rethinkdb
from kivy.properties import ListProperty
from kivy.adapters.listadapter import ListAdapter

class LobsterListItem(ListItemLabel):
   #def __init__(self,*args,**kwargs):
   #    if not 'halign' in kwargs:
   #        kwargs['halign']='left'
   #    kwargs['text_size']=(500,20)
   #    super(BetterLIL,self).__init__(*args,**kwargs)
    def on_touch_up(self,touch):
        if self.collide_point(*touch.pos):
            print("A silly monkey says: {}".format(self.text))

class LobsterList(ListView):
    def __init__(self, *args, **kwargs):
        #connect to db and get data
        conn = rethinkdb.connect(host='localhost',port=28018)
        db = rethinkdb.db('lobsters')
        table = db.table('feeditems')
        posts = table.order_by(rethinkdb.desc('updated')).run(conn)
        post_titles = [post['title'] for post in posts]
#       posts = [post['title'] for post in \
#                   rethinkdb.db('lobsters').table('feeditems').get_all().order_by(rethinkdb.desc('date')).run(conn) \
#                       ]
        #put data into scrollable list
        def args_converter(row_index,text):
            #text = text.rstrip()
            if 'updated_parsed' in text.keys():
                updated = '{:0>2} {:0>2} {:0>2} {:0>2}:{:0>2}: '.format(*text['updated_parsed'][:5])
            else:
                updated = "???? ?? ?? ??:??: "
            return {'text': updated+": "+text['title'],
                'size_hint_y': None,
                'height': 50,#len(text)/3+20,
                'valign':'middle',
                'text_size':(650,50)}#len(text)/3+10)}
        list_adapter = ListAdapter(data=posts,#_titles,
            args_converter=args_converter,
            cls=LobsterListItem
                )
        super(LobsterList, self).__init__(
                adapter=list_adapter)

class LobsterApp(App):
    def build(self):
        lisst = LobsterList()
        return lisst

if __name__=="__main__":
    LobsterApp().run()

