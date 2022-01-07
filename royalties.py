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



def pontos2(j1,j2): #devolve uma lista com os pontos obtidos em royalties e pontos 'normais'
    j1_score=royals(j1)
    j2_score=royals(j2)
    if vencedor_linha(j1.top,j2.top)==2: 
        j2_score+=1
        j1_score-=1
    if vencedor_linha(j1.top,j2.top)==1:
        j1_score+=1
        j2_score-=1
        
    if vencedor_linha(j1.mid,j2.mid)==2:
        j2_score+=1
        j1_score-=1
    if vencedor_linha(j1.mid,j2.mid)==1:
        j1_score+=1
        j2_score-=1
        
    if vencedor_linha(j1.bot,j2.bot)==2: 
        j2_score+=1
        j1_score-=1
    if vencedor_linha(j1.bot,j2.bot)==1:
        j1_score+=1
        j2_score-=1
    return [j1_score,j2_score]

        
###################################################para 3 jogadores############################################################
def vencedor_linha3(mao1,mao2,mao3): #faz linha a linha
        h1 = trunc(hand_strength(mao1))
        h2 = trunc(hand_strength(mao2))
        h3 = trunc(hand_strength(mao3))
        
        #h1 ganha a h2 e h3
        if h1>h2  and h1>h3:return 1
        #h2 ganh a h1 e h3
        if h2>h1 and h2>h3: return 2
        #h3 ganha a h1 e h2
        if h3>h1 and h3>h2: return 3
        #h1 e h2 empatam e sao maiores que h3    
        if h1==h2 and h1>h3:
            if desempate(mao1,mao2)==2: return 2
            if desempate(mao1,mao2)==1: return 1
            else: return 0 #caso muito raro
        #h1 e h3 empatam e sao maiores que h2    
        if h1==h3 and h1>h2:
            if desempate(mao1,mao3)==2: return 3
            if desempate(mao1,mao3)==1: return 1
            else: return 0 #caso muito raro
        #h2 e h3 empatam e sao maiores que h1    
        if h2==h3 and h2>h1:
            if desempate(mao2,mao3)==2: return 3
            if desempate(mao2,mao3)==1: return 2
            else: return 0 #caso muito raro
        else: #no caso em que ambos tem o mesmo tipo de mao
           if desempate(mao1,mao2)==1 and desempate(mao1,mao3)==1: return 1 #mao1 e a mais alta
           if desempate(mao1,mao2)==2 and desempate(mao2,mao3)==1: return 2 #mao2 e a mais alta
           if desempate(mao1,mao3)==2 and desempate(mao2,mao3)==2: return 3 #mao2 e a mais alta
           else: return 0 #caso muito raro
         
        
def royals3(j1): #royalties de um só jogador
    #print("royals",aux_royals_top(j1_top),aux_royals_mid(j1_mid),aux_royals_bot(j1_bot))
    return (aux_royals_top(j1.top)+aux_royals_mid(j1.mid)+aux_royals_bot(j1.bot))


def pontos3(j1,j2,j3): #devolve uma lista com os pontos obtidos em royalties e pontos 'normais'
    j1_score=royals(j1)
    j2_score=royals(j2)
    j3_score=royals(j3)
    
    if vencedor_linha3(j1.top,j2.top,j3.top)==2:
        j2_score+=1
        j1_score-=1
        j3_score-=1
    if vencedor_linha3(j1.top,j2.top,j3.top)==1: 
        j1_score+=1
        j2_score-=1
        j3_score-=1
    if vencedor_linha3(j1.top,j2.top,j3.top)==3: 
        j1_score-=1
        j2_score-=1
        j3_score+=1
        
    if vencedor_linha3(j1.mid,j2.mid,j3.mid)==2: 
        j2_score+=1
        j1_score-=1
        j3_score-=1
    if vencedor_linha3(j1.mid,j2.mid,j3.mid)==1: 
        j1_score+=1
        j2_score-=1
        j3_score-=1
    if vencedor_linha3(j1.mid,j2.mid,j3.mid)==3: 
        j1_score-=1
        j2_score-=1
        j3_score+=3
        
    if vencedor_linha3(j1.bot,j2.bot,j3.bot)==2:
        j2_score+=1
        j1_score-=1
        j3_score-=1
    if vencedor_linha3(j1.bot,j2.bot,j3.bot)==1: 
        j1_score+=1
        j2_score-=1
        j3_score-=1
    if vencedor_linha3(j1.bot,j2.bot,j3.bot)==3: 
        j1_score-=1
        j2_score-=1
        j3_score+=1
    return [j1_score,j2_score,j3_score]
        
#player.update()

#

mao_top1=['JC', '8H', 'QS']
mao_mid1=['5C', '7C', 'AH', '4H', '4D']
mao_bot1=['8C', '7D', 'JS', '9D', 'KC']

mao_top2= ['TS', '9H', 'JH'] #str -4
mao_mid2=  ['7S', '2C', '5D', '2D', 'TD'] #-par-1
mao_bot2=['3C', '8D', 'QC', '8S', 'QH'] #2 pares vale 2 - foul

#jogo 2
mao_top3= ['5S','7D','4C']
mao_mid3= ['AS','JH','9S','TD','TS']
mao_bot3= ['JD','KC','QC','TD','9C']

#print(royals3(mao_trio2,mao_3akind,mao_str_flush))
mao_1_par=['AC', '4S', 'AH', '3C', 'KD']   
mao_1_par1=['KC', '4S', 'AH', '3C', 'KD']  
mao_1_par2=['4C', '4S', 'AH', '3C', 'KD']  
#print(vencedor_linha3(mao_1_par,mao_4akind,mao_1_par))
#print(vencedor_linha3(mao_1_par,mao_1_par,mao_1_par))
#print("royals3",royals3(mao_top3,mao_mid3,mao_bot3))
#print("top",vencedor_linha3(mao_top1,mao_top2,mao_top3))
#print("mid",vencedor_linha3(mao_mid1,mao_mid2,mao_mid3))
#print("bot",vencedor_linha3(mao_bot1,mao_bot1,mao_bot3))
#print(pontos3(mao_top1,mao_mid1,mao_bot1,mao_top2,mao_mid2,mao_bot2,mao_top3,mao_mid3,mao_bot3))
#print(aux_royals_top(mao_top2))
#print(aux_royals_mid(mao_mid2))
#print(aux_royals_bot(mao_bot2))
