from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, session

from db import Client, Lesson, User

app = Flask(__name__)
app.secret_key = "flash message"


@app.route('/')
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    clients = Client.select()
    return render_template("home.html", clients=clients)


@app.route('/action')
def action():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template('action.html')


@app.route('/history/<int:client_id>')
def history(client_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    client = Client.get(Client.id == client_id)
    lessons = Lesson.select().where(Lesson.client_id == client_id)
    return render_template('history.html', client=client, lessons=lessons)


@app.route('/update/<int:client_id>')
def update(client_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    try:
        lesson = Lesson.select().where(Lesson.client_id == client_id, Lesson.lesson_date == datetime.now().date()).get()
        # flash("Already updated" + Client.client_name)
        print("Already updated")
        flash("Register Already Updated. You can only update a client once per day!")
    except:
        Lesson.create(client_id=client_id)
        client = Client.get(Client.id == client_id)
        # print(client.client_name)
        # if int (client.lessons) <=0:
        #     client.lessons = int(client.lessons)
        #     client.save()
        #     flash("Lessons Exhausted. Ask client to renew!")

        if int(client.lessons) > 0:
            client.lessons = int(client.lessons) - 1
            client.save()
            flash("Register Updated Successfully for " + client.client_name)
        # print(client.client_name,client.lessons)
    return redirect(url_for('home'))

@app.route('/invoice')
def invoice():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template('invoice.html')

@app.route('/invoiceform', methods=["POST","GET"])
def invoiceform():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        names = request.form['names']
        number = request.form['number']
        date = request.form['date']
        amount = request.form['amount']
        description = request.form['description']
        rate = request.form['rate']
        lessons = request.form['lessons']
        amount = request.form['amount']
        amount = request.form['amount']
        amountpaid = request.form['amountpaid']
        balance = request.form['balance']

        data = {"names": names, "number": number, "date": date, "amount": amount, "description": description,
                "rate": rate, "lessons": lessons, "amount": amount, "amount": amount, "amountpaid": amountpaid,
                "balance": balance}
        return render_template('invoice.html', data=data);
    return render_template('invoiceform.html')

@app.route('/receipt')
def receipt():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template('receipt.html')


@app.route('/receiptform', methods=["POST","GET"])
def receiptform():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        names = request.form['names']
        number = request.form['number']
        date = request.form['date']
        amount = request.form['amount']
        invoicereference = request.form['invoicereference']
        paymentreference = request.form['paymentreference']
        invoicetotal = request.form['invoicetotal']
        amountpaid = request.form['amountpaid']
        stillowing = request.form['stillowing']
        totalamount = request.form['totalamount']
        amountpaid = request.form['amountpaid']
        balancedue = request.form['balancedue']

        data = {"names": names, "number": number, "date": date, "amount": amount, "invoicereference": invoicereference,
                "paymentreference": paymentreference, "invoicetotal": invoicetotal, "amountpaid": amountpaid, "stillowing": stillowing, "totalamount": totalamount,
                "amountpaid": amountpaid, "balancedue": balancedue}
        return render_template('receipt.html', data=data);
    return render_template('receiptform.html')


@app.route('/renewal')
def renewal():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    clients = Client.select()
    return render_template('renewal.html', clients=clients)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        x = User.get(User.email == email, User.password == password)
        x = "yyyy"

        # if x:
        # session["names"] = x.capitalize()
        # session["names"] = x
        # # session["names"]=x.names
        session["names"] = x
        session["id"] = x
        session["logged_in"] = True
        return redirect(url_for('home'))
    else:
        # flash("Wrong username or password")
        return render_template('login.html')


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        names = request.form['names']
        email = request.form['email']
        password = request.form['password']
        User.create(names=names, email=email, password=password)
        return redirect(url_for('login'))
    # flash("You have successfully registered. Now login with your email and password!")
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route('/renew/<int:client_id>', methods=['POST'])
def renew(client_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        number = request.form['number']
        client = Client.get(Client.id == client_id)
        client.lessons = int(client.lessons) + int(number)
        client.save()
        flash(client.client_name + " lessons are now " + str(client.lessons))
    return redirect(url_for('renewal'))


@app.route('/insert', methods=['POST'])
def insert():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        flash("Client Registered Successfully")
        client_name = request.form['client_name']
        registration_date = request.form['registration_date']
        parent_name = request.form['parent_name']
        postal_address = request.form['postal_address']
        personal_address = request.form['personal_address']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        client_package = request.form['client_package']
        lessons = request.form['lessons']
        Client.create(client_name=client_name, registration_date=registration_date, parent_name=parent_name,
                      postal_address=postal_address, personal_address=personal_address, date_of_birth=date_of_birth,
                      gender=gender, email=email, phone=phone, client_package=client_package, lessons=lessons)
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
