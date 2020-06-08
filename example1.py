from TwitchConnector import TwitchConnector, Message
from TwitchCredentials import USER, OAUTH_TOKEN

tc = TwitchConnector(USER, OAUTH_TOKEN)
tc.connect()
tc.joinChannel("#izeroonei")
while True:
    message = tc.getMessages()
    if message:
        print(message)