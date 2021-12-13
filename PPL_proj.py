import numpy as np
from player import *

def convert_to_string(lista):
    """
    Função que tranforma uma lista de chars numa string
    Util para podermos aceder às keys dos nossos dicionaríos
     dos pontos
    """

    s = ""
    for x in lista:
        s+=x
    
    return s


# Dícionário dos pontos tendo em conta onde a mão está, top, mid ou bot
top_point = {
        "66" : 1,
        "77" : 2,
        "88" : 3,
        "99" : 4,
        "TT" : 5,
        "JJ" : 6,
        "QQ" : 7,
        "KK" : 8,
        "AA" : 9,
        "222" : 10,
        "333" : 11,
        "444" : 12,
        "555" : 13,
        "666" : 14,
        "777" : 15,
        "888" : 16,
        "999" : 17,
        "TTT" : 18,
        "JJJ" : 19,
        "QQQ" : 20,
        "KKK" : 21,
        "AAA" : 22
        }
mid_point = {
        "3OfKind" : 2,
        "seq" : 4,
        "flush" : 8,
        "FHouse" : 12,
        "4OfKind" : 20,
        "seqFlush" : 30,
        "RFlush" : 50
        }
bot_point = {
        "seq" : 2,
        "flush" : 4,
        "FHouse" : 6,
        "4OfKind" : 10,
        "seqFlush" : 15,
        "RFlush" : 25
        }


class Game:
    def __init__(self, names = ["Player1", "Player2"], num_jogadores = 1):
        """
        Class associada ao jogo de Poker, onde temos um baralho de 52 cartas,
        \'2,3,4,5,6,7,8,9,10,J,Q,K,A\' com 4 nipes cada uma das cartas
        \'S\' - Spades
        \'H\' - Hearts
        \'C\' - Clubs
        \'D\' - Diamons
        """

        self.baralho = self.create_deck()
        self.player1 = Player(names[0])
        self.player2 = Player(names[1])

    def create_deck(self):
        h_cards = np.array(["T", "Q", "J", "K", "A"])
        l_cards = np.linspace(2, 9, 8, dtype = int)
        num_cards = np.concatenate((h_cards, l_cards))
        nipes = ["S", "H", "C", "D"]
        deck = []
        
        for nipe in nipes:
            for num in num_cards:
                deck += [num + nipe]
            
        return np.array(deck)
    
    def draw_card(self, player):
        card = np.random.choice(self.baralho)
        self.baralho = np.delete(self.baralho, np.argwhere(self.baralho == card))

        if player == "player1":
            self.player1.give_card(card)
        elif player == "player2":
            self.player2.give_card(card)
        else:
            print(f"O jogador ({player}) não está a jogar")
        return card
    
    def get_score(self):
        points1 = 0
        points2 = 0

        top1 = self.player1.top
        top1_num = [x[0] for x in top1]
        top1_notrep = list(set(top1_num)) #remover repetidos
        top1_group = [[x for x in top1_num if x == y] for y in top1_notrep] # group por cartas iguais
        top1_str = [convert_to_string(x) for x in top1_group]
        point1

        top2 = self.player2.top
        top2_num = [x[0] for x in top2]
        top2_notrep = list(set(top2_num))
        top2_group = [[x for x in top2_num if x == y] for y in top2_notrep]    


def main():
    jogo = Game() # Criação do Jogo
    player1 = jogo.player1 # Player
    player2 = jogo.player2 # Ai
    print(jogo.baralho)
    
    # Tirar as primeiras 5 cartas para o Jogador e para a AI 
    for _ in range(5):
        card1 = jogo.draw_card("player1")
        card2 = jogo.draw_card("player2")
    
    # Primeira Mão Player
    print(6*"#" + " Player " + 6*"#")
    print(f"Saiu lhe a seguinte mão {player1.hand}")
    for i in range(5):
        pos = input(f"Onde quer colocar {player1.hand[i]}?\n>>> ")
        player1.add_2_table(pos)

    print(2*"\n")

    # Primeira Mão AI
    print(6*"#" + " AI " + 6*"#")
    print(f"Saiu lhe a seguinte mão {player2.hand}")
    for i in range(5):
        pos = input(f"Onde quer colocar {player2.hand[i]}?\n>>> ")
        player2.add_2_table(pos)

    # Ciclo de Jogo o jogo acaba quando o Jogador e a AI têm ambos 13 cartas
    while len(player1.hand) < 13 and len(player2.hand) < 13:
        print(6*"#" + " Player " + 6*"#") # Vez do jogador 1 jogar
        card = jogo.draw_card("player1")
        print(player1.field)
        pos = input(f"Jogador 1 saiu lhe {card} onde quer por a carta?\n>>> ")
        player1.add_2_table(pos)
        
        print(2*"\n")
        
        print(6*"#" + " Ai " + 6*"#")
        card = jogo.draw_card("player2")
        print(player2.field)
        pos = input(f"Jogador 2 saiu lhe {card} onde quer por a carta?\n>>> ")
        player2.add_2_table(pos)
        
        print(2*"\n")
    """
    print("O jogo acabou, e estes são as maos dos 2 jogadores")
    player1.top = np.array(["KS", "KC", "QS"])
    print("Player")
    print(player1.field)
    print("\nAI")
    print(player2.field)
    """
    print("Vamos calcular os pontos")

    #print(jogo.get_score())



if __name__ == "__main__":
    print("Projeto de PP")
    main()
