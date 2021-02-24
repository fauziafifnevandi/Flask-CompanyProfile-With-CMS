from flask import Flask, render_template, request, flash, redirect, url_for, session, redirect, url_for, Response
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import re
import os
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static')

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'bAkSoBuLaTdIGoReNgLiMaRaTuSanHaLo'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)


#---------------------------#
# [website] Company Profile #
#---------------------------#
@app.route('/')
def main():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM header')
    header = cur.fetchall()

    cur.execute('SELECT * FROM jumbotron')
    jumbotron = cur.fetchall()

    cur.execute('SELECT * FROM tentang')
    tentang = cur.fetchall()

    cur.close()
    return render_template('index.html', header=header, jumbotron=jumbotron, tentang=tentang)


#--------------------#
# [website] Register #
#--------------------#
#this will be the registration page, we need to use both GET and POST requests
@app.route('/web/register', methods=['GET', 'POST'])
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


#-----------------#
# [website] Login #
#-----------------#
@app.route('/web/login', methods=['GET', 'POST'])
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


#------------------#
# [website] Logout #
#------------------#
@app.route('/web/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
   

#-------------#
# [Dashboard] Main #
#-------------#
@app.route('/dashboard', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('dashboard.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#-------------------------#
# [Dashboard] Admin Profile #
#-------------------------#
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


#--------------------#
# [Dashboard] Header #
#--------------------#
@app.route('/dashboard/header')
def header():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM header')
    data = cur.fetchall()
    cur.close()
    return render_template('header.html', header = data)


#-------------------------#
# [Dashboard] Header Edit #
#-------------------------#
@app.route('/dashboard/header/edit/<id>', methods=[ 'POST','GET'])
def header_edit(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM header WHERE id = %s', (id,))
    data = cursor.fetchall()
    cursor.close()
    print(data[0])
    return render_template('header_edit.html', header = data[0])


#---------------------------#
# [Dashboard] Header Update #
#---------------------------#
@app.route('/dashboard/header/update/<id>', methods=[ 'POST'])
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


#-----------------------#
# [Dashboard] Jumbotron #
#-----------------------#
@app.route('/dashboard/jumbotron')
def jumbotron():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM jumbotron')
    data = cur.fetchall()
    cur.close()
    return render_template('jumbotron.html', jumbotron = data)


#----------------------------#
# [Dashboard] Jumbotron Edit #
#----------------------------#
@app.route('/dashboard/jumbotron/edit/<id>', methods=[ 'POST','GET'])
def jumbotron_edit(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM jumbotron WHERE id = %s', (id,))
    data = cursor.fetchall()
    cursor.close()
    print(data[0])
    return render_template('jumbotron_edit.html', jumbotron = data[0])


#------------------------------#
# [Dashboard] Jumbotron Update #
#------------------------------#
@app.route('/dashboard/jumbotron/update/<id>', methods=[ 'POST'])
def jumbotron_update(id):
    if request.method == 'POST':
        tagline = request.form['tagline']
        caption = request.form['caption']
        
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
        cursor.execute('UPDATE jumbotron SET tagline = %s, caption = %s, gambar = %s WHERE id = %s', (tagline, caption, gambar, id,))
        mysql.connection.commit()
  
        cursor.close()
        return redirect(url_for('jumbotron'))


#-------------------------#
# [Website] Pesan / Kirim #
#-------------------------#
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


#----------------------------#
# [Dashboard] Pesan / Terima #
#----------------------------#
@app.route('/dashboard/pesan')
def pesan():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM pesan')
    data = cur.fetchall()

    cur.close()
    return render_template('pesan.html', pesan = data)


#---------------------#
# [Dashboard] Tentang #
#---------------------#
@app.route('/dashboard/tentang')
def tentang():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM tentang')
    data = cur.fetchall()

    cur.close()
    return render_template('tentang.html', tentang = data)


#--------------------------#
# [Dashboard] Tentang Edit #
#--------------------------#
@app.route('/dashboard/tentang/edit/<id>', methods=[ 'POST','GET'])
def tentang_edit(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tentang WHERE id = %s', (id,))
    data = cursor.fetchall()
    cursor.close()
    print(data[0])
    return render_template('tentang_edit.html', tentang = data[0])


@app.route('/dashboard/tentang/update/<id>', methods=[ 'POST'])
def tentang_update(id):
    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        moto1 = request.form['moto1']
        moto2 = request.form['moto2']
        moto3 = request.form['moto3']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE tentang SET judul = %s, isi = %s, moto1 = %s, moto2 = %s, moto3 = %s WHERE id = %s', (judul, isi, moto1, moto2 , moto3, id,))
        mysql.connection.commit()
  
        cursor.close()
        return redirect(url_for('tentang'))



if __name__ == "__main__":
    app.run(debug=True)