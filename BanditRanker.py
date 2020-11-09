import numpy as np
from collections import OrderedDict


def banditRanker(arms, k):
    new_mean = 0
    sample = 0
    activeArms = {} # insieme delle azioni attive
    storedArms = np.array([]) # memorizzo azioni le cui medie sono fissate, non hanno overlap con le adiacent
    delInd = np.array([]) # indici di azioni da eliminare dall'insieme di azioni attive e riporre in storedArms, azioni le cui medie sono fissate, non hanno overlap con le adiacenti
    armskeys = np.array(list(activeArms.keys())) # indici delle azioni nell'insieme di azioni attive
    eps_r = 0.009  # imposto il valore di epsilon - INDICATIVO PER ORA, SOLO PER TEST!!!

    print("medie iniziali------------ ") # stampo i valori iniziali delle medie
    for x in range(k): # per ogni azione
        print("azione", x, "con media:", arms[x]._mean) # stampo la media
        activeArms[x] = arms[x]._mean # aggiungo la media di tale azione all'insieme di azioni attive

    armskeys = np.array(list(activeArms.keys()))

    # per un certo numero di round, cerco l'ordinamento corretto delle azioni
    for r in range(10000): #100 valore casuale, decidi poi
        numberRewards = r + 100 # per ora suppongo che abbia già campionato 99 volte, per dare valore alle medie iniziali delle azioni
        #print("--------------------------------round: ", r)
        print("nuovo ciclo - armskeys", armskeys)
        for i in range(armskeys.size):# per ogni azione nell'insieme di azioni attive
            # CAMPIONO E AGGIORNO LE MEDIE
            mean, sample = arms[armskeys[i]].sampleReward(rep_index=0) # campiono e restituisco expected reward e sample
            #print("media al round corrente: ", mean)
            #print("reward campionato: ", sample)
            new_mean = ((arms[armskeys[i]]._mean * (numberRewards-1)) + sample)/(numberRewards)  # calcolo la nuova media in base al reward campionato
            #print("nuova media: ", new_mean)
            arms[armskeys[i]]._mean = new_mean # aggiorno la media dell'azione con la nuova media
            activeArms[i] = arms[armskeys[i]]._mean # aggiungo la media (aggiornata) dell'azione all'insieme di azioni attive
            new_mean = 0 # risetto la variabile a 0 per la prossima azione
            sample = 0 # risetto la variabile a 0 per la prossima azione

        # ORDINO LE MEDIE
        activeArms = {k: v for k, v in sorted(activeArms.items(), key=lambda item: item[1], reverse=True)} # ordino le medie delle azioni attive sorted prende dict ma mi restituisce list, mentre così ho ancora dict
        print("Medie ordinate: ", activeArms)

        # FASE DI CONTROLLO DELL'OVERLAP CON LE MEDIE ADIACENTI
        Kmin = 1.0 # inizializzo variabili per confronto
        Kplus = 0.0 # inizializzo variabili per confronto
        j = 0

        if r == 0:
            armskeys = np.array(list(activeArms.keys()))
        for j in range(armskeys.size): # per ogni azione nell'insieme di azioni attive
            print(armskeys)
            if j == 0: # se valuto la prima media, dunque quella maggiore di tutte
                print("prima azione")
                print(activeArms[armskeys[j]])
                print(activeArms[armskeys[j]] - (2 * eps_r))
                print(activeArms[armskeys[j+1]]) # C'è UN PROBLEMA QUI!!
                if activeArms[armskeys[j]] - (2 * eps_r) > activeArms[armskeys[j+1]]: # controllo solamente che non vi sia overlap con la media dell'azione successiva
                    storedArms = np.append(storedArms, activeArms[armskeys[j]]) # memorizzo tale media nell'array in cui memorizzo le medie "fisse" che non hanno overlap con le adiacenti
                    delInd = np.append(delInd, j) # memorizzo l'indice di tale azione per poi poterla rimuovere dall'insieme di azioni attive
                    print("dentro ciclo per prima azione")

            elif j == armskeys.size - 1: # altrimenti, se sto valutando l'ultima azione, quella con media minore tra tutte
                print("ultima azione")
                print(activeArms[armskeys[j]])
                print(activeArms[armskeys[j]] + (2 * eps_r))
                print(activeArms[armskeys[j - 1]])
                if activeArms[armskeys[j]] + (2 * eps_r) < activeArms[armskeys[j-1]]: # controllo solamente che non vi sia overlap con la media dell'azione precedente
                    storedArms = np.append(storedArms, activeArms[armskeys[j]]) # memorizzo tale media nell'array in cui memorizzo le medie "fisse" che non hanno overlap con le adiacenti
                    delInd = np.append(delInd, j) # memorizzo l'indice di tale azione per poi poterla rimuovere dall'insieme di azioni attive
                    print("dentro ciclo per ultima azione")

            else: # per tutte le altre azioni che non siano la prima e l'ultima
                print("azioni centrali")
                print(activeArms[armskeys[j]])
                print(activeArms[armskeys[j]] - (2 * eps_r))
                print(activeArms[armskeys[j + 1]])
                print(activeArms[armskeys[j]] + (2 * eps_r))
                print(activeArms[armskeys[j - 1]])
                if activeArms[armskeys[j]] + (2 * eps_r) < activeArms[armskeys[j-1]]: # se non hanno overlap con l'azione precedente, con media maggiore
                    if activeArms[armskeys[j]] - (2 * eps_r) > activeArms[armskeys[j+1]]: # se non hanno overlap con l'azione successiva, con media inferiore
                        storedArms = np.append(storedArms, activeArms[armskeys[j]]) # memorizzo tale media nell'array in cui memorizzo le medie "fisse" che non hanno overlap con le adiacenti
                        delInd = np.append(delInd, j) # memorizzo l'indice di tale azione per poi poterla rimuovere dall'insieme di azioni attive
                        print("dentro ciclo per azioni interne")

        print("indexes: ", delInd) # stampo indici delle azioni la cui media non ha overlap con le adiacenti, con media "stabile", da rimuovere dall'insieme di azioni attive
        print(armskeys) # stampo lista di indici delle azioni attive
        armskeys = np.delete(armskeys, delInd.astype(int)) # dala lista di indici delle azioni attive elimino quelle le cui medie non hanno overlap
        print(armskeys) # stampo indici delle azioni attive, ancora da valutare
        ind = np.array([b for b in range(delInd.size)]) # array di indici delle azioni da eliminare che mi serve al passo successivo
        delInd = np.delete(delInd, ind.astype(int)) # ripulisco l'insieme degli indici delle azioni da eliminare dall'insieme di azioni attive
        #print(delInd) # stampo per controllare sia vuoto
        storedArms = np.sort(storedArms)[::-1] # ordino l'array contenente le azioni senza overlap eliminate dall'insieme di azioni attive ed ora fissate
        print("medie rimosse fisse: ", storedArms) # stampo le medie delle azioni senza overlap

        # QUANDO RIPARTO DEVO TENERE SOLO LE AZIONI NON FISSATE
        if armskeys.size == 0:
            break
        eps_r -= 0.001 # imposto il valore di epsilon - INDICATIVO PER ORA, SOLO PER TEST!!!
        if eps_r < 0.0:
            eps_r = 0.0001
    #print("medie finali------------ ")
    #for x in range(k):
    #    print("azione", x, "con media:", arms[x]._mean)
    #print("sorted_means finali: ", sorted_means)

    return storedArms

def piLow(arms, orderedArms):
    return 0
