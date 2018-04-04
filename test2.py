import requests
def register(name ,passwd):
    response = requests.get('http://localhost:8000/reg?act=reg&name={}&passwd={}'.format(name ,passwd))
    if response.json()['message'] == 'false':
        print("this user already exists\n")
    else:
        print("you've been registerd\n")
def login(name ,passwd):
    #request to l
    response = requests.get('http://localhost:8000/reg?act=log&name={}&passwd={}'.format(name ,passwd))
    if response.json()['message'] == 'false':
        print("wronge password\n")
    else:
        print("logged in\n")
        while(1):
            action = int(input("what do you want to do:\n1:balance\n2:deposit\n3:withdraw\n4:transfer\n"))
            if action==1:
                balance(name)
            elif action==2:
                amount = input("how much do you want to deposit?\n")
                depo(name ,amount)
            elif action==3:
                with_amount = input("how much do you want to withdraw?\n")
                withdraw(name ,with_amount)
            elif action==4:
                rec = input("who do you wish to transfer to?\n")
                trans_amount = input("how much do you want to transfer to?\n")
                transfer(name ,trans_amount ,rec)
            else:
                return

def withdraw(user ,amount):
    #withdraw money
    response = requests.get('http://localhost:8000/account?name={}&act=with&amount={}'.format(user ,amount))
    if response.json()['message'] == 'true':
        print("action done\n")
        balance(user)
    else:
        print("action stoped\n")
def depo(user ,amount):
    #depo some money
    response = requests.get('http://localhost:8000/account?name={}&act=depo&amount={}'.format(user ,amount))
    if response.json()['message'] == 'true':
        print("action done\n")
        balance(user)
    else:
        print("action stoped\n")
        
def transfer(user , amount ,reciever):
    #transfer moeny
    response = requests.get('http://localhost:8000/account?name={}&act=trans&amount={}&rec={}'.format(user ,amount ,reciever))
    if response.json()['message'] == 'false':
        print("reciever is wrong or the amount is more than what you have\n")
        balance(user)
    else:
        print("action is done\n")
def balance(user):
    respone = requests.get('http://localhost:8000/account?name={}&act=balance'.format(user))
    print("your balance is "+respone.json()['message']+"\n")


while(1):
    action = int(input("enter your action \n1:register\n2:login\n"))
    if action==1:
        name = str(input("enter a name:\n"))
        passwd = str(input("enter a password:\n"))
        register(name ,passwd)
    elif action == 2:
        name = str(input("enter your name:\n"))
        passwd = str(input("enter your password:\n"))
        login(name ,passwd)
