# Simulation environment for the B2DEP experiments
# author = 'Giulia Clerici'

import random
import numpy as np
from arms import Arms
from algorithmsB2DEP import banditRanker, piLow



def main():
    armsSet = {}
    #armsSet = [Arms(mean=i/10, delay=i, gamma=0.4) for i in range(10)]
    armsSet = [Arms(mean=random.uniform(0, 1), delay=i, gamma=0.4, state=0) for i in range(10)]
    #for x in range(10):
    #    print(armsSet[x]._mean) # ricorda che qui la prima azione è 0, non 1
    #    print(armsSet[x]._delay)
    #    print(armsSet[x]._state)
    #print(armsSet[6].sampleReward(currentDelay=0, rep_index=1))

    #chiamo il primo algoritmo di ordinamento delle azioni
    orderedArms = banditRanker(armsSet, k=10)
    #chiamo il secondo algoritmo ad eliminazione che restituisce l'insieme di policy ottime
    piLow(armsSet, orderedArms) #opp. mi basta solo orderedArms



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
