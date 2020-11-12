import numpy as np
from scipy.stats import bernoulli
import scipy

class Arms():
    """Bernoulli distributed arm"""

    def __init__(self, mean, delay, gamma, state):
        self._mean = mean
        self._delay = delay
        self._gamma = 2 # determina funzione monotona non decrescente, inizio ad impostarla a 0.5
        self._state = state # all'inizio 0, poi aumenta - quando è ≤ delay allora reward(tau) altrimenti se ≥ delay baseline reward, quando viene nuovamente giocata si pone state= 1
        self._currentDelay = 0

    def sampleReward(self, rep_index):
        expectedReward = self._mean
        if self._state != 0 and self._state <= self._delay: # se recentemente giocata, reward subisce effetto delay
            expectedReward *= (1 - self._gamma **(- self._state)) # segue una funzione monotona non decrescente
        self._state = 1 # dopodiché bisogna aggiornarlo ad ogni round!
        return (expectedReward, bernoulli.rvs(expectedReward, random_state=rep_index)) # restituisco media (baseline o affetta da delay) e reward Bernoulliano in {0,1}, in base alla media - non mi piace come funziona
        #scipy.random.binomial(n=1, p=expectedReward)) # parameters: number of trials, probability - #

    def updateState(self): # non valuto il caso dell'azione appena giocata perché lì lo stato viene già aggiornato con sampleReward
        self._state = self._state + 1
        return self._state


