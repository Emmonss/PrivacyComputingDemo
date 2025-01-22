from abc import abstractmethod



class BaseSender:
    def __init__(self):
        self.role = 'sender'


    @abstractmethod
    def send(self, msg):
        pass

class BaseReceiver:
    def __init__(self):
        self.role = 'receiver'

    @abstractmethod
    def remote(self):
        pass