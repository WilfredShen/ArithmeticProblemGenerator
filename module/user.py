class User:

    def __init__(self, usertype, username, password):
        self.__type = usertype
        self.__username = username
        self.__password = password

    def GetUsername(self):
        return self.__username
    
    def setType(self, usertype):
        self.__type = usertype

    def Authenticate(self, username, password):
        if self.__username == username and self.__password == password:
            return self.__type
        return None