from random import sample, randrange
import itertools
import time
from hand_strength import hand_strength
from collections import Counter
import numpy as np
from royalties import aux_royals_top, aux_royals_mid, aux_royals_bot, royals

class Sim_Game:
    """
    Class responsavel por simular as maos, uma dada pontuacaop e atribuida a cada uma das jogadas
    tendo em conta se ganha a linha ou nao, tendo em conta a pontuacao extra dada peloos royalty
    poinst a 'AI' dispoem as cartas que tem na mao de todas as maneiras possiveis e recolhe do 
    baralho o resto da cartas para completar o seu jogo, calulando assim o pontuacao final do jogo,
    a forma que as cartas que a AI usa para completar o seu jogo sao dispostas na mesa de forma 
    completamente aleatoria

    game -> Classe de jogo (onde esta defenido o baralho e os jogadore)
    player -> Classe do jogador que a 'AI' vai controlar 
    cards_to_place -> cartas que a 'AI' tem na mao
    order_to_place -> forma como as cartas que a 'AI' tem na mao sao dispostas na mesa
    card_off -> para as rondas onde a 'AI' recebe 3 cartas uma delas tem que ser discartada (card_off)
    """
    def __init__(self, game, player, cards_to_place, order_to_place, card_off):
        """
        Inicializacao da class 
            -Dispoe as cartas na mesa usando o tuplo order_to_place
            -Inicializacao de variavies
            -Criacao do baralho
        """
        self.hand = {} 
        self.hand["top"] = list(player.top[:])
        self.hand["mid"] = list(player.mid[:])
        self.hand["bot"] = list(player.bot[:])
        self.order_to_place = order_to_place
        self.card_off = card_off
        for i in range(len(cards_to_place)):
            if order_to_place[i] == 0:
                self.hand["top"] += [cards_to_place[i]]
            elif order_to_place[i] == 1:
                self.hand["mid"] += [cards_to_place[i]]
            else: 
                self.hand["bot"] += [cards_to_place[i]]
        self.evs_ar = np.array([])
        self.times_run = 0
        self.enemies = game.players_list + game.AIs_list
        self.enemies.remove(player)
        get_trash = lambda x: x.lixo
        self.trash = []
        for player in self.enemies:
            self.trash += list(player.lixo)

        self.deck = np.concatenate((game.baralho[:], np.array(self.trash)), axis=None)

    def run_hand(self):
        """
        Uma simulacao de Monte Carlo:
            -Distribui cartas de forma aleatoria
            -Calcula os pontos desse jogo
        """
        en_roya = []
        run_handb = {}
        run_handb["top"] = self.hand["top"][:]
        run_handb["mid"] = self.hand["mid"][:]
        run_handb["bot"] = self.hand["bot"][:]
        
        top_len = len(run_handb["top"])
        mid_len = len(run_handb["mid"])
        bot_len = len(run_handb["bot"])
        
        card_samp = sample(list(self.deck), 13-top_len-mid_len-bot_len)

        if(top_len < 3):
            run_handb["top"] += card_samp[:3-top_len]
        if(mid_len < 5):
            run_handb["mid"] += card_samp[3-top_len:3-top_len+5-mid_len]
        if(bot_len < 5):    
            run_handb["bot"] += card_samp[3-top_len+5-mid_len:3-top_len+5-mid_len+5-bot_len]
        
        top_strb = hand_strength(run_handb["top"]) 
        mid_strb = hand_strength(run_handb["mid"])
        bot_strb = hand_strength(run_handb["bot"])
        
        enemies_points = []
        for player in self.enemies:
            
            run_hand = {}
            run_hand["top"] = list(player.top[:])
            run_hand["mid"] = list(player.mid[:])
            run_hand["bot"] = list(player.bot[:])
            
            top_len = len(run_hand["top"])
            mid_len = len(run_hand["mid"])
            bot_len = len(run_hand["bot"])
            
            card_samp = sample(list(self.deck), 13-top_len-mid_len-bot_len)

            if(top_len < 3):
                run_hand["top"] += card_samp[:3-top_len]
            if(mid_len < 5):
                run_hand["mid"] += card_samp[3-top_len:3-top_len+5-mid_len]
            if(bot_len < 5):    
                run_hand["bot"] += card_samp[3-top_len+5-mid_len:3-top_len+5-mid_len+5-bot_len]
            
            top_str = hand_strength(run_hand["top"]) 
            mid_str = hand_strength(run_hand["mid"])
            bot_str = hand_strength(run_hand["bot"])
            
            if top_str > mid_str or top_str > bot_str or mid_str > bot_str:
                top_str = -1
                mid_str = -1
                bot_str = -1

            enemies_points += [{
                    "top": top_str,
                    "mid" : mid_str,
                    "bot" : bot_str}]

        en_roya += [aux_royals_top(run_hand["top"])+aux_royals_mid(run_hand["mid"])+aux_royals_bot(run_hand["bot"])]

        if top_strb > mid_strb or top_strb > bot_strb or mid_strb > bot_strb:
            self.ev = -6
        else:
            self.ev = aux_royals_top(run_hand["top"])+aux_royals_mid(run_hand["mid"])+aux_royals_bot(run_hand["bot"])
            i = 0
            for enemie in enemies_points:
                try:
                    self.ev -= en_roya[i]
                except:
                    pass
                i += 1
                if top_strb >= enemie["top"]:
                    self.ev += 1
                else:
                    self.ev -= 1
                if mid_strb >= enemie["mid"]:
                    self.ev += 3
                else:
                    self.ev -= 1
                if top_strb >= enemie["bot"]:
                    self.ev += 6
                else:
                    self.ev -= 1


        self.evs_ar = np.append(self.evs_ar, self.ev)
        self.times_run += 1
        
        return "One game simulation"

    def get_ev_ave(self):
        """
        Calcula a media de pontos de cada mao
        """
        return sum(self.evs_ar)/self.times_run

def place_cards(game, player, cards_to_place, thread_scale = 5,  monte_carlo_stats=True):
    """
    Funca responsavel por escolher a melhor mao de todas as maos simuladas

    game -> Jogo em causa
    player -> Jogador que a AI vai controlar
    cards_to_place -> Cartas que o bot tem na mao
    thread_scale -> Nivel de difculdade, diretamente proporcional ao tempode de execucao
    monte_carlo_stats -> Mostra Info extra 
    """
    possible_hands = []
    possible_placements = []

    if len(player.top) < 3:
        possible_placements.append(0)
    if len(player.mid) < 5:
        possible_placements.append(1)
    if len(player.bot) < 5:
        possible_placements.append(2)
    
    for p in itertools.product(possible_placements, repeat=len(cards_to_place)):
        
        iter_off = dict(Counter(p))
        if len(cards_to_place) == 3:
            iter_off = dict(Counter(p[1:]))
        
        try:
            iter_off0 = iter_off[0]
        except:
            iter_off0 = 0
        try:
            iter_off1 = iter_off[1] 
        except:
            iter_off1 = 0
        try:
            iter_off2 = iter_off[2] 
        except:
            iter_off2 = 0

        if len(player.top) + iter_off0 > 3 or len(player.mid) + iter_off1 > 5 or len(player.bot) + iter_off2 > 5:
            continue
        else:
            card_off = None
            cards_to_place_on_sim = cards_to_place[:]
            p_on_sim = p[:]
            if len(cards_to_place) == 3:
                card_off = cards_to_place[p[0]]
                cards_to_place_on_sim = cards_to_place[1:]
                p_on_sim = p[1:]
            possible_hands.append(Sim_Game(game, player, cards_to_place_on_sim, p_on_sim, card_off))

    # Tempo para as simulacoes (defenido por um thread scale (dificuldade), mais tempo => jogadas mais "pensadas"
    start = time.time()
    fivecardtime = thread_scale + 5
    twocardtime = thread_scale//2 + 3
    max_time = fivecardtime if len(cards_to_place) == 5 else twocardtime
    
    num_sims = 0
    
    while(time.time() - start < max_time):
        for hand in possible_hands:
            hand.run_hand()
        num_sims += 1

    best_ev = -200
    for pos_hand in possible_hands:
        if pos_hand.get_ev_ave() > best_ev:
            best_ev = pos_hand.get_ev_ave()
            best_order_to_place = pos_hand.order_to_place
            card_off = pos_hand.card_off
    
    if monte_carlo_stats:
        explanation = f"After {num_sims} Monte Carlo simulations the AI thinks it can make {best_ev} points, on average, of {len(possible_hands)} possible hands"
        print(explanation)
    return best_order_to_place, card_off
