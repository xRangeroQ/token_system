import socket
import os
import secrets

token=""

clientudp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clientudp.sendto(token.encode("utf-8"), ("192.168.95.137", 8081))

data, address=clientudp.recvfrom(1024)
print(data, address)

clientudp.close()

clienttcp=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clienttcp.connect((address[0], address[1]-1))

clienttcp.send(token.encode("utf-8"))

data=clienttcp.recv(1024)

clienttcp.close()


if  data==b'ONAYLANDI':
    print("Geçiş Serbest")

elif data==b'REDDEDILDI':
    print("Geçiş Yapılamadı")

else:
    print("Crackli program kullanma.")
