#Basic representation of a data provider


class dataProviderCore():
    def __init__(self, host_p):
        self.host = host_p
        """ init """
    def connection(self,request) -> None:
        """ connection """

    def getMetadata(self,request, type, id) -> None:
        """ metadata """

    def getElements(self,request) -> None:
        """ data elements """