from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_address

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=contract_address, abi=abi)

def login():
    try:
        public_key = input("Введите публичный ключ: ")
        password = input("Введите пароль: ")
        w3.geth.personal.unlock_account(public_key, password)
        print(f"Аккаунт авторизован: {public_key}")
        return public_key
    except Exception as e:
        print(f"Ошибка авторизации:{e}")
        return None

def register():
    while True:
        password = input("Введите пароль: ")
        if (len(password) < 12 or
            not any(c.isupper() for c in password) or
            not any(c.islower() for c in password) or
            not any(c.isdigit() for c in password) or
            not any(c in "!@#$%^&*()-_+=" for c in password)):
            print("Пароль не удовлетворяет требованиям:")
            print("- Длина пароля должна быть не менее 12 символов.")
            print("- Пароль должен содержать хотя бы одну заглавную букву, одну строчную букву, одну цифру и один специальный символ (!@#$%^&*()-_+=)")
            continue
        else:
            account = w3.geth.personal.new_account(password)
            print(f"Аккаунт создан: {account}")
            break

def createestate(account):
    try:
        size = int(input("Введите размер недвижимости: "))
        address = input("Введите адрес недвижимости: ")
        estype = int(input("Введите тип недвижимости (0 - дом, 1 - квартира, 2 - лофт): "))
        tx_hash = contract.functions.createestate(size, address, estype).transact({
            'from': account,
        })
        print("Запись о недвижимости успешно создана.")
        print(f"Транзакция отправлена: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка создания записи о недвижимости: {e}")

def createad(account):
    try:
        idestate = int(input("Введите ID недвижимости: "))
        price = int(input("Введите цену недвижимости: ")) 
        tx_hash = contract.functions.createad(idestate, price).transact({
            'from': account,
        })
        print("Объявление о продаже недвижимости успешно создано.")
        print(f"Транзакция отправлена: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка создания объявления о продаже недвижимости: {e}")

def changeestatestatus(account):
    try:
        idestate = int(input("Введите ID недвижимости: "))
        tx_hash = contract.functions.changeestatestatus(idestate).transact({
            'from': account,
        })
        print("Статус недвижимости успешно изменен.")
        print(f"Транзакция отправлена: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка изменения статуса недвижимости: {e}")

def changeadstatus(account):
    try:
        idad = int(input("Введите ID объявления: "))
        tx_hash = contract.functions.changeadstatus(idad).transact({
            'from': account,
        })
        print("Статус объявления успешно изменен.")
        print(f"Транзакция отправлена: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка изменения статуса объявления: {e}")

def buyestate(account):
    try:
        idad = int(input("Введите ID объявления: ")) 
        advertisements = contract.functions.getads().call() 
        price = advertisements[idad - 1][2] 
        tx_hash = contract.functions.buyestate(idad).transact({
            'from': account,
            'value': price 
        })
        print("Недвижимость успешно куплена.")
        print(f"Транзакция отправлена: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка покупки недвижимости: {e}")

def withdraw(account):
    try:
        amount = int(input("Введите сумму для вывода: "))
        tx_hash = contract.functions.withdraw(amount).transact({
            'from': account,
        })
        print("Средства успешно выведены.")
        print(f"Транзакция отправлена: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка вывода средств: {e}")

def getestates():
    try:
        estates = contract.functions.getestates().call()
        print("Доступные недвижимости:")
        for estate in estates:
            print(estate) 
    except Exception as e:
        print(f"Ошибка получения информации о недвижимостях: {e}")

def getads():
    try:
        advertisements = contract.functions.getads().call()
        print("Текущие объявления о продаже недвижимости:")
        for ad in advertisements:
             print(ad)
    except Exception as e:
        print(f"Ошибка получения информации о объявлениях: {e}")

def getbalance():
    try:
        balance = contract.functions.getContractBalance().call()
        print(f"Баланс на смарт-контракте: {balance}")
    except Exception as e:
        print(f"Ошибка получения баланса на смарт-контракте: {e}")

def getaccountbalance(account):
    try:
        balance = contract.functions.getAccountBalance().call({'from': account})
        print(f"Баланс аккаунта на смарт-контракте: {balance}")
    except Exception as e:
        print(f"Ошибка получения баланса аккаунта на смарт-контракте: {e}")

def deposit(account):
    try:
        amount = int(input("Введите сумму для ввода: "))
        tx_hash = contract.functions.deposit().transact({
            'from': account,
            'value': amount 
        })
        print("Средства успешно внесены.")
        print(f"Транзакция отправлена: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка внесения средств: {e}")



def main():
    account = ""
    while True:
        if account == "" or account == None:
            choice = input('Выберите: \n1. Авторизация \n2. Регистрация\n')
            if choice == "1":
                account = login()
            elif choice == "2":
                register()
            else:
                print("Введите корректное число")
        else:
            print("\nВыберите действие:")
            print("1. Создать запись о недвижимости")
            print("2. Создать объявление")
            print("3. Изменить статус недвижимости")
            print("4. Изменить статус объявления")
            print("5. Покупка недвижимости")
            print("6. Вывод средств")
            print("7. Ввод средств")
            print("8. Получение информации")
            print("9. Выход")

            try:
                choice = int(input("Введите номер действия: "))
                if choice == 1:
                    createestate(account)
                elif choice == 2:
                    createad(account)
                elif choice == 3:
                    changeestatestatus(account)
                elif choice == 4:
                    changeadstatus(account)
                elif choice == 5:
                    buyestate(account)
                elif choice == 6:
                    withdraw(account)
                elif choice == 7:
                    deposit(account)
                elif choice == 8:
                    getbalance()
                    getestates()
                    getads()
                    getaccountbalance(account)
                elif choice == 9:
                    account = ""
                else:
                    print("Введите корректное число")
            except ValueError:
                print("Ошибка: Введено некорректное значение.")
            except Exception as e:
                print(f"Ошибка: {e}")

main()