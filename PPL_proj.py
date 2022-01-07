import numpy as np
from player import *
from hand_strength import get_score, hand_strength, vencedor_linha
from bot import place_cards
from royalties import pontos2,pontos3

class Game:
    def __init__(self, n_players, n_AIs, thread_scale,num_jogadores = 1):
        """
        Class associada ao jogo de Poker, onde temos um baralho de 52 cartas,
        \'2,3,4,5,6,7,8,9,10,J,Q,K,A\' com 4 nipes cada uma das cartas
        \'S\' - Spades
        \'H\' - Hearts
        \'C\' - Clubs
        \'D\' - Diamons
        """
        self.thread_scale = thread_scale
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
        self.run_game_until()

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
            
            place_AI = place_cards(self, bot, bot.hand, self.thread_scale)[0]
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
                print(6*"#" + f" {player.name} " + 6*"#") # Vez do jogador 1 jogar
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
                
                AI_move = place_cards(self, bot, cards, self.thread_scale)
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
            print(6*"#" + f" {player.name} " + 6*"#")
            print(player.field)

        players_wins = self.players_list + self.AIs_list
        winner = players_wins[0]
        max_poinst = -1
        no_winners_flag = False
        if len(players_wins)==2:
            pontos = pontos2(players_wins[0],players_wins[1])
        elif len(players_wins)==3:         
            pontos = pontos3(players_wins[0],players_wins[1],players_wins[2])
            
        for point, player in zip(pontos, players_wins):
            player.update_points(point)
            print(f"{player.name}: {player.points}")

    def run_game_until(self, points_th = 5):
        max_point = 0
        
        while max_point < points_th:
            self.game_loop()
            max_point = 0
            players_list = self.players_list + self.AIs_list
            for i in range(len(self.players_list) + len(self.AIs_list)):
                max_point = max(max_point, players_list[i].points)
            self.baralho = self.create_deck()
            players = self.players_list + self.AIs_list

            for player in players:
                player.reset()
def main():
    jogo = Game(0,3,0)

if __name__ == "__main__":
    main()
