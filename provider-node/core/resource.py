from abc import ABC, abstractmethod

class Resource(ABC):
    
    @abstractmethod
    def consume(self):
        pass
    