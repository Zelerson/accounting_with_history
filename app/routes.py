from flask import Blueprint, render_template, request, redirect
from .models import Product, Balance, History, db
from .utils import change_balance, purchase, sale

warehouse_bp = Blueprint('warehouse', __name__, template_folder='../templates')


@warehouse_bp.route('/')
def index():
    stock_data = Product.query.all()
    account = Balance.query.first()
    balance = account.balance
    return render_template('index.html', stock_data=stock_data, balance=balance)


@warehouse_bp.route('/modify_balance', methods=['POST'])
def modify_balance():
    try:
        try:
            modifier = int(request.form.get('amount'))
        except ValueError:
            modifier = 0

        if modifier == 0:
            raise ValueError('Dozwolone liczby dodatnie lub ujemne')
        elif change_balance(modifier):
            history_record = History(operation=f'Saldo: {modifier}')
            db.session.add(history_record)
            db.session.commit()
            return redirect('/')
        else:
            raise ValueError('Debet niedozwolony')

    except ValueError as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@warehouse_bp.route('/purchase', methods=['POST'])
def handle_purchase():
    try:
        p_name = request.form.get('purchase_name')
        p_quant = int(request.form.get('purchase_quant'))
        p_price = int(request.form.get('purchase_price'))

        if not (p_name and p_quant > 0 and p_price > 0):
            raise ValueError("Błędnie wypełniony formularz")

        product = Product(name=p_name, quantity=p_quant, price=p_price)
        if purchase(product):
            history_record = History(operation=f'Zakup: {product.name} {product.quantity} szt, cena: {product.quantity * product.price}')
            db.session.add(history_record)
            db.session.commit()
        return redirect('/')

    except ValueError as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@warehouse_bp.route('/sale', methods=['POST'])
def handle_sale():
    p_name = request.form.get('sale_name')
    p_quant = int(request.form.get('sale_quant'))
    p_price = int(request.form.get('sale_price'))

    product = Product(name=p_name, quantity=p_quant, price=p_price)
    try:
        sale(product)
        history_record = History(operation=f'Sprzedaz: {product.name} {product.quantity} szt, cena: {product.quantity * product.price}')
        db.session.add(history_record)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@warehouse_bp.route('/historia/', methods=['POST'])
def show_history():
    number1 = request.form.get('number1')
    number1 = int(number1) if number1 else None
    number2 = request.form.get('number2')
    number2 = int(number2) if number2 else None
    history_data = History.query.all()
    if history_data:
        history_data_filtered = history_data[number1:number2]
    try:
        if (number1 is None or 0 <= number1 < len(history_data)) and (number2 is None or 0 <= number2 <= len(history_data_filtered)):
            return render_template('historia.html', history_data=history_data_filtered)
        else:
            raise IndexError(f'Zakres historii to 0 - {(len(history_data) - 1) if len(history_data) != 0 else 0}')
    except IndexError as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)
