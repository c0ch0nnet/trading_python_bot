import jsonpickle
from bj.iBank_2 import Account, CreditAccount


EMPLOYEE_PASSWORD = "123"
ACCOUNTS_FILE = 'accounts'


def close_account():
    passport = input("Введите номер паспотра клиента: ")
    for account in accounts:
        if account.passport == passport:
            account.closing()
    """
    Закрыть счет клиента.
    Считаем, что оставшиеся на счету деньги были выданы клиенту наличными, при закрытии счета
    """


def view_accounts_list():
    for num, account in enumerate(accounts, 1):
        print(f"{num}. {account}")

    """
        Отображение всех клиентов банка в виде нумерованного списка
        """


def view_account_by_passport():
    passport = input("Введите номер паспорта клиента: ")
    for account in accounts:
        if account.passport == passport:
            return account.full_info()


def view_client_account(account):
    return account.__repr__()
    """
    Узнать состояние своего счета
    """


def put_account(account):
    amount = input("Введите сумму для зачисления: ")
    account.deposit(amount)
    """
    Пополнить счет на указанную сумму.
    Считаем, что клиент занес наличные через банкомат
    """


def withdraw(account):
    amount = input("Введите сумму для снятия: ")
    account.withdraw(amount)
    """
    Снять со счета.
    Считаем, что клиент снял наличные через банкомат
    """


def transfer(account):
    print("Введите необходимую информацию")
    phone_number = input("Номер телефона получателя: ")
    amount = input("Сумма перевода: ")
    for acc in accounts:
        if acc.phone_number == phone_number:
            target_account = acc
    account.transfer(amount, target_account)
    """
    Перевести на счет другого клиента по номеру телефона
    """


def create_new_account():
    print("Укажите данные клиента")
    name = input("Имя:")
    passport = input("Номер паспорта: ")
    phone_number = input("Номер телефона: ")
    try:
        account = Account(name, passport, phone_number)
        accounts.append(account)
    except ValueError as err:
        print(f"Не те данные: {err}")


def create_new_credit_acc():
    print("Укажите данные клиента")
    name = input("Имя:")
    passport = input("Номеч паспорта: ")
    phone_number = input("Номер телефона: ")
    negative_limit = input('Введите допустимый отрицательный баланс:')
    account = CreditAccount(name, passport, phone_number, negative_limit)
    credit_accounts.append(account)


def client_menu(account):
    while True:
        print(f"***********Меню клиента <{account.name}>*************")
        print("1. Состояние счета")
        print("2. Пополнить счет")
        print("3. Снять со счета")
        print("4. Перевести деньги другому клиенту банка")
        print("5. Exit")
        choice = input(":")
        if choice == "1":
            view_client_account()
        elif choice == "2":
            put_account()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            transfer()
        elif choice == "5":
            return
    # input("Press Enter")


def employee_menu():
    while True:
        print("***********Меню сотрудника*************")
        print("1. Создать новый счет")
        print("2. Закрыть счет")
        print("3. Посмотреть список счетов")
        print("4. Посмотреть счет по номеру паспорта")
        print("5. Создать новый кредитный счет")
        print("6. Exit")
        choice = input(":")
        if choice == "1":
            create_new_account()
        elif choice == "2":
            close_account()
        elif choice == "3":
            view_accounts_list()
        elif choice == "4":
            view_account_by_passport()
        elif choice == "5":
            create_new_credit_acc()
        elif choice == "6":
            return


def employee_access():
    """
    Проверяет доступ сотрудника банка, запрашивая пароль
    """
    password = input("Пароль: ")
    if password == EMPLOYEE_PASSWORD:
        return True
    return False


def client_access(accounts):
    """
    Находит аккаунт с введеным номером паспорта
    Или возвращает False, если аккаунт не найден
    """
    try:
        passport = input("Номер паспорта: ")
    except ValueError:
        return False
    # acc = [account for account in accounts if passport == account.passport8]
    # return acc[0] if len(acc) > 1 else False

    for account in accounts:
        if passport == account.passport8:
            return account

    return False


def start_menu():
    while True:
        print("Укажите вашу роль:")
        print("1. Сотрудник банка")
        print("2. Клиент")
        print("3. Завершить работу")

        choice = input(":")
        if choice == "3":
            with open(ACCOUNTS_FILE, 'w') as out:
                jsonpickle.set_encoder_options("json", indent=2)
                out.write(jsonpickle.encode(accounts))
            break
        elif choice == "1":
            if employee_access():
                employee_menu()
            else:
                print("Указан неверный пароль, укажите роль и повторите попытку...")
        elif choice == "2":
            account = client_access(accounts)
            if account:
                client_menu(account)
            else:
                print("Указан несуществующий пасспорт, укажите роль и повторите попытку...")
        else:
            print("Указан н1екорректный пункт меню, повторите выбор...")


if __name__ == "__main__":
    try:
        with open(ACCOUNTS_FILE) as f:
            accounts = jsonpickle.decode(f.read())
    except FileNotFoundError:
        accounts = []
    credit_accounts = []
    start_menu()