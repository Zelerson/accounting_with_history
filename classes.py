class Product:
    def __init__(self, name: str, quant: int, price: int):
        self.name = name.lower()
        self.quant = quant
        self.price = price

    def __str__(self):
        return f'Nazwa: {self.name.capitalize()}, Ilość: {self.quant}, Cena: {self.price}'

    def __repr__(self):
        return f'Product(name="{self.name}", quant={self.quant}, price={self.price})'


class Manager:
    def __init__(self, balance: int = 0):
        self.stock = []
        self.history = []
        self.balance = balance
        self.actions = {}

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
        return decorate

    def execute(self, name, *args, **kwargs):
        if name not in self.actions:
            print("Action not defined")
        else:
            return self.actions[name](self, *args, **kwargs)



