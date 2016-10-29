import Skype4Py

skype = Skype4Py.Skype()
skype.Attach()

def sendMessage(message):
    chat = skype.FindChatUsingBlob('ZM_jy6lt7FtGVGlsmkBPhisEaOGaaooqC7xiWqQQC373QSap65IeFDHwejRs3M5jlRjEKMA2VrDfEOT6wCKbLg')
    chat.SendMessage(message)
