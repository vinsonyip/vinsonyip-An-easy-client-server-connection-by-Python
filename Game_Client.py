from socket import *
import sys

def func_auth(socket):
    res = "1002"
    while res.split(" ")[0] == "1002":
        acc = input("Please input your user name: ")
        pwd = input("Please input your password: ")
        tmpstr = "/login " + acc + " " + pwd
        socket.send(tmpstr.encode())
        res = socket.recv(1024).decode()
        print(res)

def func_list(socket):
    socket.send("/list".encode())
    res = socket.recv(1024).decode()
    print(res)
    
    
def func_enter(socket,cmd):
    socket.send(cmd.encode())
    res = socket.recv(1024).decode()
    if res == "3011 Wait":
        print(res)
        while True:
            res = socket.recv(1024).decode()
            if res.split(" ")[0] == "3012":
                #print(res)
                guess = input(res+"\n")
                socket.send(guess.encode())
                win_lose = socket.recv(1024).decode()
                while win_lose == "4002 Unrecognized message":
                    guess = input(win_lose+"\n")
                    socket.send(guess.encode())
                    win_lose = socket.recv(1024).decode()
                print(win_lose)
                break
    else:
        if res.split(" ")[0] == "3012":
            guess = input(res+"\n")
            socket.send(guess.encode())
            win_lose = socket.recv(1024).decode()
            while win_lose == "4002 Unrecognized message":
                guess = input(win_lose+"\n")
                socket.send(guess.encode())
                win_lose = socket.recv(1024).decode()
            print(win_lose)
        else:
            print(res)

        
if __name__ == "__main__":
    socket = socket(AF_INET,SOCK_STREAM)
    try:
        socket.connect(("localhost",20000))
    except error as err:
        print("Connection error: ",err)
        sys.exit(1)
        
    func_auth(socket)
    #print("\nYou are in the Game Hall now!")
    while True:
        cmd = input('')
        if cmd == "/list":
            func_list(socket)
        elif cmd.split(" ")[0] == "/enter" and len(cmd.split(" "))==2:
            func_enter(socket,cmd)
            #print("\nYou are in the Game Hall now!")
        elif cmd == "/exit":
            socket.send(cmd.encode());
            rtn_msg = socket.recv(1024).decode()
            print(rtn_msg+"\nClient ends")
            break;
        else:
            socket.send(cmd.encode());
            rtn_msg = socket.recv(1024).decode()
            print(rtn_msg)

    socket.close()


