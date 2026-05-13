from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'clave_secreta_papus'

MONGO_URI = "mongodb+srv://miguel85yt1_db_user:Carcam010@fruteria.3a76l9l.mongodb.net/?appName=Fruteria"
client = MongoClient(MONGO_URI)
db = client['fruteria_db']
usuarios_col = db['usuarios']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form.get('usuario')
        p = request.form.get('password')
        # Buscar usuario en el nuevo cluster
        user = usuarios_col.find_one({"usuario": u, "password": p})
        if user:
            session['user'] = u
            return redirect(url_for('index'))
        error = "Usuario o contraseña incorrectos."
    return render_template("login.html", error=error)

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        u = request.form.get('usuario')
        p = request.form.get('password')
        if u and p:
            if not usuarios_col.find_one({"usuario": u}):
                usuarios_col.insert_one({"usuario": u, "password": p})
                return redirect(url_for('login'))
            return "El usuario ya existe.", 400
    return render_template("registro.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)