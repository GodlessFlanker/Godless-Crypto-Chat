import socket
import threading

import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None

# // Godless_Developement_Presents //


#   //this command line we use in order to make it more functional
ip = input("Enter your Ip adress: ")
ip_2 = input("Enter your partner's IP adress: ")

choice = input("Do you want to host (1) or to connect (2): ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, 9999))
    server.listen()

#The other person should specify IP of you to connect
    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_2, 9999))
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
else:
    exit()


def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)


def receiving_messages(c):
    while True:
        
        print("Partner: " + rsa.decrypt(c.recv(1024), private_key).decode())

threading.Thread(target=sending_messages, args=(client, )).start()
threading.Thread(target=receiving_messages, args=(client, )).start()
