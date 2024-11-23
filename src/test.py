import abc

class Base(abc.ABC):
    def __init__(self):
        self.activated = False
        
    @abc.abstractmethod
    def description(self):
        raise NotImplementedError
    
    
class RedBase(Base):
    def __init__(self):
        super().__init__()
        
    def description(self):
        return 'this is the red waypoint analog'
    
if __name__ == '__main__':
    check_item = RedBase()
    print(issubclass(type(check_item), abc.ABC))
    print(isinstance(check_item, Base))