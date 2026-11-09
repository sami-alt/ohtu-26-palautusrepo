#tehdään alussa importti

from logger import logger
from summa import summa
from erotus import erotus

logger("totetus alkaa") #tätä muutettiin

x = input("Luku 1: ")
y = input("Luku 2: ")
print(f"{x} + {y} = {summa(x, y)}")#muutos main
print(f"{x} - {y} = {erotus(x, y)}")#muutos main

#muutos
logger("lopetetaan")
print("goodbye")# lisätty bugi korjaus
