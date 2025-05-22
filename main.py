from threading import Thread
import importlib
import os

from pysync.genprodcons import GenProdCons
from pysync.rendezvousdechange import RendezvousDEchange

expected_module = 'PRODCONSMODULE'
default_module = 'pysync'

if expected_module in os.environ:
    prod_cons_mdl = os.environ[expected_module]
else:
    prod_cons_mdl = 'pysync'

prod_cons_imprt = importlib.__import__(prod_cons_mdl, globals(), locals(), [], 0)

def producer(prod_cons):
    i = 0
    while True:
        prod_cons.put(i)
        i = i + 1

def consumer(prod_cons, rendezvous, number_mod):
    while True:
        value = prod_cons.get()
        exchanged = rendezvous.echanger(value)
        print(f"Consumidor recibió: {value}, intercambiado por: {exchanged}, módulo: {number_mod}")

if __name__ == "__main__":
    prod_cons_1 = GenProdCons()
    prod_cons_2 = GenProdCons()
    rendezvous  = RendezvousDEchange()

    thr_prod_1 = Thread(target=producer, args=(prod_cons_1,))
    thr_prod_2 = Thread(target=producer, args=(prod_cons_2,))
    thr_cons_1 = Thread(target=consumer, args=(prod_cons_1, rendezvous, 5000))
    thr_cons_2 = Thread(target=consumer, args=(prod_cons_2, rendezvous, 3000))

    thr_prod_1.start()
    thr_prod_2.start()
    thr_cons_1.start()
    thr_cons_2.start()
    
    thr_prod_1.join()
    thr_prod_2.join()
    thr_cons_1.join()
    thr_cons_2.join()
