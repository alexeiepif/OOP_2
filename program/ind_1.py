#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Выполнить индивидуальное задание 2 лабораторной работы 4.1,
# максимально задействовав имеющиеся в Python
# средства перегрузки операторов.


class AccountOwner:
    def __init__(self, owner: str):
        self.__owner = owner

    def read(self):
        self.__owner = input("Введите владельца счета: ")

    @property
    def owner(self) -> str:
        return self.__owner

    @owner.setter
    def owner(self, new_owner: str):
        self.__owner = new_owner


class AccountBalance:
    def __init__(self, balance: float):
        self.__balance = balance

    # @property
    # def balance(self):
    #     return self.__balance

    # @balance.setter
    # def balance(self, new_balance: float):
    #     self.__balance = new_balance

    def __iadd__(self, rhs: float):  # +=
        self.__balance += rhs
        return self

    def __isub__(self, rhs: float):  # -=
        self.__balance -= rhs
        return self

    def __lt__(self, rhs: float):  # <
        return self.__balance < rhs

    def __mul__(self, rhs: float):  # *
        return self.__balance * rhs

    def __int__(self):  # int
        return int(self.__balance)

    def __str__(self):  # str
        return str(self.__balance)


class BalanceOperations:
    def __init__(self, acc_balance: AccountBalance):
        self.__acc_balance = acc_balance

    def withdraw(self, amount: float):
        if self.__acc_balance < amount:
            print("Недостаточно средств на счете.")
        else:
            self.__acc_balance -= amount

    def deposit(self, amount: float):
        self.__acc_balance += amount


class InterestConverter:
    def __init__(self, acc_balance: AccountBalance, interest_rate: float):
        self.__acc_balance = acc_balance
        self.__interest_rate = interest_rate

    def add_interest(self):
        self.__acc_balance += self.__acc_balance * self.__interest_rate


class СurrencyConverter:
    def __init__(
        self,
        acc_balance: AccountBalance,
        rub_dollar_rate: float,
        rub_eur_rate: float,
    ):
        self.__acc_balance = acc_balance
        self.__rub_dollar_rate = rub_dollar_rate
        self.__rub_eur_rate = rub_eur_rate

    def convert_to_usd(self):
        return self.__acc_balance * self.__rub_dollar_rate

    def convert_to_eur(self):
        return self.__acc_balance * self.__rub_eur_rate


class AmountInWords:
    def __init__(self, acc_balance: AccountBalance):
        self.__acc_balance = acc_balance

    def __str__(self) -> str | None:
        # Реализация преобразования суммы в числительное
        sl_n = [
            {
                0: "ноль",
                1: "один",
                2: "два",
                3: "три",
                4: "четыре",
                5: "пять",
                6: "шесть",
                7: "семь",
                8: "восемь",
                9: "девять",
            },
            {
                1: "десять",
                2: "двадцать",
                3: "тридцать",
                4: "сорок",
                5: "пятьдесят",
                6: "шестьдесят",
                7: "семьдесят",
                8: "восемьдесят",
                9: "девяносто",
            },
            {
                1: "сто",
                2: "двести",
                3: "триста",
                4: "четыреста",
                5: "пятьсот",
                6: "шестьсот",
                7: "семьсот",
                8: "восемьсот",
                9: "девятьсот",
            },
            {
                1: "тысяча",
                2: "две тысячи",
                3: "три тысячи",
                4: "четыре тысячи",
                5: "пять тысяч",
                6: "шесть тысяч",
                7: "семь тысяч",
                8: "восемь тысяч",
                9: "девять тысяч",
            },
            {
                1: "одиннадцать",
                2: "двенадцать",
                3: "тринадцать",
                4: "четырнадцать",
                5: "пятнадцать",
                6: "шестнадцать",
                7: "семнадцать",
                8: "восемнадцать",
                9: "девятнадцать",
            },
        ]

        bal = list(map(int, str(int(self.__acc_balance))))
        bal.reverse()
        list_bal = []
        if len(bal) == 1:
            str_bal = sl_n[bal[0]]
        elif len(bal) < 5:
            prew = 0
            for count, i in enumerate(bal):
                if (count == 1) and (i == 1) and (prew != 0):
                    list_bal[0] = sl_n[-1][prew]
                else:
                    val = sl_n[count].get(i, None)
                    if val:
                        list_bal.append(val)
                prew = i
            list_bal.reverse()
            str_bal = " ".join(list_bal)
        else:
            print("Сумма больше 99999")
            return None

        return str_bal


class AccountStorage:
    def __init__(
        self,
        acc_owner: AccountOwner,
        account_number: int,
        acc_balance: AccountBalance,
    ):
        self.__acc_owner = acc_owner
        self.__account_number = account_number
        self.__acc_balance = acc_balance

    def __str__(self):
        return (
            f"Владелец счета: {self.__acc_owner.owner}\n"
            f"Номер счета: {self.__account_number}\n"
            f"Текущая сумма на счете: {self.__acc_balance}"
        )


class Account:
    def __init__(
        self,
        owner: str,
        account_number: int,
        interest_rate: float,
        balance: float,
        rub_dollar_rate: float,
        rub_eur_rate: float,
    ):
        # Создаем объекты, которые нужны для работы с аккаунтом
        self.account_owner = AccountOwner(owner)
        self.account_balance = AccountBalance(balance)
        self.balance_operations = BalanceOperations(self.account_balance)
        self.interest_converter = InterestConverter(
            self.account_balance, interest_rate
        )
        self.currency_converter = СurrencyConverter(
            self.account_balance, rub_dollar_rate, rub_eur_rate
        )
        self.am_in_words = AmountInWords(self.account_balance)
        self.account_storage = AccountStorage(
            self.account_owner, account_number, self.account_balance
        )

    # Методы для управления аккаунтом
    def display(self):
        print(self.account_storage)

    def change_owner(self, new_owner: str):
        self.account_owner.owner = new_owner

    def withdraw(self, amount: float):
        self.balance_operations.withdraw(amount)

    def deposit(self, amount: float):
        self.balance_operations.deposit(amount)

    def add_interest(self):
        self.interest_converter.add_interest()

    def convert_to_usd(self):
        return self.currency_converter.convert_to_usd()

    def convert_to_eur(self):
        return self.currency_converter.convert_to_eur()

    def amount_in_words(self):
        return self.am_in_words

    def change_currency_converter(
        self, rub_dollar_rate: float, rub_eur_rate: float
    ):
        self.currency_converter = СurrencyConverter(
            self.account_balance, rub_dollar_rate, rub_eur_rate
        )

    def change_interest_converter(self, interest_rate: float):
        self.interest_converter = InterestConverter(
            self.account_balance, interest_rate
        )

    def read_owner(self):
        self.account_owner.read()


# Демонстрация возможностей класса
if __name__ == "__main__":
    rub_dollar_rate = 80
    rub_eur_rate = 90
    my_account = Account(
        "Иванов", "10032", 0.05, 9045, rub_dollar_rate, rub_eur_rate
    )
    my_account.display()
    my_account.change_owner("Петров")
    my_account.deposit(500)
    my_account.withdraw(300)
    my_account.add_interest()
    print("\nИзменённый счет:\n")
    my_account.display()
    usd_amount = my_account.convert_to_usd()
    print(f"Баланс в USD: ${usd_amount}")
    eur_amount = my_account.convert_to_eur()
    print(f"Баланс в EUR: €{eur_amount}")
    word = my_account.amount_in_words()
    print(f"Округленная сумма в рублях: {word}")
    my_account.read_owner()
    print()
    my_account.display()
