

class Message():
    '''
        Une message qui est renvoyé à l'utilisateur.
    '''

    def __init__(self, channel, content):
        self.__channel = channel
        self.__content = content
    
    @property
    def channel(self):
        return self.__channel
    
    @property
    def content(self):
        return self.__content

class ExceptionToUser(Exception):
    '''
        Une classe qui gère les exceptions qui sont envoyées à des utilisateurs.
    '''

    def __init__(self, string_output, message_to_user):
        self.__string_output = string_output
        self.__message_to_user = message_to_user

    @property
    def stringOutput(self):
        return self.__string_output
    
    @property
    def messageToUser(self):
        return self.__message_to_user

    
