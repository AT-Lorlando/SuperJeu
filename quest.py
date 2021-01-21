from item import *

class Quest():
    def __init__(self, ID,rewards_tab,text_dialogue):
        self.ID = ID
        self.rewards = rewards_tab    
        self.xp = 500
        self.money = 500
        self.goal = None
        self.text_dialogue = text_dialogue
        self.is_finished = False

    def give_rewards(self, player):
        for reward in self.rewards:
            player.inv.add_without_case(reward)
        player.gain_money(self.money)
        player.gain_xp(self.xp)

    def give_up(self, player):
        if self in player.quest_list:
            player.quest_list.remove(self)
        
    def is_complete(self, player):
        pass

    def congrats(self, player):
        self.give_rewards(player)
        player.quest_list.remove(self)
        player.finished_quest.append(self.ID)
        self.is_finished = True

class Lost_Item_Quest(Quest):
    def __init__(self, ID, rewards_tab, needed_tab,text_dialogue):
        super(Lost_Item_Quest,self).__init__(ID,rewards_tab,text_dialogue)
        self.needed = needed_tab
        self.goal = f'QUEST {self.ID}: You have to find {[item.name for item in self.needed]}.'

    def is_complete(self, player):
        return all([player.inv.is_in(item) for item in self.needed])

    def congrats(self, player):
        self.give_rewards(player)
        for item in self.needed:
            player.inv.remove(item)
        player.quest_list.remove(self)
        player.finished_quest.append(self.ID)
        self.is_finished = True

Gime_apple = Lost_Item_Quest(12112, [Empowered_Sword],[Item(192, "Apple"), Item(202, "Meat")], ["Bonjour M.Hugo", "Désolé, je ne peux pas trop vous parler", "Je dois absolument faire la récolte de mon champ !", "Malheureusement, je viens de casser ma pelle...","Pouvez vous allez m'en acheter une ?", "Le marchand se trouve juste à gauche !",  "Je vous recompenserais !"])
Lost_ring_Quest = Lost_Item_Quest(23112, [Empowered_Staff],[Lost_ring], ["Coucou", "J'ai perdu ma bague", "Aled"])


QUEST_DICT = {12112: Gime_apple, 23112: Lost_ring_Quest}