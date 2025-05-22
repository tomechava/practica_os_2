from threading import Thread
from queue import Queue
from typing import Generic, TypeVar

E = TypeVar('E')

class GenProdCons(Generic[E]):
    
    def __init__(self, size: int = 10):
        #Revisar que size si sea un int
        if isinstance(size, int):
            self.size = size
        else:
            raise ValueError("El tamaño debe ser un entero")
        
        if size <= 0:
            raise ValueError("El tamaño del buffer debe ser mayor que 0")
        
        
        #Creamos cola FIFO para almacenar los elementos
        self.queue = Queue(maxsize=size)
        
        #Variable para controlar el estado de la cola
        self.disabled = False
        
    def put(self, e: E):
        self.queue.put(e)        
    
    def get(self) -> E:
        return self.queue.get()
    
    def __len__(self):
        return self.queue.qsize()