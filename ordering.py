import  numpy as np
import random


k = 6 # numero delle azioni
rounding = 5 # numero di cifre decimali a cui arrotondare
means = np.empty(k) # array che conterrà le medie delle azioni, per ora vuoto
policies = np.empty(k)
temp = 0
temp2 = 0

for i in range(k): # per ogni azione
    means[i] = round(random.uniform(0,1), rounding) # genero un numero random tra o ed 1, arrotondato alla quinta cifra decimale e lo memorizzo nel vettore delle medie


means = np.sort(means)[::-1] # ordino le medie in modo decrescente

print("medie ordinate: ", means)

# scambio due posizioni
pos1 = random.randint(0, k-1)
pos2 = random.randint(0, k-1)
if pos1 == pos2:
    pos2 = (pos2 + 1) % k
temp = means[pos1]
means[pos1] = means[pos2]
means[pos2] = temp

print("medie con avvenuto scambio: ", means)
#means = [0.9, 0.2, 0.7, 0.5, 0.8, 0.1] # medie preimpostate per test

# calcolo il reward di ogni policy
for i in range(k):
    sum = 0
    for j in range(i+1):
        sum += means[j]
    policies[i] = sum / (i+1)
print("reward delle policy: ", policies)

for i in range(k):
    succ = k-1 if i == k-1 else i + 1
    if policies[i] < policies[succ]:
        # scambio con precedente, sposto sia policy che media
        # prima mi occupo della policy
        temp = policies[i]
        policies[i] = policies[succ]
        policies[succ] = temp
        # poi mi occupo della media
        temp2 = means[i]
        means[i] = means[succ]
        means[succ] = temp2
for i in range(k-1, -1, -1):
    prec = 0 if i == 0 else i - 1
    if policies[i] > policies[prec]:
        # scambio con successiva, sposto sia policy che media
        # prima mi occupo della policy
        temp = policies[i]
        policies[i] = policies[prec]
        policies[prec] = temp
        # poi mi occupo della media
        temp2 = means[i]
        means[i] = means[prec]
        means[prec] = temp2

print("Policy riordinate: ", policies)
print("Però attenzione che i reward non sono ancora giusti, vanno ricalcolati secondo l'ordinamento nuovo.")
print("medie ordinate correttamente: ", means)

# calcolo il reward di ogni policy con l'ordinamento corretto
for i in range(k):
    sum = 0
    for j in range(i+1):
        sum += means[j]
    policies[i] = sum / (i+1)
print("reward delle policy con ordinamento corretto: ", policies)
