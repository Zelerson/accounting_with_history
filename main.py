from classes import Manager, Product
from os.path import exists

manager = Manager()


@manager.assign("check_history")
def check_history(manager):
    start_input = input('Podaj indeks startowy: ')
    end_input = input('Podaj indeks końcowy: ')

    try:
        start_index = int(start_input) if start_input else None
        end_index = int(end_input) if end_input else None
        if ((start_index is None or 0 <= start_index < len(manager.history))
                and (end_index is None or 0 <= end_index <= len(manager.history))):
            print(manager.history[start_index:end_index])
        else:
            print(f'Zakres historii to 0 - {len(manager.history) - 1}')
    except TypeError:
        print('Podaj liczby lub brak wartości(enter)')


@manager.assign("export_history")
def export_history(manager):
    with open('history.txt', 'w') as file:
        for line in manager.history:
            file.write(line + '\n')


@manager.assign("export_status")
def export_status(manager):
    with open('warehouse_status.txt', 'w') as file:
        file.write(str(manager.balance) + '\n')
        for product in manager.stock:
            file.write(repr(product) + '\n')


@manager.assign("import_status")
def import_status(manager):
    with open('warehouse_status.txt', 'r') as file:
        lines = file.readlines()
        manager.balance = int(lines[0])
        for product in lines[1:]:
            manager.stock.append(eval(product))


@manager.assign("find_product")
def find_product(manager, search_key):
    return next((p for p in manager.stock if p.name == search_key), None)


@manager.assign("check_stock")
def check_stock(manager):
    for item in manager.stock:
        print(item)


@manager.assign("change_balance")
def change_balance(manager, amount: int):
    if 0 < manager.balance + amount:
        manager.balance += amount

        with open('warehouse_status.txt', 'r') as file:
            lines = file.readlines()
        with open('warehouse_status.txt', 'w') as file:
            file.writelines(lines)

        manager.history.append(f'Saldo: {amount}')
        return True
    else:
        print('Debet niedozwolony')
        return False


@manager.assign("sale")
def sale(manager, product: Product):
    existing_product = manager.execute('find_product', search_key=product.name)

    if existing_product and existing_product.quant >= product.quant:
        existing_product.quant -= product.quant
        manager.execute('change_balance', amount=product.price * product.quant)
        manager.history.append(f'Sprzedaz: {product.name} {product.quant} szt')

        if existing_product.quant == 0:
            manager.stock.remove(existing_product)

        manager.execute('export_status')
        manager.execute('export_history')
    else:
        print('Brak wystarczającej ilości w magazynie')


@manager.assign("purchase")
def purchase(manager, product: Product):
    if manager.execute('change_balance', amount=-product.price * product.quant):
        existing_product = manager.execute('find_product', search_key=product.name)
        if existing_product:
            existing_product.quant += product.quant
        else:
            manager.stock.append(product)
        manager.history.append(f'Zakup: {product.name} {product.quant} szt')
        manager.execute('export_status')
        manager.execute('export_history')


def add_product():
    name = input('Podaj nazwę produktu:\n')
    quant = input('Podaj ilość sztuk:\n')
    price = input('Podaj cenę:\n')
    if int(quant) > 0 and int(price) > 0:
        return Product(name, int(quant), int(price))
    else:
        print('Ilość sztuk oraz cena muszą być liczbami dodatnimi')


manager.execute('import_status') if exists('warehouse_status.txt') else manager.execute('export_status')

while True:
    print('Lista komend:\nsaldo\nsprzedaż\nzakup\nkonto\nlista\nmagazyn\nprzegląd\nkoniec\n')

    command = input('Wprowadź komendę: ')

    match command:
        case 'saldo':
            a = input('Podaj kwotę do dodania lub odjęcia z konta:\n')
            # try:
            manager.execute('change_balance', amount=int(a))
            # except TypeError:
            #     print('Należy podać liczbę całkowitą')
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


