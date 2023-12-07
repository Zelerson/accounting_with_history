from .models import Product, History, Balance, db


def change_balance(amount: int):
    balance = Balance.query.first().balance
    if balance + amount < 0:
        return False
    else:
        Balance.query.first().balance += amount
        return True


def purchase(product: Product):
    if change_balance(-product.price * product.quantity):
        existing_product = Product.query.filter_by(name=product.name).first()
        if existing_product:
            existing_product.quantity += product.quantity
        else:
            db.session.add(product)
        return True
    else:
        return False


def sale(product: Product):
    existing_product = Product.query.filter_by(name=product.name).first()

    if existing_product and existing_product.quantity >= product.quantity:
        existing_product.quantity -= product.quantity
        change_balance(product.price * product.quantity)

        if existing_product.quantity == 0:
            db.session.delete(existing_product)
    else:
        raise Exception('Brak wystarczającej ilości w magazynie')