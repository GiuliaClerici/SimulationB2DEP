# Simulation environment for the B2DEP experiments
# author = 'Giulia Clerici'

import random
import numpy as np
from armsMAB import Arms
from BanditRanker import banditRanker
from PiLow import  piLow


def main():
    horizon = 810000 # orizzonte
    k = 10 # numero di azioni
    armsSet = {}
    # armsSet = [Arms(mean=i / 10, delay=i - 1, gamma=0.5, state=0) for i in range(10, 0, -1)]
    # armsSet[9]._delay = 1
    armsSet = [Arms(mean=random.uniform(0, 1), delay=i+1, gamma=0.5, state=0) for i in range(k)] # genero un'istanza di Arms (dunque un'azione) con media, parametro di delay, gamma e stato
    #for x in range(10):
    #    print(armsSet[x]._mean) # ricorda che qui la prima azione è 0, non 1
    #    print(armsSet[x]._delay)
    #    print(armsSet[x]._state)

    #chiamo il primo algoritmo di ordinamento delle azioni
    orderedArms = banditRanker(armsSet, k) # sistemare tuning di epsilon

    #chiamo il secondo algoritmo ad eliminazione che restituisce l'insieme di policy ottime
    piLow(orderedArms, k, horizon) # sistemare tuning di S nella costante C quando confronto i g(m)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
