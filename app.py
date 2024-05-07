from flask import Flask, render_template, request, redirect, session
import pyodbc

app = Flask(__name__, template_folder='template')
app.secret_key = '7f84c74d14a8602475c8e2f9cbcf3a6a'

# Conexión a la base de datos SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ALVARO\SQLEXPRESS;'
                      'Database=login;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

@app.route('/')
def index():
    return redirect('/login.html')
#Verifica los campos de el login
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificar credenciales
        cursor.execute("SELECT * FROM TBL_USER WHERE username=? AND passwor=?", (username, password))
        user = cursor.fetchone()
        
        if user:
            session['username'] = username
            return redirect('/welcome')
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
    else:
        return render_template('login.html', error='')
#page of welcome to a new page
@app.route('/welcome')
def bienvenido():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect('/login')

@app.route('/login.html')
def logout():
    session.pop('username', None)
    return redirect('/login')
#For agreg  a new user.
@app.route('/register.html', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
    
        fullname = request.form ['fullname']
        firstname = request.form['firstname']
        username = request.form['username']
        password = request.form['password']

            #Para que no se agrege una sola letra en el campo
        if len(fullname) <= 1 or len(firstname) <= 1:

             return render_template('register.html', error='Por favor, introduce un nombre y apellido válidos.')
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM TBL_USER WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return render_template('register.html', error='El nombre de usuario ya está en uso')
        
        # Insertar el nuevo usuario en la base de datos
        cursor.execute("INSERT INTO TBL_USER (NOMBRES,APELLIDOS,USERNAME, PASSWOR) VALUES (?, ?,?,?)", (fullname,firstname,username, password))
        conn.commit()
        
        # Redirigir al usuario a la página de inicio de sesión
        return redirect('/login.html')
    else:
        return render_template('register.html', error='No se agrego')
#End code for insert a new user
if __name__ == '__main__':
    app.run(debug=True)
