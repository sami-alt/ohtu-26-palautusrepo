#tehdään alussa importti

from logger import logger
from summa import summa
from erotus import erotus

logger("totetus alkaa") #tätä muutettiin

x = input("Luku 1: ")
y = input("Luku 2: ")
print(f"{summa(x, y)}")
print(f"{erotus(x, y)}")


logger("lopetetaan")
