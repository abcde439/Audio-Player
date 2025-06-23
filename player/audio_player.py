from abc import ABC, abstractmethod
class AudioPlayer(ABC):
    @abstractmethod
    def play(self, path): pass
    
    @abstractmethod
    def pause(self): pass
    
    @abstractmethod
    def resume(self): pass
    
    @abstractmethod
    def stop(self): pass
