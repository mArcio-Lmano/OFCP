from hand_strength import *
import numpy as np
from math import trunc

baralho=create_deck()
mao=list(np.random.choice(baralho,5))

mao_rly_flush=['AH','KH','JH','QH','TH']
mao_str_flush=['KC', 'QC', 'JC', 'TC', '9C']     #sequencia do mesmo naipe
mao_4akind=['KC', 'KS', '4H', 'KC', 'KD']        #4=
mao_full_house=['KC', '4S', 'KH', '4C', 'KD']    #1 trio 1 par 
mao_flush=['KC', '9C', 'AC', '3C', '2C']         #tudo do mesmo naipe
mao_str=['KC', 'QS', 'JH', 'TC', '9D']           #sequencia sem ser do mesmo naipe
mao_3akind=['KC', 'KS', 'AH', '4C', 'KD']        #3=
mao_2_pares=['KC', '4S', 'AH', '4C', 'KD']       #2 pares
mao_1_par=['KC', '4S', 'AH', '3C', 'KD']         #1 par


mao_trio =['6H', '6S', 'AC']
mao_trio2 =['AC', 'AH', 'AS']
###################################################################################################################

def aux_royals_top(mao):
    values=aux_mao_values_inv(mao)
    counts = Counter(values).most_common(2)   #[(14,1), (10,1)]  para mao2 = ['4C', 'AH', 'TS']

    if (counts[0][1]==1):  #Carta mais alta
        #print("carta mais ata")
        return 0
        
    if (counts[0][1]==2) : #par
        #print("1 par")
        if counts[0][0]==6: return 1
        if counts[0][0]==7: return 2
        if counts[0][0]==8: return 3
        if counts[0][0]==9: return 4
        if counts[0][0]==10: return 5
        if counts[0][0]==11: return 6
        if counts[0][0]==12: return 7
        if counts[0][0]==13: return 8
        if counts[0][0]==14: return 9
        else: return 0 

    if counts[0][1]==3 : #3akind
        #print("3 of a kind")
        if counts[0][0]==2: return 10
        if counts[0][0]==3: return 11
        if counts[0][0]==4: return 12
        if counts[0][0]==5: return 13
        if counts[0][0]==6: return 14
        if counts[0][0]==7: return 15
        if counts[0][0]==8: return 16
        if counts[0][0]==9: return 17
        if counts[0][0]==10: return 18
        if counts[0][0]==11: return 19
        if counts[0][0]==12: return 20
        if counts[0][0]==13: return 21
        if counts[0][0]==14: return 22
        

def aux_royals_mid(mao):
    if trunc(hand_strength(mao))==3: return 2 #3akind
    if trunc(hand_strength(mao))==4: return 4 #str
    if trunc(hand_strength(mao))==5: return 8 #flusn
    if trunc(hand_strength(mao))==6: return 12 #full_house
    if trunc(hand_strength(mao))==7: return 20 #4akind
    if trunc(hand_strength(mao))==8: return 30 #str_flush
    if trunc(hand_strength(mao))==9: return 50 #rly_flush
    else: return 0
    
def aux_royals_bot(mao):
    if trunc(hand_strength(mao))==4: return 2 #str
    if trunc(hand_strength(mao))==5: return 4 #flusn
    if trunc(hand_strength(mao))==6: return 6 #full_house
    if trunc(hand_strength(mao))==7: return 10 #4akind
    if trunc(hand_strength(mao))==8: return 15 #str_flush
    if trunc(hand_strength(mao))==9: return 25 #rly_flush
    else: return 0
    
#print(aux_royals_bot(mao_str))
#print(aux_royals_mid(mao_flush))

def royals(j1): #royalties de um só jogador
    print("royals",aux_royals_top(j1.top)+aux_royals_mid(j1.mid)+aux_royals_bot(j1.bot))
    return (aux_royals_top(j1.top)+aux_royals_mid(j1.mid)+aux_royals_bot(j1.bot))



def pontos(j1,j2): #devolve uma lista com os pontos obtidos em royalties e pontos 'normais'
    j1_score=royals(j1)
    j2_score=royals(j2)
    if vencedor_linha(j1.top,j2.top)==2: j2_score+=1
    if vencedor_linha(j1.top,j2.top)==1: j1_score+=1
        
    if vencedor_linha(j1.mid,j2.mid)==2: j2_score+=1
    if vencedor_linha(j1.mid,j2.mid)==1: j1_score+=1
        
    if vencedor_linha(j1.bot,j2.bot)==2: j2_score+=1
    if vencedor_linha(j1.bot,j2.bot)==1: j1_score+=1
    return [j1_score,j2_score]
        

        
        
