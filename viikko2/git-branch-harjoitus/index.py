#tehdään alussa importti

from logger import logger
from summa import summa
from erotus import erotus

logger("aloitetaan")

x = input("Luku 1: ")
y = input("Luku 2: ")
print(f"Lukujen x{} ja {y} summa on {summa(x, y)}")
print(f"Lukujen {x} ja {y}} summa on {erotus(x, y)}")


logger("lopetetaan")
print("goodbye")# lisätty bugi korjaus
