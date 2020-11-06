import numpy as np
from scipy.stats import bernoulli
import scipy

class Arms():
    """Bernoulli distributed arm"""

    def __init__(self, mean, delay, gamma, state):
        self._mean = mean
        self._delay = delay
        self._gamma = gamma # determina funzione monotona non decrescente
        self._state = state # all'inizio 0, poi aumenta - quando è ≤ delay allora reward(tau) altrimenti se ≥ delay baseline reward, quando viene nuovamente giocata si pone state= 1
        self._currentDelay = 0

    def sampleReward(self, currentDelay, rep_index):
        expectedReward = self._mean
        if currentDelay != 0 and currentDelay <= self._delay: # se recentemente giocata, reward subisce effetto delay
            expectedReward *= (1 - self._gamma ** currentDelay) # segue una funzione monotona non decrescente
        return (expectedReward, bernoulli.rvs(expectedReward, random_state=rep_index)) # restituisco media (baseline o affetta da delay) e reward Bernoulliano in {0,1}, in base alla media
        #scipy.random.binomial(n=1, p=expectedReward)) # parameters: number of trials, probability - #

    def stateArm(self, currentDelay):
        expectedReward = self._mean
        if currentDelay <= self._delay and currentDelay >= 0:
            expectedReward = self._mean * (1.0 - (self._gamma ** currentDelay))
            print(1, "computeState(), disc mean {}".format(expectedReward)) # restituisco la media e un numero random campionato dalla distribuzione bernoulliana, quindi 0 o 1
        else:
            print(1, "computeState(), exp mean {}".format(expectedReward))
        return expectedReward


