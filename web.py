from flask import Flask, render_template, request, redirect, url_for, session, redirect, url_for, Response
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import re
import os
from base64 import b64encode
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static')


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')
def main():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM header')
    header = cur.fetchall()
    cur.close()
    return render_template('index.html', header=header)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()

        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
   

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/dashboard', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('dashboard.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/dashboard/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/header/edit/<id>', methods=[ 'POST','GET'])
def header_edit(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM header WHERE id = %s', (id,))
    data = cursor.fetchall()
    cursor.close()
    print(data[0])
    return render_template('header_edit.html', header = data[0])
    

#update beta
@app.route('/header/update/<id>', methods=[ 'POST'])
def header_update(id):

    if request.method == 'POST':
        nama = request.form['nama']
        
        #gambar = request.files['gambar']
        #os.makedirs(os.path.join(app.instance_path, 'none'), exist_ok=True)
        #gambar.save(os.path.join(app.instance_path, 'none', secure_filename(gambar.filename)))

        #gambar = request.files['gambar']
        #gambar.save(secure_filename(gambar.filename))
        #gambar = gambar.filename

        gambar = request.files['gambar']
        gambar.save(os.path.join(UPLOADS_PATH, secure_filename(gambar.filename)))
        gambar = gambar.filename

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE header SET nama = %s, gambar = %s WHERE id = %s', (nama, gambar, id,))
        mysql.connection.commit()
  
        cursor.close()
        return redirect(url_for('header'))


@app.route('/dashboard/header')
def header():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM header')
    data = cur.fetchall()
    cur.close()
    return render_template('header.html', header = data)

@app.route('/kirimpesan', methods=['GET', 'POST'])
def kirimpesan():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        hp = request.form['hp']
        pesan = request.form['pesan']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO pesan VALUES (NULL, %s, %s, %s, %s)', (nama, email, hp, pesan,))
        mysql.connection.commit()

    return redirect(url_for('main'))

@app.route('/dashboard/jumbotron')
def jumbotron():
    return render_template('jumbotron.html')

@app.route('/dashboard/pesan')
def pesan():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM pesan')
    data = cur.fetchall()

    cur.close()
    return render_template('pesan.html', pesan = data)
    
@app.route('/img/<int:img_id>')
def serve_img(img_id):
    
    pass

@app.route('/dashboard/tentang')
def tentang():
    return render_template('tentang.html')

if __name__ == "__main__":
    app.run(debug=True)