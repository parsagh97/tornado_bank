import tornado.ioloop
import tornado.web
import tornado
import sqlite3
from sqlite3 import Error
import tornado.auth

class register(tornado.web.RequestHandler):
    def get(self):
        # self.render("templates/register.html", title="register")
        action = self.get_argument('act')
        name = self.get_argument('name')
        passwd = self.get_argument('passwd')
        conn = sqlite3.connect("user.db")
        c = conn.cursor()
        if action == 'reg':
            c.execute('select * from USER where name =?' ,(name,))
            i = 0
            for row in c.fetchall():
                i = i+1
            if i>0:
                self.write({'message':'false'})
            else:
                c.execute("insert into USER values (? ,? ,0)" ,(name ,passwd))
                conn.commit()
                self.write({'message':'true'})
        elif action == 'log':
            c.execute("select password from USER where name == ?" ,(name,)) 
            result = c.fetchone()  
            if str(passwd) == str(result[0]):
                self.write({'message':'true'})                
            else:
                self.write({'message':'false'})
        else:
            self.write({'message':'wronge command'})
    def post(self):
        pass
        
class panel(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/panel.html" ,title = "panel")
    def post(self):
        withd = self.get_argument('with_amount')
        user = self.get_argument('name')
        depo = self.get_argument('depo_amount')
        trans = self.get_argument('trans_amount')
        trans_to = self.get_argument('trans_to')
        if withd != "":
            self.redirect("http://localhost:8000/account?name={0}&act=with&amount={1}".format(user ,withd))
        elif depo != "":
            self.redirect("http://localhost:8000/account?name={0}&act=depo&amount={1}".format(user ,depo))
        elif trans_to != "":
            self.redirect("http://localhost:8000/account?name={0}&act=trans&amount={1}&rec={2}".format(user ,trans ,trans_to))
        else:
            self.wite("hello")

class account(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name')#account owner
        action = self.get_argument('act')#action withdrawl, deposit, transfer
        conn = sqlite3.connect("user.db")
        c = conn.cursor()
        if action == 'with':
            amount = self.get_argument('amount')#amount of money in action
            c.execute("select asset from USER where name=?" ,(name,))
            row = c.fetchall()
            if int(row[0][0])-int(amount) <0:
                response = {'message':'no_money'}
                self.write(response)
            else:
                c.execute("update USER set asset = asset - ? where name = ?" ,(amount ,name))
                conn.commit()
                response = {'message':'true'}
                self.write(response)
        elif action == 'depo':
            amount = self.get_argument('amount')#amount of money in action
            c.execute("update USER set asset = asset + ? where name = ?" ,(amount ,name))
            conn.commit()
            response = {'message':'true'}
            self.write(response)
        elif action == 'trans':
            amount = self.get_argument('amount')#amount of money in action
            rec = self.get_argument('rec')#if the action is trans then this is the name of the reciver
            c.execute("select asset from USER where name=?" ,(name,))
            row = c.fetchall()
            if int(row[0][0])-int(amount) <0:
                response = {'message':'no_money'}
                self.write(response)
            else:
                c.execute("select * from USER where name=?" ,(rec ,))
                i = 0
                for row in c.fetchall():
                    i = i + 1
                if i!=0:
                    c.execute("update USER set asset = asset - ? where name = ?" ,(amount ,name))
                    conn.commit()
                    c.execute("update USER set asset = asset + ? where name = ?" ,(amount ,rec))
                    conn.commit()
                    response = {'message':'true'}
                    self.write(response)
                else:
                    self.write({'message':'no reciever'})

        elif action == 'balance':
            c.execute("select asset from USER where name=?" ,(name,))
            row = c.fetchall()
            asset = row[0][0]
            self.write({'message':str(asset)})
        else:
            response = {'message':'bad request'}
            self.write(response)
        c.execute("select * from USER where name = ?" ,(name ,))
        for row in c.fetchall():
            print(row)     
   
    def post(self):
        pass
        
def main_app():
    return tornado.web.Application([
    (r"/reg", register,),
    (r"/account", account),
    (r"/panel" ,panel),
    ])
    
if __name__ == "__main__":
    
    app = main_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
