from random import randint
'''
Класс Карта. Содержит описание одной карты.
self.number - Значение карт: строка
self.value - Стоимость карты: целое число
self.id - Порядковый номер карты
self.short_name - Краткое текстовое обозначение карты
'''
class Card:
    """
    Входные параметры
    c_id - от 1 до 104
    """
    values = (1, 2, 3, 5, 7)
    '''
    Конструктор класса
    '''
    def __init__(self,c_id):
        self.number = str(c_id)
        self.value = Card.values[0]
        if ((c_id % 5) == 0):
            self.value = Card.values[1]
        if ((c_id % 10) == 0):
            self.value = Card.values[2]
        if ((c_id % 11) == 0):
            self.value = Card.values[3]
        if ((c_id % 55) == 0):
            self.value = Card.values[4]
        self.short_name = self.number + "(" + str(self.value) + ")"
        self.id = c_id
        self.in_deck = True
        self.counts = False
    '''
    Функция вывода строкой информации о карте
    '''
    def __str__(self):
        return self.short_name + "  id: " + str(self.id) + "  очков: " + str(self.value) + "  в колоде: " + str(self.in_deck)

'''
Класс Колода карт. Содержит описание карт колоды и методы для генерации последовательности карт и отметок о выдаче карт игрокам.
self.numbers - Значения карт: строка
self.values - Стоимость карты: целое число
self.id - Краткий идентификатор карты
'''
class Deck:
    """
    Конструктор класса - создание колоды из 104 карт.
    """
    def __init__(self):
        self.max = 104
        m = range(1,self.max+1)
        self.cards = []
        for i in m:
            self.cards.append(Card(i))
    """
    Функция получения карты из колоды. Возвращает тип данных - Card. В случае если в колоде не осталось карт - выводит сообщение и возвращает Card с id -1
    """
    def get_card(self):
        got_cards = 0
        temp_number = -1
        for card in self.cards:
            if card.in_deck == True:
                got_cards += 1
        if got_cards == 0:
            print("\n\nВ колоде кончились карты!\n\n")
            return Card(-1)
        else:
            i = 0
            while True:
                temp_number = randint(0,self.max-1)
                if self.cards[temp_number].in_deck == True:
                    self.cards[temp_number].in_deck = False
                    break
                i += 1
            return self.cards[temp_number]
    """
    Функция возврата карт колоды. Возвращает все карты в колоду.
    """
    def cards_back(self):
        temp_range = range(0,self.max)
        for temp_i in temp_range:
            self.cards[temp_i].in_deck = True
'''
Класс игрока: Обладает картами, деньгами и функциями по отбору новой карты прекращению набора карт, проверки на победу и прекращения игры.
'''
class Player:
    '''
    Инициализация - обнуление очков
    '''
    def __init__(self):
        self.cards = []
        self.points = 0
        self.p_type = "Human"
    '''
    Функция сортировки карт игрока.
    '''
    def order_cards(self):
        num_cards = len(self.cards)
        mn = 0
        if(num_cards > 0):
            #Сортировка по id
            for i in range(0,num_cards-1):
                card = self.cards[i]
                mn = i
                for j in range(i+1,num_cards):
                    if card.id > self.cards[j].id:
                        card = self.cards[j]
                        mn = j
                card = self.cards[i]
                self.cards[i] = self.cards[mn]
                self.cards[mn] = card
        del card
    '''
    Функция получения игроком карты. Инициируется основной программой, на вход передается карта, полученная из колоды. 
    Пересчитываются внутренние атрибуты.
    '''
    def receive_card(self,card):
        card.counts = False
        if card.id != -1:
            self.cards.append(card)
    '''
    Функция получения игроком карты в отбой. Инициируется основной программой, на вход передается карта, полученна со стола. 
    Пересчитываются внутренние атрибуты.
    '''
    def to_trash_card(self,card):
        card.counts = True
        if card.id != -1:
            self.cards.append(card)
    '''
    Функция передачи игроком карты. Инициируется основной программой и передается на стол.
    '''
    def send_card(self):
        while True:
            a = input("\nВыберите номер карты для хода (в строке Карты игрока XX(Y): XX-номер карты, Y-количество очков):")
            num_cards = len(self.cards)
            flag = False
            out = -1
            for i in range(0,num_cards):
                if a == self.cards[i].number:
                    flag = True
                    out = i
            if flag:
                self.cards[out].counts = False
                card = self.cards[out]
                self.cards.pop(out)
                break
            else:
                print("Необходимо ввести номер карты, которой вы хотите сделать ход.\n Попробуйте еще раз.")
        return card
    '''
    Функция подсчета очков.
    '''
    def count_points(self):
        num_cards = len(self.cards)
        self.points = 0
        for i in range(0,num_cards):
            if self.cards[i].counts == True:
                self.points += self.cards[i].value
        return self.points
    '''
    Функция окончания игры: удаляет карты, подводит итог по очкам.
    '''
    def end_game(self):
        num_cards = len(self.cards)
        points = self.count_points()
        rez = "Набрано " + str(points) + " очков"
        return rez
    '''
    Функция подготовки печатной строки игрока.
    '''
    def __str__(self):
        points = self.count_points()
        str_out = f"\nОчков набрано: {points}\nКарты игрока:  "
        if len(self.cards) > 0:
            for card in self.cards:
                if card.counts == False:
                    str_out = str_out + f"{card.short_name}  "
        str_out = str_out + "\n"
        return str_out
'''
Класс компьютерного игрока.
'''
class C_player:
    '''
    Функция инициализации компьютерного игрока. Установка базовых переменных.
    '''
    def __init__(self):
        self.cards = []
        self.points = 0
        self.p_type = "PC"
        self.cards_on_table = [0]*4
    '''
    Функция сортировки карт компьютерного игрока.
    '''
    def order_cards(self):
        num_cards = len(self.cards)
        mn = 0
        if(num_cards > 0):
            #Сортировка по id
            for i in range(0,num_cards-1):
                card = self.cards[i]
                mn = i
                for j in range(i+1,num_cards):
                    if card.id > self.cards[j].id:
                        card = self.cards[j]
                        mn = j
                card = self.cards[i]
                self.cards[i] = self.cards[mn]
                self.cards[mn] = card
        del card
    '''
    Функция получения компьютерным игроком карты. Инициируется основной программой, на вход передается карта, полученная из колоды. 
    Пересчитываются внутренние атрибуты.
    '''
    def receive_card(self,card):
        card.counts = False
        if card.id != -1:
            self.cards.append(card)
    '''
    Функция получения компьютерным игроком карты. Инициируется основной программой, на вход передается карта, полученная из колоды. 
    Пересчитываются внутренние атрибуты.
    '''
    def get_cards_info(self,cards_on_top):
        for i in range(0,4):
            self.cards_on_table[i] = cards_on_top[i]
    '''
    Функция получения компьютерным игроком карты в отбой. Инициируется основной программой, на вход передается карта, полученна со стола. 
    Пересчитываются внутренние атрибуты.
    '''
    def to_trash_card(self,card):
        card.counts = True
        if card.id != -1:
            self.cards.append(card)
    '''
    Функция передачи компьютерным игроком карты. Инициируется основной программой и передается на стол.
    Компьютер выбирает случайную карту из имеющихся у него.
    '''
    def send_card(self):
        got_cards = len(self.cards)
        if self.p_type == "PC1":
            while True:
                card_index = randint(0,got_cards-1)
                if self.cards[card_index].counts == False:
                    break
            self.cards[card_index].counts = False
            card = self.cards[card_index]
            self.cards.pop(card_index)
        else:
            crit = [[0 for _ in range(got_cards)] for _ in range(4)]
            for k in range(0,4):
                for i in range(0,got_cards):
                    if self.cards[i].counts == True:
                        crit[k][i] = -1000
                    else:
                        crit[k][i] = self.cards[i].id - self.cards_on_table[k]
            mini = 1000
            temp_i = 0
            for k in range(0,4):
                for i in range(0,got_cards):
                    if crit[k][i] > 0 and mini > crit[k][i]:
                        mini = crit[k][i]
                        temp_i = i
            if mini != 1000:
                card = self.cards[temp_i]
                self.cards.pop(temp_i)
            else:
                while True:
                    card_index = randint(0,got_cards-1)
                    if self.cards[card_index].counts == False:
                        break
                self.cards[card_index].counts = False
                card = self.cards[card_index]
                self.cards.pop(card_index)
        return card
    '''
    Функция подсчета очков.
    '''
    def count_points(self):
        num_cards = len(self.cards)
        self.points = 0
        for i in range(0,num_cards):
            if self.cards[i].counts == True:
                self.points += self.cards[i].value
        return self.points
    '''
    Функция окончания игры: удаляет карты, подводит итог по очкам.
    '''
    def end_game(self):
        num_cards = len(self.cards)
        points = self.count_points()
        rez = "Компьютер набрал " + str(points) + " очков"
        return rez
    '''
    Функция подготовки печатной строки компьютерного игрока.
    '''
    def __str__(self):
        points = self.count_points()
        str_out = f"\nОчков набрал {self.p_type}: {points}\nКарты компьютера:  "
        if len(self.cards) > 0:
            for card in self.cards:
                if card.counts == False:
                    str_out = str_out + f"##(#)  " #Для отображения карт компа, заменить на {card.short_name}
        return str_out
'''
Класс Игровой стол. Содержит 4 стопки карт, растущих до 6 карт и сбрасывающих 5 карт в таком случае игроку, положившему 6 карту.
self.numbers - Значения карт: строка
self.values - Стоимость карты: целое число
self.id - Краткий идентификатор карты
'''
class Table:
    """
    Конструктор класса - создание 4х стопок и помещение туда первых 4 карт.
    """
    def __init__(self,card1,card2,card3,card4):
        self.max = 6
        self.a_cards = []
        self.b_cards = []
        self.c_cards = []
        self.d_cards = []
        self.a_cards.append(card1)
        self.b_cards.append(card2)
        self.c_cards.append(card3)
        self.d_cards.append(card4)
    """
    Функция получения карты от игрока. Стол получает карту и проверяет по условиям игры: если карта
    игрока меньше всех крайних карт стопок - игрок забирает стопку карт по своему выбору (а функция возвращает 
    номер стопки, отдаваемой игроку в отбой). Карта, переданная игроком, становится первой вместо стопки, которая 
    была отдана игроку в отбой.
    """
    def get_card(self,card,p_type):
        a_len = len(self.a_cards)
        b_len = len(self.b_cards)
        c_len = len(self.c_cards)
        d_len = len(self.d_cards)
        delta = [0,0,0,0]
        delta[0] = card.id - self.a_cards[a_len-1].id
        delta[1] = card.id - self.b_cards[b_len-1].id
        delta[2] = card.id - self.c_cards[c_len-1].id
        delta[3] = card.id - self.d_cards[d_len-1].id
        #Если у игрока карта не подходит ни к одной из стопок - спросить, какую он заберет. ПК берет с минимальными очками.
        if delta[0] < 0 and delta[1] < 0 and delta[2] < 0 and delta[3] < 0:
            if p_type == "Human":
                print("\nВаша карта не подходит ни одной из стопок.")
                while True:
                    a = input("Выберите стопку, которую желаете забрать (введите номер стопки от 1 до 4):")
                    if a == "1" or a == "2" or a == "3" or a == "4":
                        break
                    else:
                        print("\nНеобходимо выбрать одну из четырех стопок. Введите число от 1 до 4.\nпопробуйте еще раз.\n")
            if p_type == "PC1" or p_type == "PC2":
                a = self.min_points_num()
            if a == "1":
                self.a_cards.append(card)
            if a == "2":
                self.b_cards.append(card)
            if a == "3":
                self.c_cards.append(card)
            if a == "4":
                self.d_cards.append(card)
            return int(a)
        else:#Если карта подходит в одну из стопок - проверить не 6-я ли она.
            for i in range(0,4):
                if delta[i] < 0:
                    delta[i] = 1000
            min = delta[0]
            mn = 0
            for i in range(1,4):
                if delta[i] < min:
                    min = delta[i]
                    mn = i
            if mn == 0:
                self.a_cards.append(card)
                a_len = len(self.a_cards)
                if a_len < 6:
                    b = 0
                else:
                    b = 1
            if mn == 1:
                self.b_cards.append(card)
                b_len = len(self.b_cards)
                if b_len < 6:
                    b = 0
                else:
                    b = 2
            if mn == 2:
                self.c_cards.append(card)
                c_len = len(self.c_cards)
                if c_len < 6:
                    b = 0
                else:
                    b = 3
            if mn == 3:
                self.d_cards.append(card)
                d_len = len(self.d_cards)
                if d_len < 6:
                    b = 0
                else:
                    b = 4
            return b
    """
    Функция получения номеров 4-х карт со стола
    """
    def get_card_nums(self):
        cards_on_top = [0]*4
        step_len = len(self.a_cards)
        cards_on_top[0] = self.a_cards[step_len-1].id
        step_len = len(self.b_cards)
        cards_on_top[1] = self.b_cards[step_len-1].id
        step_len = len(self.c_cards)
        cards_on_top[2] = self.c_cards[step_len-1].id
        step_len = len(self.d_cards)
        cards_on_top[3] = self.d_cards[step_len-1].id
        return cards_on_top
    """
    Функция передачи карты из стопки d_num в отбой игрока. Возвращает тип данных - Card - нулевая карта стопки.
    """
    def send_card(self, d_num):
        if d_num == 1:
            d_len = len(self.a_cards)
            card = self.a_cards[0]
            self.a_cards.pop(0)
        if d_num == 2:
            d_len = len(self.b_cards)
            card = self.b_cards[0]
            self.b_cards.pop(0)
        if d_num == 3:
            d_len = len(self.c_cards)
            card = self.c_cards[0]
            self.c_cards.pop(0)
        if d_num == 4:
            d_len = len(self.d_cards)
            card = self.d_cards[0]
            self.d_cards.pop(0)
        return card
    '''
    Функция вывода номера стопки с минимальным количеством очков.
    '''
    def min_points_num(self):
        s_len = [0]*4
        s_sum = [0]*4
        s_len[0] = len(self.a_cards)
        s_len[1] = len(self.b_cards)
        s_len[2] = len(self.c_cards)
        s_len[3] = len(self.d_cards)
        s_sum[0] = 0
        for i in range(0,s_len[0]):
            s_sum[0] += self.a_cards[i].value
        s_sum[1] = 0
        for i in range(0,s_len[1]):
            s_sum[1] += self.b_cards[i].value
        s_sum[2] = 0
        for i in range(0,s_len[2]):
            s_sum[2] += self.c_cards[i].value
        s_sum[3] = 0
        for i in range(0,s_len[3]):
            s_sum[3] += self.d_cards[i].value
        min = s_sum[0]
        i_min = 0
        for i in range(1,4):
            if s_sum[i] < min:
                i_min = i
                min = s_sum[i]
        return str(i_min+1)
    '''
    Функция вывода количества карт в стопке d_num.
    '''
    def cards_amount(self, d_num):
        d_sum = 0
        if d_num == 1:
            d_sum = len(self.a_cards)
        if d_num == 2:
            d_sum = len(self.b_cards)
        if d_num == 3:
            d_sum = len(self.c_cards)
        if d_num == 4:
            d_sum = len(self.d_cards)
        return d_sum
    '''
    Функция печати строкой содержимого стола.
    '''
    def __str__(self):
        a_len = len(self.a_cards)
        b_len = len(self.b_cards)
        c_len = len(self.c_cards)
        d_len = len(self.d_cards)
        outstr = "\n\n1:  "
        for i in range(0,a_len):
            outstr += self.a_cards[i].short_name + " "
            t = 3 - len(self.a_cards[i].number)
            for p in range(0,t):
                outstr += " "
        outstr += "\n2:  "
        for i in range(0,b_len):
            outstr += self.b_cards[i].short_name + " "
            t = 3 - len(self.b_cards[i].number)
            for p in range(0,t):
                outstr += " "
        outstr += "\n3:  "
        for i in range(0,c_len):
            outstr += self.c_cards[i].short_name + " "
            t = 3 - len(self.c_cards[i].number)
            for p in range(0,t):
                outstr += " "
        outstr += "\n4:  "
        for i in range(0,d_len):
            outstr += self.d_cards[i].short_name + " "
            t = 3 - len(self.d_cards[i].number)
            for p in range(0,t):
                outstr += " "
        outstr += "\n"
        return outstr