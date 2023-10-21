from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

fee_heads = []
dues = []
invoices = []
payments = []

class FeeHead:
    def __init__(self, name, amount, frequency_months):
        self.name = name
        self.amount = amount
        self.frequency_months = frequency_months

class Due:
    def __init__(self, fee_head, due_date):
        self.fee_head = fee_head
        self.due_date = due_date

class Invoice:
    def __init__(self, dues):
        self.dues = dues
        self.status = "Unpaid"

class Payment:
    def __init__(self, invoice, amount, date):
        self.invoice = invoice
        self.amount = amount
        self.date = date

@app.route('/')
def index():
    return render_template('index.html', fee_heads=fee_heads, invoices=invoices)

@app.route('/create_fee_head', methods=['GET', 'POST'])
def create_fee_head():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        frequency_months = int(request.form['frequency_months'])
        fee_head = FeeHead(name, amount, frequency_months)
        fee_heads.append(fee_head)
        flash('Fee head created successfully', 'success')
        return redirect(url_for('create_fee_head'))

    return render_template('create_fee_head.html')

@app.route('/create_due', methods=['GET', 'POST'])
def create_due():
    if request.method == 'POST':
        fee_head = fee_heads[int(request.form['fee_head_index'])]
        due_date = request.form['due_date']
        due = Due(fee_head, due_date)
        dues.append(due)
        flash('Due created successfully', 'success')
        return redirect(url_for('create_due'))

    return render_template('create_due.html', fee_heads=fee_heads)

@app.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    if request.method == 'POST':
        selected_dues = [dues[int(index)] for index in request.form.getlist('due_index')]
        invoice = Invoice(selected_dues)
        invoices.append(invoice)
        flash('Invoice created successfully', 'success')
        return redirect(url_for('create_invoice'))

    return render_template('create_invoice.html', dues=dues)

@app.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    if request.method == 'POST':
        invoice = invoices[int(request.form['invoice_index'])]
        amount = float(request.form['amount'])
        date = request.form['payment_date']
        payment = Payment(invoice, amount, date)
        payments.append(payment)
        invoice.status = "Paid"
        flash('Payment made successfully', 'success')
        return redirect(url_for('make_payment'))

    return render_template('make_payment.html', invoices=invoices)

if __name__ == '__main__':
    app.run(debug=True)
