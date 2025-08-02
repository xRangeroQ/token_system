# --| LIBRARIES |--
import socket
import threading
import uuid
import secrets
import json
import time
import os
import sys
import sqlite3 as sql


# --| VARIABLES |--

    # ----| GVARIABLES |----
KeyFileName="TheKey.key"
TheKey=b"xRangeroQ"
DatabaseName="Database.db"
JSONConfigFileName="config.json"
JSONConfigFileContent={"_Config": {"_IP": "0.0.0.0", "_TCPPORT": 8080, "_UDPPORT": 8081, "_Debug": True, "_Debug-Level": 4}}


    # ----| COLOR CODES |----
Clear="\033[0m"
Black="\033[30m"
LightRed="\033[31m"
Green="\033[32m"
Yellow="\033[33m"
Blue="\033[34m"
Purple="\033[35m"
DarkRed="\033[91m"


    # ----| POINTERS |----
Successful=f"{Green}[SUCCESS]{Clear}"
Information=f"{Blue}[INFO]{Clear}"
Warn=f"{Yellow}[WARN]{Clear}"
Error=f"{DarkRed}[ERROR]{Clear}"
FatalError=f"{Black}[FATAL]{Clear}"
LoggingIndex=[Successful, Information, Warn, Error, FatalError]



# --| FUNCTIONS |--

    # ----| KEY SYSTEM |----
def GetKey():
    if not os.path.exists(KeyFileName):
        open(KeyFileName, "w").close()
        Debug("Key file created!", 1)
        sys.exit()

    else:
        Key=open(KeyFileName, "r").read()
        if bytes(Key.encode())!=TheKey:
            Debug("Wrong Key!", 2)
            sys.exit()
        Debug("Correct Key!", 0)



    # ----| LOGGING |----
def Debug(Message, Debug_Level):
    if not Debug_Level>=0 and not Debug_Level<=4:
        Debug(f"Debug Level is invalid!\n0 > {LoggingIndex[0]}\n1 > {LoggingIndex[1]}\n2 > {LoggingIndex[2]}\n3 > {LoggingIndex[3]}\n4 > {LoggingIndex[4]}", 4)
        sys.exit()

    try:
        if Debug_Level<=DebugLevel and DebugStatus:
            print(f"{LoggingIndex[Debug_Level]} {Message}")

    except (NameError, json.JSONDecodeError) as e:
        print(f"{LoggingIndex[2]} A error occurred while debugging! Default config settings loaded.")
        sys.exit()
        


    # ----| GET JSON DATA |----
def GetJSONConfig():
    try:
        with open(JSONConfigFileName, "r") as JSON:
            global JsonData, DebugStatus, DebugLevel, IP, TCPPORT, UDPPORT
            # -- JSON Vars

            JsonData=json.load(JSON)
            JsonData=JsonData["_Config"]
            IP=JsonData["_IP"]
            TCPPORT=JsonData["_TCPPORT"]
            UDPPORT=JsonData["_UDPPORT"]
            DebugStatus=JsonData["_Debug"]
            DebugLevel=JsonData["_Debug-Level"]

            # -- Control Debug Level
            if not (0<=DebugLevel<=4):
                Debug(f"Debug Level is invalid!\n\n0 > {LoggingIndex[0]}\n1 > {LoggingIndex[1]}\n2 > {LoggingIndex[2]}\n3 > {LoggingIndex[3]}\n4 > {LoggingIndex[4]}", 4)
                sys.exit()

            print(f"{LoggingIndex[0]} Config file successfully loaded!")
        
    except (FileNotFoundError, FileExistsError):
        with open(JSONConfigFileName, "w") as JSON:
            json.dump(JSONConfigFileContent, JSON, indent=4, ensure_ascii=False)
        print(f"{LoggingIndex[2]} Config file not found! Default settings loaded.")
        GetJSONConfig()
    
    except (json.JSONDecodeError, KeyError):
        with open(JSONConfigFileName, "w") as JSON:
            json.dump(JSONConfigFileContent, JSON, indent=4, ensure_ascii=False)
        print(f"{LoggingIndex[2]} Failed to load config file! Default settings loaded.")
        GetJSONConfig()



    # ----| SQL |----
def ConnectDB():
    global db, cursor
    try:
        db=sql.connect(DatabaseName, check_same_thread=False)
        Debug("Connected to database!", 1)
        cursor=db.cursor()
        Debug("Created cursor!", 1)
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                        UUID VARCHAR(48) NOT NULL PRIMARY KEY,
                        IP VARCHAR(32) NOT NULL,
                        PORT INTEGER NOT NULL
                        )""")
        Debug("Users table was created if it did not exist!", 1)
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS Tokens(
                        UUID VARCHAR(48) UNIQUE NOT NULL,
                        TOKEN VARCHAR(255) NOT NULL,
                        FOREIGN KEY (UUID) REFERENCES Users(UUID)
                        )""")
        Debug("Tokens table was created if it does not exist!", 1)

        db.commit()

    except Exception:
        Debug("A critical error occurred while performing database operations!", 4)
        sys.exit()



    # ----| SOCKET |----

        # ----| SOCKET TCP |----
def ServerTCP():
    global servertcp
    try:
        servertcp=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Debug("TCP Socket created successfully!", 0)
        servertcp.bind((IP, TCPPORT))
        Debug(f"The TCP socket was successfully associated with the specified {IP}:{TCPPORT}!", 0)
        servertcp.listen()
        Debug(f"Server listening...", 0)
    
    except Exception:
        Debug("A critical error occurred while performing TCP Socket operations!", 4)


def GetConnectionsTCP(servertcp):
    connection, address=servertcp.accept()

    data=connection.recv(4096)

    DbContent=cursor.execute("""SELECT Tokens.TOKEN FROM Tokens INNER JOIN Users ON Tokens.UUID = Users.UUID WHERE IP = ?""", (address[0], ))

    if data.decode("utf-8")!=DbContent.fetchone()[0]:
        connection.send(b'REDDEDILDI')
        connection.close()
    
    else:
        connection.send(b'ONAYLANDI')
        connection.close()



        # ----| SOCKET UDP |----
def ServerUDP():
    try:
        serverudp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Debug("UDP Socket created successfully!", 0)
        serverudp.bind((IP, UDPPORT))
        Debug(f"The UDP socket was successfully associated with the specified {IP}:{UDPPORT}!", 0)

        UDPThread=threading.Thread(target=GetConnectionsUDP, args=(serverudp, ))
        UDPThread.start()
        UDPThread.join()
    
    except Exception:
        Debug("A critical error occurred while performing UDP Socket operations!", 4)


def GetConnectionsUDP(serverudp):
    while True:
        try:
            data, address=serverudp.recvfrom(1024)
            Debug(f"Data arrived from {address}!", 1)

            serverudp.sendto(b'SERVER:GETADDRESS', address)
            Debug(f"Data throwed at {address}!", 1)

            TCPThreading=threading.Thread(target=GetConnectionsTCP, args=(servertcp, ), daemon=True)
            TCPThreading.start()
            Debug("Thread created!", 1)
        
        except Exception:
            Debug("A critical error was encountered while creating a UDP Data transfer and Thread!", 4)
            sys.exit()

        DbContent=cursor.execute("""SELECT 1 FROM Users WHERE IP = ?""", (address[0], ))
        Control=DbContent.fetchone() is not None
        
        if Control:
            Debug("No action taken because Client IP is registered in database!", 1)

        else:
            newUUID=str(uuid.uuid4())
            newTOKEN=secrets.token_hex(32)
            cursor.execute("""INSERT INTO Users(UUID, IP, PORT) VALUES(?, ?, ?)""", (newUUID, address[0], address[1]))
            cursor.execute("""INSERT INTO Tokens(UUID, TOKEN) VALUES(?, ?)""", (newUUID, newTOKEN))
            db.commit()
            Debug("New client added to database!", 0)



# --| MAIN CODE |--
def Start():
    GetJSONConfig()
    GetKey()
    ConnectDB()
    
    ServerTCPThreading=threading.Thread(target=ServerTCP, daemon=True)
    ServerUDPThreading=threading.Thread(target=ServerUDP, daemon=True)

    ServerTCPThreading.start()
    time.sleep(.1)
    ServerUDPThreading.start()
    
    ServerTCPThreading.join()
    ServerUDPThreading.join()


# --| Start Script |--
if __name__=="__main__":
    Start()
