import random
from scipy.stats import bernoulli
import scipy
from collections import OrderedDict
import numpy as np
from math import sqrt, log
from armsMAB import Arms


flag = 1
if flag == 1:
    k = 10
    horizon = 810000
    arms = [Arms(mean=i/10, delay=i-1, gamma=0.5, state=0) for i in range(10, 0, -1)]
    arms[9]._delay = 1
    actPol = np.array([m for m in range(k)]) # insieme di policy attive, che all'inizio ha cardinalità K, uguale al numero di azioni, dove la policy 1 cicla solo sulla prima azione, la policy 2 sulla prima e seconda azione e così via
    ghost = 0 # ghost policy, quella rivelatasi migliore - memorizzo indice dell'azione m su cui cicla la ghost policy
    n = 0 # numero round
    sum = 0
    g = np.empty(k)
    rounding = 5
    delta = 0.1
    ind = np.array([])
    s = 0 # indice rounding

    for i in range(k):
        arms[i]._state = 0


    while (s <= horizon): # finché il numero di pull non  supera l'orizzonte -METTO 0 SOLO PER I TEST, POI DEVO METTERE HORIZON
        #print("n: ", n)
        for m in range(actPol.size): # gioca ogni policy nell'insieme di policy attive
            print(actPol.size)
            #print(" nuova policy m: ", m)
            #print("verrà giocata per volte: ", int(((horizon**(1-2**(-(n+1)))) / ((m+1) * 10))) + 1 )
            sum = 0
            for j in range(int(((horizon**(1-2**(-(n+1)))) / ((m+1) * 10))) + 1 ): # per un certo numero di round gioca la policy
                #print("j: ", j)
                if j <= m: # per il primo round
                    #print("j nel primo loop: ", j)
                    #print("confermo m: ", m)
                    #print("dentro primo loop.")
                    arms[j].sampleReward(rep_index=0) # gioco l'azione, scarto il primo round ma aggiorno lo stato - così avrò medie in funzione dello stato, dipendenti dal delay
                    #print("stato: ", arms[j]._state)
                else: # per i restanti round
                    #print("entro nel calcolo g(m) con j: ", j)
                    #print("stato: ", arms[(j % (m+1))]._state)
                    mean, sample = arms[(j % (m+1))].sampleReward(rep_index=0) # campiono azione tra le azioni 1 - ... - m e aggiorno lo stato
                    #print("mean prima di sum: ", mean)
                    sum += mean # potrei accorpare in una sola riga sum += arms[(j % m)].sampleReward(rep_index=0)[0]
                    for i in range(m): # per ogni altra azione
                        if i != (j % m): # tranne quella giocata
                            arms[i].updateState() # aggiorno lo stato
                            #print("azione: ", i , "stato: ", arms[i]._state)
            g[m] = sum / j # calcolo g(m) - dove j è  ((horizon**(1-2**(-n))) / (m * actPol.size)) + 1 - tra l'altro ad ogni round aggiorno g(m) della policy che cicla su m, per quelle eliminate rimane l'ultima g(m) calcolata prima dell'eliminazione
            s += int(((horizon**(1-2**(-(n+1)))) / ((m+1) * 10))) + 1 # calcolo numero di round
        print("le diverse g(m): ", g)
        c = (0.5*round(sqrt( log((((horizon**(1-2**(-(n+1))))+ k) * k * 2)/delta) * (k / (2 * (horizon**(1-2**(-(n+1))))))), rounding)) # confidence gap che utilizzo per valutare quali policy eliminare
        print("c gap: ", c)
        for i in range(m+1): # per ogni policy attiva
            #print("i: ", i)
            #print("g(i): ", g[i])
            #print("confronto: ", np.max(g) - 2 * c)
            if g[i] < np.max(g) - 2 * c and i != np.argmax(g): # se g(m) di tale policy è minore di max g(m) di un certo gap
                #print("i in if: ", i)
                ind = np.append(ind, i)
        print("g ind: ", ind)
        print("g max: ", np.max(g))
        actPol = np.delete(actPol, ind.astype(int)) # elimino tale policy dall'insieme delle policy attive
        g = np.delete(g, ind.astype(int))
        delInd = np.array([b for b in range(ind.size)])  # array di indici delle azioni da eliminare che mi serve al passo successivo
        ind = np.delete(ind, delInd.astype(int))
        n += 1
        #s = s + 1
        if actPol.size == 1:
            ghost = actPol
            print("ghost: ", actPol)
            break
        #print(actPol)
    print("Quante policy restituite da PiLow? ", actPol.size)
    print("La ghost policy è quella che cicla sulle prime ", ghost+1 , " azioni, ossia sulle azioni 0 - ... -  ", ghost)


