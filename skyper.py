from skpy import Skype
import properties

skype = Skype(properties.chat_bot_login, properties.chat_bot_password)

def sendMessage(message):
    chat = skype.chats.chat(properties.chat_id)
    chat.sendMsg(message)
