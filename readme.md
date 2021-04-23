# COMP3234 Assignment 1

-------------------------

## How to use

1. You can find the username and password in `UserInfo.txt`

## Server side implementation

I use mainly 3 dictionaries to implement the whole program

1. __acc_dict__</br>
This dictionary is used for storing user name and corresponding password, which the dictionary is preloaded the whole `UserInfo.txt` file, in order to verify user's identity

2. __room_dict__</br>
This dictionary is used for storing the room number and the client connection sockets, where `key is room number, value is also a dictionary`, which the dictionary is storing`{client socket object : Boolean}`, the boolean is the user's choice in the game

3. __semdict__</br>
This dictionary is used for storing the `semaphore`, which I define semaphores to different room, in order to `resolve the deadlock`, when clients in the room access the same list or dictionary at the same time

Also, I define 4 functions throughout the program for server side implementation

1. __func_auth__</br>
This function contains the logic of authentication
2. __func_enter_game__</br>
This function contains the logic of the game,it execute when the game start
3. __func_enter__</br>
When user use `/enter` command, then this function will be run, and `func_enter_game` will be run within this function
4. __thrfunc__</br>
This function is a thread function, it used for each client when they connect to the server, it contains all logic of user's observable behaviors

I try not to use any of global variables throughout the project, because it could guarantee not variable miss use will happen.

## Client side implementation

### The function of client side is not going to process all the functions, because the server side will do all of the job

I define 3 functions throughout the program for client side implementation

1. __func_auth__</br>
This function contains the logic of authentication
2. __func_list__</br>
This function is going to send `/list` request to server and print out the response
3. __func_enter__</br>
This function will take care of users behavior inside after the request of `/enter` has been sent

It is noteworthy that we will use `main` function to deal with most of the users' command when they are in the Game Hall.
