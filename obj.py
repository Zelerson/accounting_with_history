from os.path import exists


class Product:
    def __init__(self, name: str, quant: int, price: int):
        self.name = name.lower()
        self.quant = quant
        self.price = price

    def __str__(self):
        return f'Nazwa: {self.name.capitalize()}, Ilość: {self.quant}, Cena: {self.price}'

    def __repr__(self):
        return f'Product(name="{self.name}", quant={self.quant}, price={self.price})'


class Warehouse:
    def __init__(self, balance: int = 0):
        self.stock = []
        self.history = []
        self.balance = balance

    def check_history(self):
        start_input = input('Podaj indeks startowy: ')
        end_input = input('Podaj indeks końcowy: ')

        try:
            start_index = int(start_input) if start_input else None
            end_index = int(end_input) if end_input else None
            if (start_index is None or 0 <= start_index < len(self.history)) and (end_index is None or 0 <= end_index <= len(self.history)):
                print(self.history[start_index:end_index])
            else:
                print(f'Zakres historii to 0 - {len(self.history) - 1}')
        except TypeError:
            print('Podaj liczby lub brak wartości(enter)')

    def export_history(self):
        if not exists('history.txt'):
            f = open('history.txt', 'x')
            f.close()
        with open('history.txt', 'a') as file:
            for line in self.history:
                file.write(line + '\n')

    def export_status(self):
        with open('warehouse_status.txt', 'w') as file:
            file.write(str(self.balance) + '\n')
            for product in self.stock:
                file.write(repr(product) + '\n')

    def import_status(self):
        with open('warehouse_status.txt', 'r') as file:
            lines = file.readlines()
            self.balance = int(lines[0])
            for product in lines[1:]:
                self.stock.append(eval(product))

    def find_product(self, name: str):
        return next((p for p in self.stock if p.name == name), None)

    def check_stock(self):
        for item in self.stock:
            print(item)

    def change_balance(self, amount: int):
        if 0 <= self.balance + amount:
            self.balance += amount

            with open('warehouse_status.txt', 'r') as file:
                lines = file.readlines()
            with open('warehouse_status.txt', 'w') as file:
                file.writelines(lines)

            self.history.append(f'Saldo: {amount}')
            return True
        else:
            print('Debet niedozwolony')
            return False

    # sprzedaż
    def sale(self, product: Product):
        existing_product = self.find_product(product.name)

        if existing_product and existing_product.quant >= product.quant:
            existing_product.quant -= product.quant
            self.change_balance(product.price * product.quant)
            self.history.append(f'Sprzedaz: {product.name} {product.quant} szt')

            if existing_product.quant == 0:
                self.stock.remove(existing_product)

            self.export_status()
            self.export_history()
        else:
            print('Brak wystarczającej ilości w magazynie')

    # zakup
    def purchase(self, product: Product):
        if self.change_balance(-product.price * product.quant):
            existing_product = self.find_product(product.name)
            if existing_product:
                existing_product.quant += product.quant
            else:
                self.stock.append(product)
            self.history.append(f'Zakup: {product.name} {product.quant} szt')
            self.export_status()
            self.export_history()


def add_product():
    name = input('Podaj nazwę produktu:\n')
    quant = input('Podaj ilość sztuk:\n')
    price = input('Podaj cenę:\n')
    if int(quant) > 0 and int(price) > 0:
        return Product(name, int(quant), int(price))
    else:
        print('Ilość sztuk oraz cena muszą być liczbami dodatnimi')


