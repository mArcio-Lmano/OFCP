import numpy as np
from player import *
from hand_strength import get_score, hand_strength, vencedor_linha
from decidir import place_cards




class Game:
    def __init__(self, n_players, n_AIs, num_jogadores = 1):
        """
        Class associada ao jogo de Poker, onde temos um baralho de 52 cartas,
        \'2,3,4,5,6,7,8,9,10,J,Q,K,A\' com 4 nipes cada uma das cartas
        \'S\' - Spades
        \'H\' - Hearts
        \'C\' - Clubs
        \'D\' - Diamons
        """
        
        while n_players + n_AIs > 3:
            print("Maximo 3 jogadores")
            n_players = input("Number of human players\n>>>")
            n_AIs = input("Number of BOTS\n>>>")

        self.players_list = []
        self.AIs_list = []

        for i in range(n_players):
            #listab de players
            nome = input(f"Player {i+1} what is your name?\n>>>")
            self.players_list += [Player(nome)] 

        for i in range(n_AIs):
            self.AIs_list += [Player(f"AI {i+1}")]

        self.baralho = self.create_deck()

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
        
        player.give_card(card)

        return card
    
    def game_loop(self):
        """
        Loop associado a um jogo de POFCP
        """

        # PLayers Turn
        for player in self.players_list:

            # Tirar as primeiras 5 cartas 
            for _ in range(5):
                card = self.draw_card(player)
    
            # Primeira Mão Player
            print(6*"#" + f" {player.name} " + 6*"#")
            print(f"Saiu lhe a seguinte m`ão {player.hand}")

            for i in range(5):
                pos = input(f"Onde quer colocar {player.hand[i]}?\n>>> ")
                player.add_2_table(pos)
            
            print(player.field)
            print(2*"\n")

        # BOTS Turn
        for bot in self.AIs_list:

            # Tirar as primeiras 5 cartas
            for _ in range(5):
                card = self.draw_card(bot)

            print(6*"#" + f" {bot.name} " + 6*"#")
            print(f"Saiu lhe a seguinte mão {bot.hand}")
            
            place_AI = place_cards(self, bot, bot.hand)[0]
            print(place_AI)
            for i in range(5):
                if place_AI[i] == 0:
                    bot.add_2_table("top")
                elif place_AI[i] == 1:
                    bot.add_2_table("mid")
                else:
                    bot.add_2_table("bot")
            
            print(bot.field)
            print(2*"\n")

        num_cards = sum([len(player.hand) for player in self.players_list + self.AIs_list])/ (len(self.players_list) + len(self.AIs_list))

        while  num_cards != 13:

            # Player 3cards game cicle
            for player in self.players_list:
                print(6*"#" + " {player.name} " + 6*"#") # Vez do jogador 1 jogar
                cards = np.array([])
                
                for _ in range(3):
                    card = self.draw_card(player)
                    cards = np.append(cards, card)
               
                print(player.field)
                card_off = input(f"{player.name} saiu lhe as seguintes {cards} qual quer descartar?\n>>> ")
                
                while card_off not in cards:
                    card_off = input(f"Carta inválida!! {cards} qual quer descartar?\n>>> ")
                
                player.add_lixo(card_off)
                cards = np.delete(cards, np.argwhere(cards == card_off))
                
                for card in cards: 
                    pos = input(f"{player.name} saiu lhe {card} onde quer por a carta?\n>>> ")
                    player.add_2_table(pos)
                
                print(2*"\n")

            # Player 3cards game cicle
            for bot in self.AIs_list:

                print(6*"#" + f" {bot.name} " + 6*"#")
                cards = np.array([])
               
                for _ in range(3):
                    card = self.draw_card(bot)
                    cards = np.append(cards, card)
                
                AI_move = place_cards(self, bot, cards)
                place_AI = AI_move[0]
                card_off = AI_move[1]
                
                bot.add_lixo(card_off)
                cards = np.delete(cards, np.argwhere(cards == card_off))
                
                for i in range(2):
                    j = i
                    if len(place_AI) == 1:
                        j = 0
                    if place_AI[j] == 0:
                        bot.add_2_table("top")
                    elif place_AI[j] == 1:
                        bot.add_2_table("mid")
                    else:
                        bot.add_2_table("bot")

                print(bot.field)
                print(2*"\n")

            num_cards = sum([len(player.hand) for player in self.players_list + self.AIs_list])/ (len(self.players_list) + len(self.AIs_list))
        
        print("Vamos calcular os pontos")
        for player in self.players_list + self.AIs_list:
            print(6*"#" + f"{player.name}" + 6*"#")
            print(player.field)



        #print("Na posicao top: o player1 obteve",hand_strength(player1.top),"o player2 obteve:",hand_strength(player2.top))
        #print("venceu o jogador",vencedor_linha(player1.top,player2.top))
        #print("Na posição mid o player1 obteve",hand_strength(player1.mid),"o player2 obteve:",hand_strength(player2.mid))
        #print("venceu o jogador",vencedor_linha(player1.mid,player2.mid))
        #print("Na posição bot o player1 obteve",hand_strength(player1.bot),"o player2 obteve:",hand_strength(player2.bot))
        #print("venceu o jogador",vencedor_linha(player1.bot,player2.bot))

        players_wins = self.players_list + self.AIs_list
        winner = players_wins[0]
        max_poinst = -1
        no_winners_flag = False

        for i in range(1, len(players_wins)):

            print("Na posicao top: o", winner.name,"obteve",hand_strength(winner.top),"o ", players_wins[i].name,"obteve:",hand_strength(players_wins[i].top))
            print("venceu o jogador",vencedor_linha(winner.top,players_wins[i].top))
            print("Na posição mid o ", winner.name," obteve",hand_strength(winner.mid),"o ", players_wins[i].name," obteve:",hand_strength(players_wins[i].mid))
            print("venceu o jogador",vencedor_linha(winner.mid,players_wins[i].mid))
            print("Na posição bot o ", winner.name," obteve",hand_strength(winner.bot),"o ", players_wins[i].name," obteve:",hand_strength(players_wins[i].bot))
            print("venceu o jogador",vencedor_linha(winner.bot,players_wins[i].bot))


            win = get_score(winner, players_wins[i])
            if win == 0:
                no_winners_flag = True
            elif win == 1:
                no_winners_flag = False
            else:
                no_winners_flag = False
                winner = players_wins[i]

        if no_winners_flag:
            print("No winners in this rounda")
        else:
            print(f"Congratz {winner.name}")

def main():
    jogo = Game(0,3)
    jogo.game_loop()

if __name__ == "__main__":
    main()
#def main():
#    jogo = Game() # Criação do Jogo
#    player1 = jogo.player1 # Player
#    player2 = jogo.player2 # Ai
#    print(jogo.baralho)
#    
#    # Tirar as primeiras 5 cartas para o Jogador e para a AI 
#    for _ in range(5):
#        card1 = jogo.draw_card("player1")
#        card2 = jogo.draw_card("player2")
#    
#    # Primeira Mão Player
#    print(6*"#" + " Player " + 6*"#")
#    print(f"Saiu lhe a seguinte mão {player1.hand}")
#    for i in range(5):
#        pos = input(f"Onde quer colocar {player1.hand[i]}?\n>>> ")
#        player1.add_2_table(pos)
#
#    print(2*"\n")
#
#    # Primeira Mão AI
#    print(6*"#" + " AI " + 6*"#")
#    print(f"Saiu lhe a seguinte mão {player2.hand}")
#    for i in range(5):
#        pos = input(f"Onde quer colocar {player2.hand[i]}?\n>>> ")
#        player2.add_2_table(pos)
#
#    # Ciclo de Jogo o jogo acaba quando o Jogador e a AI têm ambos 13 cartas
#    while len(player1.hand) < 13 and len(player2.hand) < 13:
#        
#        print(6*"#" + " Player " + 6*"#") # Vez do jogador 1 jogar
#        card1 = np.array([])
#        
#        for _ in range(3):
#            card = jogo.draw_card("player1")
#            card1 = np.append(card1, card)
#       
#        print(player1.field)
#        card_off = input(f"Jogador 1 saiu lhe as seguintes {card1} qual quer descartar?\n>>> ")
#        
#        while card_off not in card1:
#            card_off = input(f"Carta inválida!! {card1} qual quer descartar?\n>>> ")
#        player1.add_lixo(card_off)
#        card1 = np.delete(card1, np.argwhere(card1 == card_off))
#        
#        for card in card1: 
#            pos = input(f"Jogador 1 saiu lhe {card} onde quer por a carta?\n>>> ")
#            player1.add_2_table(pos)
#        
#        print(2*"\n")
#        
#        print(6*"#" + " Ai " + 6*"#")
#        card2 = np.array([])
#       
#        for _ in range(3):
#            card = jogo.draw_card("player2")
#            card2 = np.append(card2, card)
#       
#        print(player2.field)
#        card_off = input(f"Jogador 2 saiu lhe as seguintes {card2} qual quer descartar?\n>>> ")
#        
#        while card_off not in card2:
#            card_off = input(f"Carta inválida!! {card2} qual quer descartar?\n>>> ")
#        player2.add_lixo(card_off)
#        card2 = np.delete(card2, np.argwhere(card2 == card_off))
#        for card in card2: 
#            pos = input(f"Jogador 2 saiu lhe {card} onde quer por a carta?\n>>> ")
#            player2.add_2_table(pos)
#        
#        print(2*"\n")
#
#    """
#    print("O jogo acabou, e estes são as maos dos 2 jogadores")
#    player1.top = np.array(["KS", "KC", "QS"])
#    print("Player")
#    print(player1.field)
#    print("\nAI")
#    print(player2.field)
#    """
#    print("Vamos calcular os pontos")
#
#    #print(jogo.get_score())
#
#
#
#if __name__ == "__main__":
#    print("Projeto de PP")
#    main()
