from flask import Flask, render_template, request , session, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from functools import wraps
import sqlite3
from tempfile import mkdtemp
from datetime import  datetime, timedelta
from mcalendar import calendar


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def db_connection():
    conn =sqlite3.connect("project_db.sqlite")
    conn.row_factory = dict_factory
    return conn

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("select * from contracts where userid = ?",(session["user_id"],))
    contracts = cur.fetchall()
    cur.execute("select * from customers where userid = ?",(session["user_id"],))
    customers = cur.fetchall()
    cur.execute("select * from vehicles where userid = ?",(session["user_id"],))
    vehicles = cur.fetchall()
    conn.close()

    if request.method == "POST":
        startdate = datetime.strptime(request.form.get("startday"), "%Y-%m-%dT%H:%M:%S.%f%z").date()
        enddate = datetime.strptime(request.form.get("endday"), "%Y-%m-%dT%H:%M:%S.%f%z").date()
        cal = calendar(startdate, enddate, vehicles, contracts, customers)
        return cal

    startdate = datetime.now().date()
    
    enddate = startdate + timedelta(days=6) 
    cal = calendar(startdate, enddate, vehicles, contracts, customers)
    
    return render_template("index.html", call=cal )

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        error=[]

        if not request.form.get("username"):
            error.append('missing username') 
        if not request.form.get("password"):
            error.append('missing password')
        if error:
            return render_template("/login.html", error = error)

        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = cur.fetchall()
        conn.close()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            error.append("invalid username or password")
            return render_template("/login.html", error = error)

            
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        return redirect("/")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        error = []

        if not request.form.get("username"):
            error.append('missing username')
        if not request.form.get("password"):
            error.append('missing password')
        if request.form.get("confirmation") != request.form.get("password"):
            error.append("passwords don't match")
        if error:
            return render_template("/register.html", error = error)
            
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = ?", (request.form.get("username"),))
        row = cur.fetchall()

        if len(row) == 1:
           error.append('Username already exists')
           return render_template("/register.html", error = error)

        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
        (request.form.get("username"),generate_password_hash(request.form.get("password"))))
        conn.commit()
        conn.close()
        flash('You were successfully register')

        return redirect("/")

    return render_template("register.html")


@app.route('/new_contract', methods=["GET", "POST"])
@login_required
def new_contract():
    if request.method == "POST":
        error = []
        rent = request.form.get("rentday")
        if not rent:
            error.append('Δεν έχετε βάλει μέρα ενοικίασης')
        retu = request.form.get("returnday")
        if not retu:
            error.append('Δεν έχετε βέλει μέρα επιστροφής')
        vehid = request.form.get("vehicle")
        if not vehid:
            error.append('Δεν έχχετε επιλέξει όχημα')
        name = request.form.get("firstname").capitalize()
        if not name:
            error.append('Δεν έχετε βάλει όνομα')
        lastname = request.form.get("lastname").capitalize()
        if not lastname:
            error.append('Δεν έχετε βάλει επώνυμο')
        address1 = request.form.get("adress1").capitalize()
        if not address1:
            error.append('Δεν έχετε βάλει διέυθηνση')
        address2 = request.form.get("adress2").capitalize()
        tel1 = request.form.get("tel1")
        if not tel1:
            error.append('Δεν έχετε βάλει τηλέφωνο')
        tel2 = request.form.get("tel2")
        licence = request.form.get("licence").upper()
        if not licence:
            error.append('Δεν έχετε βάλει αριθμό διπλώματος')
        idorpassport = request.form.get("idorpassport").upper()
        chargepd = request.form.get("chargepd")
        if not chargepd:
            error.append('Δεν έχετε βάλει χρέωση/μέρα')
        totalcharge = request.form.get("totalcharge")
        payinad = request.form.get("payinad")
        reminder = request.form.get("reminder")
        if error:
            return render_template("/new_contract.html", error = error)

        rentday = datetime.strptime(rent, "%Y-%m-%dT%H:%M")  
        returnday = datetime.strptime(retu, "%Y-%m-%dT%H:%M")

        conn = db_connection()
        cur =conn.cursor()
        cur.execute("INSERT INTO customers(firstname, lastname, address1, address2, phonenum1, phonenum2, licence, id_passport, userid) \
        VAlUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",(name, lastname, address1, address2, tel1, tel2, licence, idorpassport, session["user_id"]))

        conn.commit()
        cur.execute("SELECT id FROM customers WHERE licence = ? AND userid = ?",
        (licence , session["user_id"]))
        
        customer_id = cur.fetchall()
        cur.execute("INSERT INTO contracts(customer, vehicle, rentday, returnday, chargepd, payinad, totalcharge ,reminder, userid) \
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",(customer_id[0]["id"], vehid, rentday, returnday, chargepd, payinad, totalcharge, reminder, session["user_id"]))
        conn.commit()

        return redirect("/")

    return render_template("new_contract.html")


@app.route("/avaliable_vehicles", methods=["POST"])
@login_required
def avaliable_vehicles():

    rent = request.form.get("rentday")
    retd = request.form.get("returnday")
    
    rentday = datetime.strptime(rent, "%Y-%m-%dT%H:%M")
    returnday = datetime.strptime(retd, "%Y-%m-%dT%H:%M")

    conn = db_connection()
    cur = conn.cursor()
    cur.execute("select * from vehicles where id not in (select vehicle from contracts where datetime(rentday) <= datetime(?)  and datetime(returnday) > datetime(?) or (datetime(rentday) > datetime(?) and datetime(rentday) < datetime(?)))",(rentday,rentday,rentday,returnday))
    vehicles = cur.fetchall()
    conn.close()

    return vehicles


@app.route("/new_vehicle", methods = ["GET", "POST"])
@login_required
def add_vehicle():
    if request.method == "POST":
        ak = request.form.get("ak").upper()
        typ =request.form.get("type")
        brand = request.form.get("brand").upper()
        model = request.form.get("model").upper()
        displacement =request.form.get("displacement")

        conn = db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO vehicles(ak,type,brand,model,displacement,userid) VALUES(?,?,?,?,?,?)",
        (ak, typ, brand, model, displacement, session["user_id"]))
        conn.commit()
        conn.close()
        flash('The vehicle was added')
        return redirect("/new_vehicle")

    return render_template("/new_vehicle.html")

@app.route("/show_and_delete_contracts", methods =["GET", "POST"])
@login_required
def showordelete():
    if request.method == "POST":
        delete_id = request.form.get("delete")
        conn = db_connection()
        cur =conn.cursor()
        cur.execute("DELETE FROM customers WHERE id = (SELECT customer FROM contracts WHERE id = ? AND userid = ?)",(delete_id, session["user_id"]))
        cur.execute("DELETE FROM contracts WHERE id = ? AND userid = ?",(delete_id, session["user_id"]))
        conn.commit()
        conn.close()
        return redirect("/show_and_delete_contracts")

    conn = db_connection()
    cur =conn.cursor()
    cur.execute("SELECT contracts.id, contracts.rentday, contracts.returnday, contracts.chargepd, contracts.totalcharge, contracts.payinad, contracts.reminder, customers.firstname, customers.lastname ,vehicles.ak FROM ((contracts INNER JOIN customers ON customers.id = contracts.customer) INNER JOIN vehicles ON vehicles.id = contracts.vehicle)  WHERE contracts.userid = ? ORDER BY contracts.id DESC", (session["user_id"],))
    contracts = cur.fetchall()
    conn.close()
    return render_template("/show_and_delete_contracts.html", contracts = contracts)


@app.route("/show_customers")
@login_required
def show_customers():
    conn = db_connection()
    cur =conn.cursor()
    cur.execute("SELECT * FROM customers WHERE userid = ? ORDER BY id DESC", (session["user_id"],))
    customers = cur.fetchall()

    return render_template("/show_customers.html", customers = customers)


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)