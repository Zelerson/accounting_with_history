from func import manager, add_product
from os.path import exists

manager.execute('import_status') if exists('warehouse_status.txt') else manager.execute('export_status')

while True:
    print('Lista komend: saldo, sprzedaż, zakup, konto, lista, magazyn, przegląd, koniec\n')
    command = input('Wprowadź komendę: ')

    match command:
        case 'saldo':
            a = input('Podaj kwotę do dodania lub odjęcia z konta:\n')
            try:
                manager.execute('change_balance', amount=int(a))
            except TypeError:
                print('Należy podać liczbę całkowitą')
        case 'sprzedaż':
            manager.execute('sale', product=add_product())
        case 'zakup':
            manager.execute('purchase', product=add_product())
        case 'konto':
            print(f'Stan konta: {manager.balance}')
        case 'lista':
            manager.execute('check_stock')
        case 'magazyn':
            name = input('Podaj nazwę wyszukiwanego produktu: ')
            searched_for = manager.execute('find_product', search_key=name)
            print(searched_for) if searched_for else print('Brak produktu w magazynie')
        case 'przegląd':
            manager.execute('check_history')
        case 'koniec':
            break
        case _:
            print('Błędna komenda \n')


