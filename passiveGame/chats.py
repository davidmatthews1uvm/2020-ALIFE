import pickle

from chat import CHAT

class CHATS:

    def __init__(self):

        self.chats = {}

    def Print(self):

        for chat in self.chats:

            self.chats[chat].Print()

    def Process_Chat(self):

        chat = CHAT()

        if chat.Is_Valid():

            self.Add_Chat(chat)
            
            self.Pickle()

        return chat

# -------------- Private methods ---------------

    def Add_Chat(self,chat):

        self.chats[chat.Get_Time()] = chat

    def Pickle(self):

        pickle.dump( self , open('data/chats.p','wb') )
