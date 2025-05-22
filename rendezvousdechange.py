import threading
from typing import TypeVar, Generic, Any

E = TypeVar('E')
T = TypeVar('T')

class RendezvousDEchange(Generic[E,T]):
    def __init__(self):
        self.mutex = threading.Lock()
        self.condition = threading.Condition(self.mutex)
        self.first_arrived = False
        self.first_value = None
        self.second_value = None

    def echanger(self, value: E) -> T:
        with self.condition:
            if not self.first_arrived:
                self.first_value = value
                self.first_arrived = True
                self.condition.wait()
                result = self.second_value

                self.first_arrived = False
                self.first_value = None
                self.second_value = None

                self.condition.notify()
                return result
            else:
                self.second_value = value
                result = self.first_value
                self.condition.notify()
                self.condition.wait()
                return result
    