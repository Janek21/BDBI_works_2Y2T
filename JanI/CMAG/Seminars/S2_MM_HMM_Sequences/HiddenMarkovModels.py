'''
@author: Jan
'''
#CMAG.Seminars.S1_Probability_sequences.Probability_simulation

from Probability_simulation import RandomMultinomial

import math

'''
A class to code methods that are used in HMM.
'''
class HiddenMarkovModel(object):

    '''
    Create an object HiddenMarkovModel with transition states and emission probabilities for each state
    Transition is a dictionary where, for each state, we count the probability to move to another state
    Emission is a dictionary where, for each state, we store the probabilities of each category
    '''
    def __init__(self, transition, emission):
        if transition.__len__()!=emission.__len__(): #we need to have same number of emissions and transition, if not, raise Exception
            raise Exception("for each state, we must have an emission probability vector, but found " + transition.__len__() + " " + emission.__len__())
        self.n = transition.__len__() #how many transmission states?, n= length of transition probability matrix
        self.transition = transition
        self.emission = emission
        '''
        dictionary to store the random multinomial 
        '''
        self.random_transition = {} #later will be used for transition probabilities generated by RandomMultinomial, its a dictionary
        self.random_emission = {}  #same but for the emission
        
        '''
        Initialize the random multinomial
        '''
        for key in self.transition:
            self.random_transition[key] = RandomMultinomial(list(transition[key].values())) #for each key generate a set of random numbers using RandomMultinomials class
            self.random_emission[key] = RandomMultinomial(list(emission[key].values())) #for each key a set in transition and one in emission
        
        
    '''
    Compute a sequence of length using a prior probabilities dictionary of the states to start the chain.
    Return the sequence and its hidden states.
    '''    
    def generate_sequence(self, length_sequence, prior_probabilities): #generates random sequence
        chain = [] #will contain the random sequence
        hidden_states = [] #will be used to hold the hidden markov models
        '''
        Iterate over the i elements of the sequence, generating given the emission probabilities and transition probabilities a new .
        '''
        pr = RandomMultinomial(list(prior_probabilities.values())) #with prior probabilites as input, get a sequence of random numbers
        state = list(prior_probabilities.keys())[pr.sample()] #take S or L randomly (from prior)
        for i in range(length_sequence): #iterate from 0 to the length of the sequence
            '''
            from the state, use its emission probability to sample one element
            '''
            category = list(self.emission[state].keys())[self.random_emission[state].sample()]#(take random key from emission(L or S)*takeL)[take random key from dictionary of L or S *takeL from random emission]=random number
            chain.append(category)
            hidden_states.append(state)
            state = list(self.transition[state].keys())[self.random_transition[state].sample()]#takes state for next loop iteration(first uses prior), next ones use transition
        output = [chain,hidden_states]
        return(output)
    
    
    '''
    Compute the log probability of the sequence using forward algorithm. It uses the scale algorithm (Rabiner) to prevent underflow
    '''
    def log_probability_sequence_using_scaling(self, sequence, prior_probabilities):
        '''
        scaling factor
        '''
        f_i = prior_probabilities.copy()

        '''
        the probability turns out to be the multiplication of the scaling factor.
        Since we will use the log, it is the sum of the log of the scaling factor.
        Since the initial s0 adds to 1, the log of it is 0. We do not need to do anything else        
        '''
        S = 0
        
        for i in range(len(sequence)):
            s_ii = 0
            f_ii = {}
            '''
            comes from i
            '''
            for key_ii in f_i:
                '''
                goes to ii
                '''
                a = 0
                for key_i in f_i:
                    '''
                    probability that I move from key_i to key_ii in the position i+1
                    multiplied by the stored scaled f_i at key i 
                    '''
                    a = a + self.transition[key_i][key_ii]*f_i[key_i]
                
                '''
                Probability of, being at key_ii getting the category observed at sequence i
                '''
                a = a*self.emission[key_ii][sequence[i]]
                '''
                before re-scaling by the total s_ii
                '''
                f_ii[key_ii] = a
                '''
                Update the s_ii
                '''
                s_ii = s_ii + a
                
            '''
            Once we have computed all the f_ii, we need to re_scale by the s_ii and set this as the new f_i
            '''        
            for key_ii in f_ii:
                f_i[key_ii] = f_ii[key_ii]/s_ii            
           
            S = S + math.log(s_ii)
        
        return(S)
        
        

    '''
    Compute the log probability of the sequence using forward algorithm.
    '''    
    def log_probability_sequence_without_scaling(self, sequence, prior_probabilities):
        '''
        scaling factor
        '''
        f_i = prior_probabilities.copy()
        S=0
        '''
        the probability turns out to be the multiplication of the scaling factor.
        Since we will use the log, it is the sum of the log of the scaling factor.
        Since the initial s0 adds to 1, the log of it is 0. We do not need to do anything else        
        '''

        for i in range(len(sequence)):
            #s_ii = 0 #we used s_ii to store the updates to the probability ( we rescaled the probability based on s_ii), therefore we don't need it anymore
            f_ii = {}
            '''
            comes from i
            '''
            for key_ii in f_i:
                '''
                goes to ii
                '''
                a = 0
                for key_i in f_i:
                    '''
                    probability that I move from key_i to key_ii in the position i+1
                    multiplied by the stored scaled f_i at key i 
                    '''
                    a = a + self.transition[key_i][key_ii] * f_i[key_i]
                
                '''
                Probability of, being at key_ii getting the category observed at sequence i
                '''
                a = a * self.emission[key_ii][sequence[i]]
                '''
                before re-scaling by the total s_ii
                '''
                f_ii[key_ii] = a
                #why not update s_ii?
                #s_ii = s_ii + a #this update was the one that "stored" the scaling factor
            f_i=f_ii

            #Once we have computed all the f_ii, we need to re_scale by the s_ii and set this as the new f_i     
            #for key_ii in f_ii:
                #f_i[key_ii] = f_ii[key_ii]/s_ii            
           
        S = math.log(sum(f_i.values()))
        
        return(S)


    '''
    given a sequence generated by a HiddenMarkovModel object, estimate the emission probabilities
    of the different categories for each state
    '''

    def estimate_emission_probabilities(self,seq):
        #emission_pd={"S":{"G":0,"C":0,"T":0,"A":0}, "L":{"G":0,"C":0,"T":0,"A":0}}
        emission_pd={} #In case the emission states are not the above we create an empty dict, and define as we iterate
        nucl=seq[0] #nucl= all nucleotides in seq
        states=seq[1] #states are the states in seq

        for pos in range(len(nucl)): #iterate through all nucl positions(not each nucl so that you can use the position for state)

            if states[pos] not in emission_pd: #if a state is not present in dict create an empty dictionary for that state
                emission_pd[states[pos]]={}

            if nucl[pos] not in emission_pd[states[pos]]: #if a nucleotide does not exist in a state, create it as a key with value 0
                emission_pd[states[pos]][nucl[pos]]=0

            emission_pd[states[pos]][nucl[pos]]+=1 #use dict as a counter for each base in each state, +1 for each base in each state
            #if the state and nucelotide do not exist it will still add a +1 so that they are not skipped in the count
        
        for state in emission_pd: #iterate thorugh each state
            total_state_value=sum(emission_pd[state].values()) #sum the values of everything under each state

            for nucl_key in emission_pd[state]: #iterate through the nucleotides in that state
                emission_pd[state][nucl_key]=emission_pd[state][nucl_key]/total_state_value
        
        return(emission_pd)
    
    
    '''
    given a sequence generated by a HiddenMarkovModel object, estimate the transition probabilities
    between states
    '''    
    def estimate_transition_probabilities(self,seq):
        trans_pd={} #So that transmission states can be can be anything we create an empty dict, and define as we iterate
        states=seq[1]
        for pos in range(len(states)-1):

            next_state=states[pos+1]

            if states[pos] not in trans_pd: #if a state is not present in dict create an empty dictionary for that state
                trans_pd[states[pos]]={}

            if next_state not in trans_pd[states[pos]]: #if a next state is not present in the current state, create it as a key with value 0
                trans_pd[states[pos]][next_state]=0
                
            trans_pd[states[pos]][next_state]+=1 #use dict as counter for the next states parting from the current state, +1 for each next state from the current state
            #in any case(state and next_state exist or not) we add 1 to the individual counter for the next state given a current state

        for state in trans_pd: #iterate thorugh each state
            total_state_value=sum(trans_pd[state].values()) #sum the values of everything under each state

            for next_state in trans_pd[state]: #iterate through the next states given a state
                trans_pd[state][next_state]=trans_pd[state][next_state]/total_state_value

        return trans_pd

        


def main():
    transition_probability = {"S":{"S":0.9,"L":0.1},"L":{"S":0.2,"L":0.8}}; #Define the transition states, and the probability of a next state given the current one
    emission_probability = {"S":{"G":0.1,"C":0.2,"T":0.2,"A":0.5}, "L":{"G":0.01,"C":0.1,"T":0.3,"A":0.59}} #define the emission probabilities of each nucleotide given a state
    hmm = HiddenMarkovModel(transition_probability, emission_probability) #hmm is our class, with the defined probabilities as input
    
    prior_probability = {"S":0.5, "L":0.5} #give the prior probabilities for each state
    
    seq = hmm.generate_sequence(600, prior_probability) #generate a sequence given the prior probabilities

    emission_prob = hmm.estimate_emission_probabilities(seq) #define the emission probabilities of the generated sequence
    
    for key in emission_prob: #for each emission state give the probabilities of each nucleotide
        print(key, emission_prob[key])
        
    transition_prob = hmm.estimate_transition_probabilities(seq) #define the transition probabilities of the generated sequence
    
    for key in transition_prob: #for each transition state give the probabilities of what the next state can be
        print(key, transition_prob[key])    

    print(hmm.log_probability_sequence_using_scaling(seq[0], prior_probability))

    print(hmm.log_probability_sequence_without_scaling(seq[0], prior_probability))


    
if __name__ == "__main__":
    main () 