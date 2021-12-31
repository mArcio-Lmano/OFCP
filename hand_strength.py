#codigo para o github
from typing import Counter
import numpy as np
#from numpy.core.fromnumeric import sort 
from collections import Counter
from collections import OrderedDict


def create_deck():
        h_cards = np.array(["T", "Q", "J", "K", "A"]) #T é o 10
        l_cards = np.linspace(2, 9, 8, dtype = int)
        num_cards = np.concatenate((h_cards, l_cards))
        nipes = ["S", "H", "C", "D"]
        deck = []
        for nipe in nipes:
            for num in num_cards:
                deck += [num + nipe]
        return np.array(deck)
baralho=create_deck()
mao=list(np.random.choice(baralho,5))

#maos de teste ####################################################################################################################
mao_rly_flush=['AH','KH','JH','QH','TH']
mao_str_flush=['KC', 'QC', 'JC', 'TC', '9C']     #sequencia do mesmo naipe
mao_4akind=['KC', 'KS', '4H', 'KC', 'KD']        #4=
mao_full_house=['KC', '4S', 'KH', '4C', 'KD']    #1 trio 1 par 
mao_flush=['KC', '9C', 'AC', '3C', '2C']         #tudo do mesmo naipe
mao_str=['KC', 'QS', 'JH', 'TC', '9D']           #sequencia sem ser do mesmo naipe
mao_3akind=['KC', 'KS', 'AH', '4C', 'KD']        #3=
mao_2_pares=['KC', '4S', 'AH', '4C', 'KD']       #2 pares
mao_1_par=['KC', '4S', 'AH', '3C', 'KD']         #1 par


#unsorted hands
mao_np_rly_flush=['KH','AH','TH','QH','JH']      #Maior sequência de 5 cartas do mesmo naipe (A K J Q 10)
mao_no_str_flush=['TC', '9C','KC', 'QC', 'JC']   #sequencia do mesmo naipe
mao_no_4akind=['KC', 'KD','KC', 'KS', '4H']      #4=
mao_no_full_house=['KH', '4C', 'KD','KC', '4S',] #1 trio 1 par 
mao_no_flush=['AC', '3C', '2C','KC', '9C']       #tudo do mesmo naipe
mao_no_str=['JH', 'TC', '9D','KC', 'QS']         #sequencia sem ser do mesmo naipe
mao_no_3akind=[ 'AH', '4C', 'KC', 'KS','KD']     #3=
mao_no_2_pares=['KC', '4C',  '4S', 'AH','KD']    #2 pares
mao_no_1_par=['KC', '3C', 'KD','4S', 'AH']       #1 par
#otherwise highcard################################################################################################################

#1-funçoes auxiliares
def aux_troca_letras(mao): #esta funçao troca as letra todas por numeros para poder testar se e sequencia mais facilmente
        values=list(map(lambda x: x[0],mao))
        for i in range(len(values)):
                if values[i]=='A':      values[i]=14
                if values[i]=='K':      values[i]=13
                if values[i]=='Q':      values[i]=12
                if values[i]=='J':      values[i]=11
                if values[i]=='T':      values[i]=10
        #print("values trocados",values,type(values[i]),len(values))
        return values

def aux_mao_values(mao): #recebe a lista e passa o valor das cartas para inteiros e ordena assim. Exclui-se os naipes
    values=aux_troca_letras(mao)
    values= [int(item) for item in values]
    values.sort()
    return values

def aux_mao_values_inv(mao): #recebe a lista e passa o valor das cartas para inteiros e ordena assim. Exclui-se os naipes
    values=aux_troca_letras(mao)
    values= [int(item) for item in values]
    ord = sorted(values,reverse=True)
    return ord

#print(aux_mao_values(mao_flush))

#2-decisoes de reconhecimento de mao
def is_sequencia(mao): #supondo que recebe uma lista ordenadaa!!!!!!!!  verificar a situação do A e 1!!!!!!
        values=aux_mao_values(mao)
        c = Counter(values)
        counts=c.most_common(1)
        if counts[0][1]>1: 
                return 0
        else :
                for i in range(0,len(values)-1):
                        if  abs(int(values[i+1])-int(values[i]))!=1 and i<len(values)-1:
                                return 0
        return 1

def is_naipe_smp_igual(mao): 
        suits=list(map(lambda x: x[1],mao))
        mx=max(suits,key=suits.count)        #neste caso podemos usar a funçao max porque nao estamos interessados em casos com maxs iguais
        oc=(suits.count(mx))
        return oc==len(suits)

def qual_mao_naipe_nig(mao): #sabendo que temos pelo menos 2 naipes diferentes
        if not is_naipe_smp_igual(mao) and is_sequencia(mao) :
                #print("straight")
                return 4
        values=list(map(lambda x: x[0],mao))
        c = Counter(values)
        if len(mao)==5:
                counts=c.most_common(2) #nao nos interessa mais porque o min seria 3 pares que ja sao 6 cartas 
                if (counts[0][1]==1):  
                        #print ("Carta mais alta") 
                        return 0
                if (counts[0][1]==4): 
                        #print("four of a kind")
                        return 7
                if (counts[0][1]==2 and counts[1][1]==2):
                        #print("2 pares")
                        return 2
                if (counts[0][1]==2 and counts[1][1]==1) :
                        #print("1 par")
                        return 1
                if (counts[0][1]==3 and counts[1][1]==1):
                        #print("3 of a kind")
                        return 3
                if (counts[0][1]==3 and counts[1][1]==2): 
                        #print("full house")
                        return 6
        else: #se nao for 5 tem de ser 3
                counts=c.most_common(1)
                if (counts[0][1]==1):  
                        #print ("Carta mais alta") 
                        return 0
                if (counts[0][1]==2) :
                        #print("1 par")
                        return 1
                if counts[0][1]==3 :
                        #print("3 of a kind")
                        return 3

def qual_mao_naipe_ig(mao): #rever para ter a certeza que esta bem
        if is_naipe_smp_igual(mao) and is_sequencia(mao):
                a1 = aux_mao_values(mao)
                a2 = aux_mao_values(mao_rly_flush)
                if sum(a1) ==  sum(a2):
                        #print("royal flush")
                        return 9  
                #print("straight flush") 
                return 8
        else:                                    #por omissao nao é preciso mas seria if not is_sequencia(mao) and is_naipe_smp_igual(mao) 
            #print("flush")
            return 5

def aux_peso_mao(mao):
        return sum(aux_mao_values(mao))/100

def hand_strength(mao):  
        #print("mao",mao)
        if is_naipe_smp_igual(mao): return((qual_mao_naipe_ig(mao))+aux_peso_mao(mao))
        else :                   return((qual_mao_naipe_nig(mao))+aux_peso_mao(mao))
        
        
#'''   testado e a funcionar
'''
print(hand_strength(mao_1_par))
print(hand_strength(mao_2_pares))
print(hand_strength(mao_3akind))
print(hand_strength(mao_str))        
print(hand_strength(mao_flush))
print(hand_strength(mao_full_house))
print(hand_strength(mao_4akind))
print(hand_strength(mao_str_flush)) 
print(hand_strength(mao_rly_flush))  
'''    
def desempate(mao1,mao2):
        values1=aux_mao_values_inv(mao1)
        values2=aux_mao_values_inv(mao2)
        c1 = Counter(values1).most_common(2)   #[(14,1), (9,1)]   para mao1 = ['9H', '4S', 'AC']
        c2 = Counter(values2).most_common(2)   #[(14,1), (10,1)]  para mao2 = ['4C', 'AH', 'TS']
        
        if c1[0][0] > c2[0][0]:
                #print("ganhou o jogador 1")
                return 1
        elif c2[0][0] > c1[0][0]:
                        #print("ganhou o jogador 2")
                        return 2
        else:
                if c1[1][0] > c2[1][0]:
                        #print("ganhou o jogador 1")
                        return 1
                elif c2[1][0] > c1[1][0]:
                        #print("ganhou o jogador 2")
                        return 2
                else:
                        #print("empate")
                        return 0


#3-funçao de jogo
def vencedor_linha(mao1,mao2): #faz linha a linha
        h1 = hand_strength(mao1)
        h2 = hand_strength(mao2)

        if h1<h2 :
                #print("ganhou o jogador 2")
                return 2
        if h1>h2 :
                #print("ganhou o jogador 1")
                return 1
        else :
                if desempate(mao1,mao2)==2: return 2
                if desempate(mao1,mao2)==1: return 1
                else: return 0 #devia desempatar por naipe?
                

def is_foul(j1):
        if hand_strength(j1.top)>hand_strength(j1.mid) or hand_strength(j1.mid)>hand_strength(j1.bot): 
                #print("Foul")
                return 0
        else:
                return 1
        
#is_foul(mao_2_pares,mao_1_par,mao_str)

        
#get_score(mao_1_par,mao_2_pares,mao_full_house,mao_3akind,mao_flush)

mao_trio =['4H', '4S', 'AC']
mao_trio2 =['AC', 'AH', 'TS']

#print(hand_strength (mao_trio))
#print(hand_strength (mao_trio2))


def vencedor_total(j1,j2):
        j1_score=0
        j2_score=0
        if vencedor_linha(j1.top,j2.top)==2: j2_score+=1
        if vencedor_linha(j1.top,j2.top)==1: j1_score+=1
        
        if vencedor_linha(j1.mid,j2.mid)==2: j2_score+=1
        if vencedor_linha(j1.mid,j2.mid)==1: j1_score+=1
        
        if vencedor_linha(j1.bot,j2.bot)==2: j2_score+=1
        if vencedor_linha(j1.bot,j2.bot)==1: j1_score+=1
        
        if j1_score>j2_score: return 1
        if j2_score>j1_score: return 2
        else: return 0
        
        


def get_score(j1,j2):
        if is_foul(j1)== 1 and is_foul(j2)==1: return vencedor_total(j1,j2) 
        if is_foul(j1)== 1 and is_foul(j2)!=1: return 1
        if is_foul(j1)!= 1 and is_foul(j2)==1: return 2
        else: return 0    #ambos cometeram foul
        
#print(hand_strength(mao_rly_flush))
                

#print(aux_peso_mao(mao_1_par))
        
################################################falta##############################################################        