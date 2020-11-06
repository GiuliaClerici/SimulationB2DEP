import numpy as np
from collections import OrderedDict


def banditRanker(arms, k):
    new_mean = 0
    sample = 0
    sorted_indx = np.empty(k)
    sorted_means = np.empty(k)
    array_means = np.empty(k)
    activeArms = {}
    K_plus = np.array([])
    K_minus = np.array([])

    print("medie iniziali------------ ")
    for x in range(k):
        print("azione", x, "con media:", arms[x]._mean)
        activeArms[x] = arms[x]._mean


    for r in range(1,10): #100 valore casuale, decidi poi
        numberRewards = r + 100 # per ora suppongo che abbia già campionato 99 volte, per dare valore alle medie iniziali delle azioni
        print("--------------------------------round: ", r)
        for i in activeArms.keys():# per ogni azione nell'insieme di azioni attive
            mean, sample = arms[i].sampleReward(currentDelay=0, rep_index=1) # campiono ogni azione e vado ad aggiornare le medie
            #print("media al round corrente: ", mean)
            #print("reward campionato: ", sample)
            # NON FUNZIONA IL CALCOLO DELL'AGGIORNAMENTO DELLA MEDIA
            new_mean = ((mean * (numberRewards-1)) + sample)/(numberRewards)  # fingiamo di partire con già un campione presente (che di fatto è la media assegnata inizialmente a quella azione)
            #print("nuova media: ", new_mean)
            arms[i]._mean = new_mean
            #array_means[i] = arms[i]._mean #np.append(array_means, arms[j]._mean)
            activeArms[i] = arms[i]._mean
            new_mean = 0
            sample = 0

        # ordino le medie
        activeArms = {k: v for k, v in sorted(activeArms.items(), key=lambda item: item[1], reverse=True)} # sorted prende dict ma mi restituisce list, mentre così ho ancora dict
        #print(activeArms)

        # controllo overlap
        eps_r = np.sqrt((1/(2*r)) * np.log((2*k*r*(r+1))/(0.1)))

        Kmin = 1.0
        Kplus = 0.0
        for i in activeArms.keys():
            print("act arm i: ", activeArms[i])
            for l in activeArms.keys():
                print("act arm l: ", activeArms[l])
                if activeArms[l] >= activeArms[i] and i!=l and activeArms[l] < Kmin:
                    print("sono dentro")
                    print("act arm l: ", activeArms[l])
                    Kmin = activeArms[l]
                    print("Kmin: ", Kmin)
                    #K_plus = np.append(K_plus, activeArms[l])
                if activeArms[l] < activeArms[i] and i!=l and activeArms[l] > Kplus:
                    print("sono dentro")
                    Kplus = activeArms[l]
                    print("Kplus: ", Kplus)
                    #np.append(K_minus, activeArms[l])


            print("k_plus: ", K_plus)
            if K_plus.size != 0 and activeArms[i] + (2*eps_r) < Kplus: #np.amin(K_plus):
                if K_minus.size != 0 and activeArms[i] - (2 * eps_r) > Kmin: #np.amax(K_minus):
                    np.append(K_plus, activeArms[i])
                    np.append(activeArms[i], K_minus)
                    del activeArms[i]

        eps_r = 0


    #print("medie finali------------ ")
    #for x in range(k):
    #    print("azione", x, "con media:", arms[x]._mean)
    #print("sorted_means finali: ", sorted_means)

    return

def piLow(arms, orderedArms):
    return 0
