import socket
import re
import regexCollection

class Message:
    def __init__(self, raw, user, command, params, message):
        self.raw = raw
        self.user = user
        self.command = command
        self.params = params
        self.message = message

    def __str__(self):
        return f"{self.user} {self.command} {self.params} {self.message}"

    def __bool__(self):
        if None in (self.user, self.command, self.params, self.message):
            return False
        else: return True
    
    @classmethod
    def parse(cls, data):
        mainMatch = regexCollection.mainRegex.match(data)
        if mainMatch:
            prefixMatch = regexCollection.prefixRegex.match(mainMatch.group('prefix'))
            
            command = mainMatch.group('command')
            params = mainMatch.group('params')
            message = mainMatch.group('message')

            user = None
            if prefixMatch:
                user = prefixMatch.group('user')
            return cls(data, user, command, params, message)
        else:
            return cls(data, None, None, None, None)
    

class TwitchConnector:
    def __init__(self, user, oauthToken):
        self.user = user
        self.oauthToken = oauthToken
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnected = False

    def isLoginSuccessful(self):
        sockdata = self.socket.recv(1024).decode("utf-8")
        if not re.match(r"^:(tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$", sockdata):
            return True
        else: return False

    def connect(self):
        print("Connecting to irc.twitch.tv...")
        try:
            self.socket.connect(("irc.twitch.tv", 6667))
        except Exception as e:
            print("Failed to connect to server")
            raise e
        print("Connected to irc.twitch.tv")
        print("Logging in...")
        self.socket.send(f"USER {self.user}\r\n".encode("utf-8"))
        self.socket.send(f"PASS {self.oauthToken}\r\n".encode("utf-8"))
        self.socket.send(f"NICK {self.user}\r\n".encode("utf-8"))
        if self.isLoginSuccessful():
            print("Login successfull")
            self.isConnected = True
        else:
            print("Login failed")
            raise Exception("Login failed")

    def joinChannel(self, channel):
        if self.isConnected:
            self.socket.send(f"JOIN {channel}\r\n".encode("utf-8"))
        else:
            raise Exception("The client is not connected")

    def getMessages(self):
        if self.isConnected:
            data = self.socket.recv(1024).decode("utf-8")
            if data.startswith("PING :tmi.twitch.tv"):
                self.socket.send("PONG :tmi.twitch.tv".encode("utf-8"))
            else:
                message = Message.parse(data)
                return message
        else:
            raise Exception("The client is not connected")