# from generators import get_user_data
from abc import ABC, abstractmethod


class AccountBase(ABC):
    def __init__(self, name, passport8, phone_number, start_balance=0):
        self.name = name
        self.passport8 = passport8
        self.phone_number = phone_number
        self.balance = start_balance

    @abstractmethod
    def transfer(self, target_account, amount):
        """
        Перевод денег на счет другого клиента
        :param target_account: счет клиента для перевода
        :param amount: сумма перевода
        :return:
        """
        pass

    @abstractmethod
    def deposit(self, amount):
        """
        Внесение суммы на текущий счет
        :param amount: сумма
        """
        pass

    @abstractmethod
    def withdraw(self, amount):
        """
        Снятие суммы с текущего счета
        :param amount: сумма
        """
        pass

    @abstractmethod
    def full_info(self):
        """
        Полная информация о счете в формате: "Иванов Иван Петрович баланс: 100 руб. паспорт: 12345678 т.89002000203"
        """
        return f"..."

    @abstractmethod
    def __repr__(self):
        """
        :return: Информацию о счете в виде строки в формате "Иванов И.П. баланс: 100 руб."
        """
        return f"..."


class Operation:
    DEPOSIT = 'пополнение'
    WITHDRAW = 'снятие'
    TRANSFER = 'перевод'
    INCOME = 'поступление'

    def __init__(self, type, amount, fee=0, target=None, sender=None):
        self.type = type
        self.amount = amount
        self.fee = fee
        self.target = target
        self.sender = sender

    def __str__(self):
        if self.target is not None:
            target_name = self.target
            return f'Операция: {self.type}, на сумму: {self.amount}, на счет: {target_name}, коммисия: {self.amount * (self.fee / 100)}'
        elif self.sender is not None:
            sender_name = self.sender
            return f'Операция: {self.type}, на сумму: {self.amount}, от: {sender_name}, коммисия: {self.amount*(self.fee / 100)}'
        else:
            return f'Операция: {self.type}, на сумму: {self.amount}, коммисия: {self.amount * (self.fee / 100)}'


class Account(AccountBase):
    FEE = 2

    def __init__(self, name, passport8, phone_number, start_balance=0):
        AccountBase.__init__(self, name, passport8, phone_number, start_balance)
        self.history = []
        self.in_archive = False
        revision = self.passport8.split(' ')
        if len(revision[0]) != 4 or len(revision[1]) != 6:
            raise ValueError("Incorrect format of the passport number(need: xxxx  xxxxxx)")
          #"+7-xxx-xxx-xx-xx"
        area1 = self.phone_number[3:6]
        area2 = self.phone_number[7:10]
        area3 = self.phone_number[11:13]
        area4 = self.phone_number[-2:]
        if self.phone_number != f'+7-{area1}-{area2}-{area3}-{area4}':
            raise ValueError("Please insert your phone number in format: +7-xxx-xxx-xx-xx")

    @property
    def fee(self):
       return self.FEE

    @staticmethod
    def validation_passport(self):
        pass

    @staticmethod
    def validation_passport(self):
        pass

    def transfer(self, target_account, amount, record=True):
        if self.in_archive == False:
            self.withdraw(amount, record=False)
            target_account.deposit(amount, record=False)
            if record:
                op = Operation(Operation.TRANSFER, amount, target=target_account.name, fee=self.fee)
                self.history.append(op)
                op = Operation(Operation.INCOME, amount, sender=self.name, fee=self.fee)
                target_account.history.append(op)

    def deposit(self, amount, record=True):
        if self.in_archive == False:
            self.balance += amount
            if record:
                op = Operation(Operation.DEPOSIT, amount)
                self.history.append(op)

    def __enough_money(self, amount):
        return self.balance < amount * (1 + self.fee/100)

    def withdraw(self, amount, record=True):
        if self.in_archive == False:
            if self.__enough_money(amount):
                raise ValueError("Isn't enough money")
            self.balance -= amount * (1 + self.fee/100)
            if record:
                op = Operation(Operation.WITHDRAW, amount, fee=self.fee)
                self.history.append(op)

    def full_info(self):
        return f"{self.name} баланс: {self.balance} руб. паспорт: {self.passport8} т.{self.phone_number}"

    def __repr__(self):
        return f"{self.name} баланс: {self.balance} руб."

    def show_history(self):
        hist_str = ''
        for operation in self.history:
            hist_str += str(operation) + '\n'
        return hist_str

    def to_archive(self):
        self.balance = 0
        self.in_archive = True

    def restore(self):
        self.in_archive = False


class CreditAccount(Account):
    POSITIVE_FEE = 2
    NEGATIVE_FEE = 5

    def __init__(self, name, passport8, phone_number, start_balance=0, negative_limit=-1000):
        Account.__init__(self, name, passport8, phone_number, start_balance)
        self.__negative_limit = negative_limit
        self.history = []
        self.in_archive = False

    def __repr__(self):
        return f"{self.name} K-account баланс: {self.balance} руб."

    def full_info(self):
        return f"<К> account: {self.name} баланс: {self.balance} руб. паспорт: {self.passport8} т.{self.phone_number}"

    def __enough_money(self, amount):
        return (self.balance + abs(self.__negative_limit)) < amount * (1 + self.fee / 100)

    @property
    def fee(self):
        if self.balance < 0:
            return self.NEGATIVE_FEE
        else:
            return self.POSITIVE_FEE

    def withdraw(self, amount, record=True):
        if self.__enough_money(amount):
            raise ValueError("Isn't enough money")
        self.balance -= amount * (1 + self.fee / 100)
        if record:
            op = Operation(Operation.WITHDRAW, amount, fee=self.fee)
            self.history.append(op)

    def transfer(self, target_account, amount, record=True):
        self.withdraw(amount, record=False)
        target_account.deposit(amount, record=False)
        if record:
            op = Operation(Operation.TRANSFER, amount, target=target_account.name, fee=self.fee)
            self.history.append(op)
            op = Operation(Operation.INCOME, amount, sender=self.name, fee=self.fee)
            target_account.history.append(op)

    def show_history(self):
        hist_str = ''
        for operation in self.history:
            hist_str += str(operation) + '\n'
        return hist_str

    def to_archive(self):
        if self.balance < 0:
            raise ValueError('Невозможно закрыть аккаунт с отрицательным балансом')
        else:
            self.balance = 0
            self.in_archive = True

    def restore_from_archive(self):
        self.in_archive = False




#try:
#    account1 = Account('Ivan', 24655387, '+7987-321-87-43')
#except ValueError as e:
#    print(e)
# try:
#     account2 = Account('Olga', 23424385, '59300')
# except ValueError as e:
#     print(e)
#try:
#    account2 = Account('Olga', 234385, '+7977-321-34-65')
#except ValueError as e:
#    print(e)

#account1.deposit(612)
#account1.withdraw(100)

# #account1.transfer(account2, 250)
#
# print(account1.show_history())
#
# account1.closing()
# account1.deposit(1000)
# print(account1)
