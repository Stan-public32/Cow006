from Card_Deck import Card
from Card_Deck import Deck
from Card_Deck import Player
from Card_Deck import C_player
from Card_Deck import Table

#Создание колоды карт.
deck = Deck()
#Создание экземпляра класса Игрок.
player = Player()
#Создание экземпляра класса Стол.
table = Table(deck.get_card(),deck.get_card(),deck.get_card(),deck.get_card())
#Создание экземпляра класса Компьютерный игрок.
c_player = C_player()
c_player2 = C_player()
c_player.p_type += "1"
c_player2.p_type += "2"
#Создание списка карт для хождения Карта.
r_cards = [0]*3
p_types = [0]*3

#Начинается игровой цикл, который длится 10 раундов. Для начала игроку и компьютеру раздают по 10 карт.
for i in range(0,10):
    player.receive_card(deck.get_card())
    c_player.receive_card(deck.get_card())
    c_player2.receive_card(deck.get_card())
player.order_cards()
c_player.order_cards()
c_player2.order_cards()
#Запуск 10 раундов, где игрок и компьютер пытаются скинуть как можно больше карт, не забрав ничего в ответ.
for j in range(0, 10):
    print("\n\n")
    print(c_player)
    print(c_player2)
    print(table)
    print(player)
    #Ход игрока, ПК и по его результатам игрок/ПК либо ничего не берет (action_type = 0), либо берет стопку 1-4 по значению action_type.
    r_cards[0] = player.send_card()
    p_types[0] = player.p_type
    r_cards[1] = c_player.send_card()
    p_types[1] = c_player.p_type
    r_cards[2] = c_player2.send_card()
    p_types[2] = c_player2.p_type
    #Отображение кто чем походил
    print(f"\n-----------------------------\n\nИгрок пошел картой: {r_cards[0].short_name}")
    print(f"Компьютер 1 пошел картой: {r_cards[1].short_name}")
    print(f"Компьютер 2 пошел картой: {r_cards[2].short_name}\n")
    #Определим последовательность обработки по росту номинала карт (id).
    for k in range(0,len(r_cards)-1):
        c_min = r_cards[k]
        pt_min = p_types[k]
        min_crit = r_cards[k].id
        i_min = k
        for i in range(1,len(r_cards)):
            if min_crit > r_cards[i].id:
                c_min = r_cards[i]
                pt_min = p_types[i]
                min_crit = r_cards[i].id
                i_min = i
        r_cards[i_min] = r_cards[k]
        p_types[i_min] = p_types[k]
        r_cards[k] = c_min
        p_types[k] = pt_min
    #В r_cards и p_types лежат карты игрока и компьютера по возрастанию id и отработка правил пополнения стопок стола с возвратами в отбой.
    for k in range(0,len(r_cards)):
        action_type = table.get_card(r_cards[k],p_types[k])
        if action_type == 1 or action_type == 2 or action_type == 3 or action_type == 4:
            c_amount = table.cards_amount(action_type)
            for i in range(0, c_amount-1):
                if p_types[k] == player.p_type:
                    player.to_trash_card(table.send_card(action_type))
                if p_types[k] == c_player.p_type:
                    c_player.to_trash_card(table.send_card(action_type))
                if p_types[k] == c_player2.p_type:
                    c_player2.to_trash_card(table.send_card(action_type))
#По итогам 10 раундов еще раз вывести содержимое на экран.
print(c_player)
print(c_player2)
print(table)
print(player)
#Определение победителя.
win_flag = True
if player.points > c_player.points or player.points > c_player2.points:
    win_flag = False
if win_flag:
    print("\nПоздравляю вас с победой!!!\n\n")
else:
    print("\nК сожалению, вы проиграли (((\n\n")
print("\nКонец игры. Спасибо за внимание!\nНадеюсь, вам понравилось!")