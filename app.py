from obj import Product, get_history
from logic import wh
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def index():
    stock_data = wh.stock
    balance = wh.balance
    return render_template('index.html', stock_data=stock_data, balance=balance)


@app.route('/modify_balance', methods=['POST'])
def modify_balance():
    try:
        try:
            modifier = int(request.form.get('amount'))
        except ValueError:
            modifier = 0

        if modifier == 0:
            raise ValueError('Dozwolone liczby dodatnie lub ujemne')
        elif wh.change_balance(modifier):
            return redirect('/')
        else:
            raise ValueError('Debet niedozwolony')

    except ValueError as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/sale', methods=['POST'])
def handle_sale():
    p_name = request.form.get('sale_name')
    p_quant = int(request.form.get('sale_quant'))
    p_price = int(request.form.get('sale_price'))

    product = Product(p_name, p_quant, p_price)
    try:
        wh.sale(product)
        return redirect('/')
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/purchase', methods=['POST'])
def handle_purchase():
    try:
        p_name = request.form.get('purchase_name')
        p_quant = int(request.form.get('purchase_quant'))
        p_price = int(request.form.get('purchase_price'))

        if not (p_name and p_quant > 0 and p_price > 0):
            raise ValueError("Błędnie wypełniony formularz")

        product = Product(p_name, p_quant, p_price)
        wh.purchase(product)

        return redirect('/')
    except ValueError as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/historia/', methods=['POST'])
def show_history():
    wh.export_history()
    number1 = request.form.get('number1')
    number1 = int(number1) if number1 else None
    number2 = request.form.get('number2')
    number2 = int(number2) if number2 else None
    history_data = get_history()
    if history_data:
        history_data = history_data[number1:number2]
    try:
        if (number1 is None or 0 <= number1 < len(wh.history)) and (number2 is None or 0 <= number2 <= len(wh.history)):
            return render_template('historia.html', history_data=history_data)
        else:
            raise IndexError(f'Zakres historii to 0 - {(len(wh.history) - 1) if len(wh.history) != 0 else 0}')
    except IndexError as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)



if __name__ == '__main__':
    app.run(debug=True)
