# Simulation environment for the B2DEP experiments
# author = 'Giulia Clerici'

import random
import numpy as np
from armsMAB import Arms
from BanditRanker import banditRanker
from PiLow import  piLow
from operator import itemgetter


def main():
    horizon = 810000 # orizzonte
    k = 10 # numero di azioni
    #armsSet = {}
    #armsSet = [Arms(mean=i / 10, delay=1, gamma=0.5, state=0) for i in range(10, 0, -1)]
    #armsSet[9]._delay = 1
    armsSet = [Arms(mean=random.uniform(0, 1), delay=(i+1)%5 + 1, gamma=0.5, state=0) for i in range(k)] # genero un'istanza di Arms (dunque un'azione) con media, parametro di delay, gamma e stato
    #means = np.empty(k)
    #for x in range(k):
        #means[x] = armsSet[x]._mean
        #print(armsSet[x]._mean) # ricorda che qui la prima azione è 0, non 1
        #print(armsSet[x]._delay)
        #print(armsSet[x]._state)

    armsSet.sort(key=lambda x: x._mean, reverse=True) # ordino le azioni in modo decrescente rispetto alla media _mean

    # scambio due posizioni
    pos1 = random.randint(0, k - 1)
    pos2 = random.randint(0, k - 1)
    if pos1 == pos2:
        pos2 = (pos2 + 1) % k
    temp = armsSet[pos1]
    armsSet[pos1] = armsSet[pos2]
    armsSet[pos2] = temp

    # stampo le medie delle azioni ordinate in modo decrescente
    for x in range(k):
        print(armsSet[x]._mean)  # ricorda che qui la prima azione è 0, non 1
        print(armsSet[x]._delay)

    # calcolo reward delle policy senza delay
    g = np.empty(k) # reward medi delle policy senza delay
    gdelay = np.empty(k) # reward medi delle policy con delay

    def rewardPolicies(g, m, k):
        for i in range(k):
            sum = 0
            for j in range(i + 1):
                sum += m[j]._mean
            g[i] = round(sum / (i + 1), 5)
        return g

    g = rewardPolicies(g, armsSet, k)
    print("g: ", g)

    # calcolo reward delle policy con delay
    # gioco ogni azione in modo da calibrare e avere tutti stati pari a 1 dunque attivi i delay
    for i in range(k):
        armsSet[i]._state = k - i


    def rewardPoliciesDelay(gdelay, m, k):
        for i in range(k):
            t = 0
            sum = 0
            while(t <= i):
                r, sample = m[t].sampleReward(rep_index=0)
                for x in range(i):
                    if x != t:
                        m[x].updateState()
                sum += r
                t += 1
            gdelay[i] = round(sum / (i + 1), 5)
            sum = 0
            t = 0
        return gdelay

    gdelay = rewardPoliciesDelay(gdelay, armsSet, k)
    print("gdelay: ", gdelay)

    # calcolo reward dopo campionamento

    #chiamo il primo algoritmo di ordinamento delle azioni
    #orderedArms = banditRanker(armsSet, k) # sistemare tuning di epsilon
    #for i in range(k):
    #    print(orderedArms[i]._mean)
    #    print(orderedArms[i]._delay)
    #chiamo il secondo algoritmo ad eliminazione che restituisce l'insieme di policy ottime
    #piLow(orderedArms, k, horizon) # sistemare tuning di S nella costante C quando confronto i g(m)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
