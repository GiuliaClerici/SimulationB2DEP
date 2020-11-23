import  numpy as np
import random


k = 6 # numero delle azioni
rounding = 5 # numero di cifre decimali a cui arrotondare
means = np.empty(k) # array che conterrà le medie delle azioni, per ora vuoto
policies = np.empty(k) # array che conterrà i reward delle policy
temp = 0
temp2 = 0

for i in range(k): # per ogni azione
    means[i] = round(random.uniform(0,1), rounding) # genero un numero random tra o ed 1, arrotondato alla quinta cifra decimale e lo memorizzo nel vettore delle medie


def checkOrder(a): # func. per controllare che l'array sia ordinato in ordine decrescente
    return all(a[i] >= a[i + 1] for i in range(len(a) - 1))

# calcolo il reward di ogni policy
def rewardPolicies(p, m, k):
    for i in range(k):
        sum = 0
        for j in range(i+1):
            sum += m[j]
        p[i] = round(sum / (i+1), rounding)
    return p

def medianPol(m, k):
    mediane = np.empty(k)
    mediane[0] = m[0]
    for i in range(1, k):
        mediane[i] = np.median(m[0:i+1])
    return mediane

means = np.sort(means)[::-1] # ordino le medie in modo decrescente

print("medie ordinate: ", means)
med =np.median(means)
m = np.mean(means)


# scambio due posizioni
pos1 = random.randint(0, k-1)
pos2 = random.randint(0, k-1)
if pos1 == pos2:
    pos2 = (pos2 + 1) % k
temp = means[pos1]
means[pos1] = means[pos2]
means[pos2] = temp
print("posizioni scambiate: ", pos1, " e ", pos2)
means = [0.9, 0.8, 0.7, 0.2, 0.5, 0.1] # medie preimpostate per test
#means = [0.61794, 0.84724, 0.54763, 0.47389, 0.46413, 0.21241]


print("medie con avvenuto scambio: ", means)
mediane = medianPol(means, k)
print("mediane periodiche: ", mediane)
policies = rewardPolicies(policies, means, k)
print("reward delle policy: ", policies)


checkM = checkOrder(means)
checkP = checkOrder(policies)


for i in range(k):
    print("i: ", i)
    for j in range(k-1):
        print("j: ", j)
        print(policies[j])
        print(policies[j+1])
        if policies[j] < policies[j+1]:
            # swap
            temp = policies[j]
            policies[j] = policies[j+1]
            policies[j+1] = temp
            temp2 = means[j]
            means[j] = means[j + 1]
            means[j + 1] = temp2
            #policies = rewardPolicies(policies, means, k)
            print("means 2: ", means)
            print("policies: ", policies)

    #print("policies: ", policies)
    print("means: ", means)
    policies = rewardPolicies(policies, means, k)
    print("policies: ", policies)


#print("Però attenzione che i reward non sono ancora giusti, vanno ricalcolati secondo l'ordinamento nuovo.")
#print("medie ordinate correttamente: ", means)
#print("policy ordinate correttamente:", policies)

'''
def movePolMeans(policies, means, k):
    for i in range(k):
        succ = k-1 if i == k-1 else i + 1
        if policies[i] < policies[succ]:
            print("policies dentro: ", policies)
            # scambio con precedente, sposto sia policy che media
            # prima mi occupo della policy
            temp = policies[i]
            policies[i] = policies[succ]
            policies[succ] = temp
            # poi mi occupo della media
            temp2 = means[i]
            means[i] = means[succ]
            means[succ] = temp2
            policies = rewardPolicies(policies, means, k)
    print("policy in move: ", policies)
    print("medie in move: ", means)
    for i in range(k-1, -1, -1):
        prec = 0 if i == 0 else i - 1
        if policies[i] > policies[prec]:
            print("dentro succ")
            # scambio con successiva, sposto sia policy che media
            # prima mi occupo della policy
            temp = policies[i]
            policies[i] = policies[prec]
            policies[prec] = temp
            # poi mi occupo della media
            temp2 = means[i]
            means[i] = means[prec]
            means[prec] = temp2
            policies = rewardPolicies(policies, means, k)
    return policies, means



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

#means = [0.9, 0.2, 0.7, 0.5, 0.8, 0.1] # medie preimpostate per test
#means = [0.61794, 0.84724, 0.54763, 0.47389, 0.46413, 0.21241]

print("medie con avvenuto scambio: ", means)
policies = rewardPolicies(policies, means, k)
print("reward delle policy: ", policies)

checkM = checkOrder(means)
checkP = checkOrder(policies)

while (not checkM or not checkP):
    policies, means = movePolMeans(policies, means, k)
    print("Policy riordinate: ", policies)
    print("Medie riordinate: ", means)
    policies = rewardPolicies(policies, means, k)
    print("Ricalcolo reward con ordinamento corretto: ", policies)

    checkM = checkOrder(means)
    checkP = checkOrder(policies)
    print("checkM: ", checkM)
    print("checkP: ", checkP)
    print("not checkM: ", not checkM)
    print("not checkP: ", not checkP)

'''