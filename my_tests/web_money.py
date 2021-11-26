class Pocket():
    '''Класс электронного кошелька с тремя видами валюты
    UAH, USD, EUR. Кошелек умеет добавлять на счет в соответствующей валюте,
    вычитать в одинаковой валюте, выводить на экран баланс, конвертировать одну валюту в другую ....'''

    def __init__(self, uah=0, usd=0, eur=0):
        self.uah = uah
        self.usd = usd
        self.eur = eur
        self.usd_rate_by = 27.2     # купить за гривну
        self.usd_rate_sell = 26.9   # продать за гривну
        self.eur_rate_by = 30.6     # купить за гривну
        self.eur_rate_sell = 30.2   # продать за гривну
        self.usd_in_eur = 0.88      # usd -> eur
        self.eur_in_usd = 1.11      # eur -> usd

    def add_money(self, money, valute): # добавление денег
        '''метод добавляет на счет указаную сумму. Указываем число на которое увеличиваем счет и валюту'''
        if valute in ['uah', 'грн']:
            self.uah += money
        elif valute in ['usd', 'долл', '$']:
            self.usd += money
        elif valute in ['eur', 'евро']:
            self.eur += money

    def dif_money(self, money, valute): # снятие денег
        '''метод вычитает с счета. Указываем сколько вычесть и с какой валюты'''
        if valute in ['uah', 'грн']:
            if self.uah < money:
                print('Not enough UAH!')
            else:
                self.uah -= money
        elif valute in ['usd', 'долл', '$']:
            if self.usd < money:
                print('Not enough USD!')
            else:
                self.usd -= money
        elif valute in ['eur', 'квро']:
            if self.eur < money:
                print('Not enough EUR!')
            else:
                self.eur -= money

    def show_my_money(self): # показать баланс
        '''метод показывает баланс на веб кошельке'''
        print(f'У Вас: \n {self.uah} грн. \n {self.usd} долл. \n {self.eur} евро.')

    def convert(self, how, from_valute, in_valute):
        '''метод конвертирует одну валюту в другую
        В метод передаем сколько конвертируем, какую валюту в какую валюту'''
        if from_valute in ['usd', 'долл', '$']: # конвертируем из доллара
            self.dif_money(how, from_valute)
            if in_valute in ['uah', 'грн']: # в гривну
                self.add_money(how * self.usd_rate_sell, in_valute)
            if in_valute in ['eur', 'евро']:    # в евро
                self.add_money(how * self.usd_in_eur, in_valute)
        elif from_valute in ['eur', 'евро']:    # конвертируем из евро
            self.dif_money(how, from_valute)
            if in_valute in ['uah', 'грн']: # в гривну
                self.add_money(how * self.eur_rate_sell, in_valute)
            elif in_valute in ['usd', 'долл', '$']: # в доллары
                self.add_money(how * self.eur_in_usd, in_valute)
        elif from_valute in ['uah', 'грн']: # конвертируем из гривны
            self.dif_money(how, from_valute)
            if in_valute in ['usd', 'долл', '$']:   # в доллары
                self.add_money(how * self.usd_rate_by, in_valute)
            elif in_valute in ['eur', 'евро']:  # в евро
                self.add_money(how * self.eur_rate_by, in_valute)



my_pocket = Pocket(0, 100, 0)
my_pocket.show_my_money()
# my_pocket.convert(10, 'usd', 'грн')
# my_pocket.convert(10, '$', 'евро')
my_pocket.convert(100, 'usd', 'eur')
my_pocket.convert(50, 'eur', 'uah')
my_pocket.convert(10, 'uah', 'usd')
my_pocket.show_my_money()

