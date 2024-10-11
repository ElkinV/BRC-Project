from abc import ABC, abstractmethod


class IDBConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def executeQuery(self, query):
        pass
