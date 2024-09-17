from flask import Flask, Response, render_template, request, redirect, url_for, session, flash, send_file
from datetime import timedelta
import os
import random
import string
import pandas as pd
from io import BytesIO
import csv
import tempfile
from io import StringIO
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from transaction_detail import data
# /count_db
# /print_db

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=10)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Dummy user data
users = {
    "ab025p6" : {
        "username" : "AB025P6".lower(),
        "password" : "nolo2105"
    }
}


def generate_password(length=8):
    characters = string.ascii_letters + string .digits
    return ''.join(random.choice(characters) for i in range(length))


@app.route('/count_db')
def count_db():
    count = Transaction.query.count()
    print(f"Total Transactions in the database: {count}")
    return f"Total transactions in the database: {count}"


def insert_data():
    rows = data.strip().split('\n')
    for row in rows:
        fields = row.split(';')

        while len(fields) < 30:
            fields.append('')  # You can use '' (empty string) instead of None if needed

        transaction = Transaction(
            card_fiid=fields[0] or '',  # Default to empty string if the field is missing
            term_fiid=fields[1] or '',
            card_no=fields[2].strip() if fields[2] else '',
            merchant_no=fields[3] or '',
            device_id=fields[4] or '',
            batch_no=fields[5] or '',
            proc_code=fields[6] or '',
            response_code=fields[7] or '',
            responder=fields[8] or '',
            ecom_flag=fields[9] or '',
            pin_ind=fields[10] or '',
            ucaf=fields[11] or '',
            term_lnet=fields[12] or '',
            rrn=fields[13] or '',
            card_lnet=fields[14] or '',
            merchant_name=fields[15].strip() if fields[15] else '',
            tran_amount=float(fields[16]) if fields[16] else 0.0,  # Default to 0.0 for missing amounts
            account_no=fields[17].strip() if fields[17] else '',
            auth_code=fields[18].strip() if fields[18] else '',
            acquiring_inst_id=fields[19] or '',
            aiv=fields[20] or '',
            migration_ind=fields[21] or '',
            trace_id=fields[22] or '',
            pos_entry_mode=fields[23] or '',
            edc=fields[24] or '',
            tran_date=fields[25] or '',  # Format DD/MM/YY or default to empty string
            tran_time=fields[26] or '',  # Format HH:MM:SS or default to empty string
            message_type=fields[27] or '',
            mcc=fields[28] or '',
            guuid=fields[29] or ''
        )
        db.session.add(transaction)
    db.session.commit()
    print("Data inserted successfully")

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_fiid = db.Column(db.String(4))
    term_fiid = db.Column(db.String(4))
    card_no = db.Column(db.String(16))
    merchant_no = db.Column(db.String(12))
    device_id = db.Column(db.String(8))
    batch_no = db.Column(db.String(3))
    proc_code = db.Column(db.String(6))
    response_code = db.Column(db.String(3))
    responder = db.Column(db.String(1))
    ecom_flag = db.Column(db.String(1))
    pin_ind = db.Column(db.String(1))
    ucaf = db.Column(db.String(1))
    term_lnet = db.Column(db.String(4))
    rrn = db.Column(db.String(12))
    card_lnet = db.Column(db.String(4))
    merchant_name = db.Column(db.String(40))
    tran_amount = db.Column(db.Float)
    account_no = db.Column(db.String(17))
    auth_code = db.Column(db.String(6))
    acquiring_inst_id = db.Column(db.String(3))
    aiv = db.Column(db.String(3))
    migration_ind = db.Column(db.String(1))
    trace_id = db.Column(db.String(3))
    pos_entry_mode = db.Column(db.String(2))
    edc = db.Column(db.String(3))
    tran_date = db.Column(db.String(8))  # Change to format DD/MM/YY
    tran_time = db.Column(db.String(8))  # Assuming format HH:MM:SS
    message_type = db.Column(db.String(4))
    mcc = db.Column(db.String(4))
    guuid = db.Column(db.String(36))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        user = users.get(username)
        if not user:
            flash('Incorrect username. Please contact lehlohonolo.maluleka@absa.africa for access.', 'danger')
        elif password != user['password']:
            flash('Invalid password', 'danger')
        else:
            session.permanent = True
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    new_password = generate_password()
    username = request.form['username'].lower()
    if username in users:
        users[username]['password'] = new_password
        return render_template('popup.html', new_password=new_password)
    flash('Username not found', 'danger')
    return redirect(url_for('login'))


@app.route('/support')
def support():
    support_team = [
        {
            "name": "Lehlohonolo Maluleka",
            "title": "Product Engineer",
            "team": "Merchant Payments",
            "email": "lehlohonolomaluleka@gmail.com"
        }
        
    ]
    return render_template('support.html', support_team=support_team)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/search', methods=['POST'])
def search():
    merchant_no = request.form.get('merchant-number')
    tran_date = request.form.get('tran_date')
    rrn = request.form.get('rrn')
    device_id = request.form.get('device_id')
    authcode = request.form.get('authcode')

    query = Transaction.query
    if merchant_no:
        query = query.filter_by(merchant_no=merchant_no)
    if tran_date:
        query = query.filter_by(tran_date=tran_date)
    if rrn:
        query = query.filter_by(rrn=rrn)
    if device_id:
        query = query.filter_by(device_id=device_id)
    if authcode:
        query = query.filter_by(auth_code=authcode)

    transactions = query.all()

    transactions_list = []
    for t in transactions:
        t_dict = {
            'card_fiid': t.card_fiid,
            'term_fiid': t.term_fiid,
            'card_no': t.card_no,
            'merchant_no': t.merchant_no,
            'device_id': t.device_id,
            'batch_no': t.batch_no,
            'proc_code': t.proc_code,
            'response_code': t.response_code,
            'responder': t.responder,
            'ecom_flag': t.ecom_flag,
            'pin_ind': t.pin_ind,
            'ucaf': t.ucaf,
            'rrn': t.rrn,
            'merchant_name': t.merchant_name,
            'tran_amount': t.tran_amount,
            'auth_code': t.auth_code,
            'migration_ind': t.migration_ind,
            'edc': t.edc,
            'tran_date': t.tran_date,
            'tran_time': t.tran_time,
            'message_type': t.message_type
        }
        transactions_list.append(t_dict)
        

    session['transactions'] = transactions_list

    return render_template('dashboard.html', transactions=transactions_list)
# @app.route('/dashboard')
# def dashboard():
#     transactions = session.get('transactions', [])
#     return render_template('dashboard.html', transactions=transactions)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    transactions = session.get('transactions', [])

    return render_template('dashboard.html', transactions=transactions)


@app.route('/download', methods=['GET'])
def download():
    transactions = session.get('transactions', [])

    if not transactions:
        flash("No transactions to download", "warning")
        return redirect(url_for('dashboard'))

    # Ensure the dataframe columns are in the same order as the displayed table
    df = pd.DataFrame(transactions, columns=[
        'card_fiid', 'term_fiid', 'card_no', 'merchant_no', 'device_id',
        'batch_no', 'proc_code', 'response_code', 'responder', 'ecom_flag',
        'pin_ind', 'ucaf', 'rrn', 'merchant_name', 'tran_amount', 'auth_code',
        'migration_ind', 'edc', 'tran_date', 'tran_time', 'message_type'
    ])

    
    
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    output.seek(0)

    return send_file(output, download_name="transactions.xlsx", as_attachment=True)
# @app.route('/print_db')
# def print_db():
#     transactions = Transaction.query.all()
#     print(f"Total transactions: {len(transactions)}")
#     for i, transaction in enumerate(transactions):
#         print(f"Transaction {i+1}:")
#         print(f"""
#         Card FIID: {transaction.card_fiid}
#         Term FIID: {transaction.term_fiid}
#         Card No: {transaction.card_no}
#         Merchant No: {transaction.merchant_no}
#         Device ID: {transaction.device_id}
#         Batch No: {transaction.batch_no}
#         Proc Code: {transaction.proc_code}
#         Response Code: {transaction.response_code}
#         Responder: {transaction.responder}
#         Ecom Flag: {transaction.ecom_flag}
#         Pin Ind: {transaction.pin_ind}
#         UCAF: {transaction.ucaf}
#         Term Lnet: {transaction.term_lnet}
#         RRN: {transaction.rrn}
#         Card Lnet: {transaction.card_lnet}
#         Merchant Name: {transaction.merchant_name}
#         Tran Amount: {transaction.tran_amount}
#         Account No: {transaction.account_no}
#         Auth Code: {transaction.auth_code}
#         Acquiring Inst ID: {transaction.acquiring_inst_id}
#         AIV: {transaction.aiv}
#         Migration Ind: {transaction.migration_ind}
#         Trace ID: {transaction.trace_id}
#         POS Entry Mode: {transaction.pos_entry_mode}
#         EDC: {transaction.edc}
#         Tran Date: {transaction.tran_date}
#         Tran Time: {transaction.tran_time}
#         Message Type: {transaction.message_type}
#         MCC: {transaction.mcc}
#         GUUID: {transaction.guuid}
#         """)
#     return "Database printed to terminal!"

def save_transactions_to_file(transactions):
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, 'transactions.csv')
    with open(temp_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Card FIID', 'Term FIID', 'Card Number', 'Merchant Number', 'Device ID', 'Batch Number', 
            'Proc Code', 'Response Code', 'Responder', 'ECOM Flag', 'PIN Indicator', 'UCAF', 'RRN', 
            'Merchant Name', 'Transaction Amount', 'Auth Code', 'Migration Indicator', 'EDC', 
            'Transaction Date', 'Transaction Time', 'Message Type'
        ])
        for t in transactions:
            writer.writerow([
                t['card_fiid'], 
                t['term_fiid'], 
                "'" + t['card_no'],  # Treat as text
                "'" + t['merchant_no'],  # Treat as text
                "'" + t['device_id'],  # Treat as text
                "'" + t['batch_no'],  # Treat as text
                "'" + t['proc_code'],  # Treat as text
                "'" + t['response_code'],  # Treat as text
                t['responder'],
                "'" + t['ecom_flag'],  # Treat as text
                "'" + t['pin_ind'],  # Treat as text
                "'" + t['ucaf'],  # Treat as text
                "'" + t['rrn'],  # Treat as text
                t['merchant_name'], 
                t['tran_amount'], 
                "'" + t['auth_code'],  # Treat as text
                t['migration_ind'], 
                "'" + t['edc'],  # Treat as text
                t['tran_date'],  
                t['tran_time'],  
                "'" + t['message_type']  # Treat as text
            ])
    return temp_file

@app.route('/clear_transactions', methods=['POST'])
def clear_transactions():
    try:
        num_rows_deleted = db.session.query(Transaction).delete()
        db.session.commit()
        return f"Cleared {num_rows_deleted} transactions successfully!", 200
    except Exception as e:
        db.session.rollback()
        return f"Failed to clear transactions: {str(e)}", 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
        # insert_data()    # Insert data into the database
    app.run(debug=True)