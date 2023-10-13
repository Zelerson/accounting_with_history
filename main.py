from obj import Product, Warehouse, add_product
from os.path import exists


wh = Warehouse()
wh.import_status() if exists('warehouse_status.txt') else wh.export_status()

while True:
    print('Lista komend:\nsaldo\nsprzedaż\nzakup\nkonto\nlista\nmagazyn\nprzegląd\nkoniec\n')

    command = input('Wprowadź komendę: ')

    match command:
        case 'saldo':
            amount = input('Podaj kwotę do dodania lub odjęcia z konta:\n')
            try:
                wh.change_balance(int(amount))
            except TypeError:
                print('Należy podać liczbę całkowitą')
        case 'sprzedaż':
            wh.sale(add_product())
        case 'zakup':
            wh.purchase(add_product())
        case 'konto':
            print(f'Stan konta: {wh.balance}')
        case 'lista':
            wh.check_stock()
        case 'magazyn':
            name = input('Podaj nazwę wyszukiwanego produktu: ')
            searched_for = wh.find_product(name)
            print(searched_for) if searched_for else print('Brak produktu w magazynie')
        case 'przegląd':
            wh.check_history()
        case 'koniec':
            break
        case _:
            print('Błędna komenda \n')
