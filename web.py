#----------------#
# Import Library #
#----------------#
from flask import Flask, render_template, request, flash, redirect, url_for, session, redirect, url_for, Response
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import re
import os
from os.path import join, dirname, realpath

#-----------------------------#
# Directory Image Upload Path #
#-----------------------------#
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static')

#---------------#
# Flask Service #
#---------------#
app = Flask(__name__) 

#-----------------------------------------------------------------------------#
# Change this to your secret key (can be anything, it's for extra protection) #
#-----------------------------------------------------------------------------#
app.secret_key = 'bAkSoBuLaTdIGoReNgLiMaRaTuSanHaLo'

#----------------------------------------------#
# Enter your database connection details below #
#----------------------------------------------#
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'reitha_cake'

#-----------------#
# Intialize MySQL #
#-----------------#
mysql = MySQL(app)

#--------------------------------------------Main Code Website--------------------------------------------#
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
    
    cur.execute('SELECT * FROM klien')
    klien = cur.fetchall()
    
    cur.execute('SELECT * FROM paralax')
    paralax = cur.fetchall()
    
    cur.execute('SELECT * FROM pelayanan')
    pelayanan = cur.fetchall()
    
    cur.execute('SELECT * FROM produk')
    produk = cur.fetchall()
    
    cur.execute('SELECT * FROM hubungi_kami')
    hubungi_kami = cur.fetchall()

    cur.close()   
    return render_template('index.html', header=header, jumbotron=jumbotron, tentang=tentang, klien=klien, paralax=paralax, pelayanan=pelayanan, produk=produk, hubungi_kami=hubungi_kami)

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
    msg=''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM header')
    header = cur.fetchall()
    

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
    return render_template('login.html', header=header,  msg=msg)

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

#-----------------------#
# [Dashboard] Dashboard #
#-----------------------#
@app.route('/dashboard', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM header')
        header = cur.fetchall()
        return render_template('dashboard.html', username=session['username'], header=header)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#---------------------------#
# [Dashboard] Admin Profile #
#---------------------------#
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
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM header')
        data = cur.fetchall()
        cur.close()
        return render_template('header.html', header = data)
    return redirect(url_for('login'))

#-------------------------#
# [Dashboard] Header Edit #
#-------------------------#
@app.route('/dashboard/header/edit/<id>', methods=[ 'POST','GET'])
def header_edit(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM header WHERE id = %s', (id,))
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template('header_edit.html', header = data[0])
    return redirect(url_for('login'))

#---------------------------#
# [Dashboard] Header Update #
#---------------------------#
@app.route('/dashboard/header/update/<id>', methods=[ 'POST'])
def header_update(id):

    if request.method == 'POST':    
        #gambar = request.files['gambar']
        #os.makedirs(os.path.join(app.instance_path, 'none'), exist_ok=True)
        #gambar.save(os.path.join(app.instance_path, 'none', secure_filename(gambar.filename)))

        #gambar = request.files['gambar']
        #gambar.save(secure_filename(gambar.filename))
        #gambar = gambar.filename

        nama = request.form['nama']
        gambar = request.files['gambar']
        gambar.save(os.path.join(UPLOADS_PATH, secure_filename(gambar.filename)))
        gambar = gambar.filename
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE header SET nama = %s, gambar = %s WHERE id = %s', (nama, gambar, id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('header'))
    return render_template('login.html')
        
#-----------------------#
# [Dashboard] Jumbotron #
#-----------------------#
@app.route('/dashboard/jumbotron')
def jumbotron():
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM jumbotron')
        data = cur.fetchall()
        cur.close()
        return render_template('jumbotron.html', jumbotron = data)
    return redirect(url_for('login'))

#----------------------------#
# [Dashboard] Jumbotron Edit #
#----------------------------#
@app.route('/dashboard/jumbotron/edit/<id>', methods=[ 'POST','GET'])
def jumbotron_edit(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM jumbotron WHERE id = %s', (id,))
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template('jumbotron_edit.html', jumbotron = data[0])
    return redirect(url_for('login'))

#------------------------------#
# [Dashboard] Jumbotron Update #
#------------------------------#
@app.route('/dashboard/jumbotron/update/<id>', methods=[ 'POST'])
def jumbotron_update(id):
    if request.method == 'POST':
        tagline = request.form['tagline']
        caption = request.form['caption']
        gambar = request.files['gambar']
        gambar.save(os.path.join(UPLOADS_PATH, secure_filename(gambar.filename)))
        gambar = gambar.filename
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE jumbotron SET tagline = %s, caption = %s, gambar = %s WHERE id = %s', (tagline, caption, gambar, id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('jumbotron'))
    return render_template('jumbotron.html')

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
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM pesan')
        data = cur.fetchall()
        cur.close()
        return render_template('pesan.html', pesan = data)
    return redirect(url_for('login'))

#---------------------#
# [Dashboard] Tentang #
#---------------------#
@app.route('/dashboard/tentang')
def tentang():
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM tentang')
        data = cur.fetchall()
        cur.close()
        return render_template('tentang.html', tentang = data)
    return redirect(url_for('login'))

#--------------------------#
# [Dashboard] Tentang Edit #
#--------------------------#
@app.route('/dashboard/tentang/edit/<id>', methods=[ 'POST','GET'])
def tentang_edit(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tentang WHERE id = %s', (id,))
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template('tentang_edit.html', tentang = data[0])
    return redirect(url_for('login'))

#----------------------------#
# [Dashboard] Tentang Update #
#----------------------------#
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
    return render_template('tentang.html')

#-------------------------------#
# [Dashboard] Klien dan Paralax #
#-------------------------------#
@app.route('/dashboard/klien')
def klien():
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM klien')
        klien = cur.fetchall()
        cur.execute('SELECT * FROM paralax')
        paralax = cur.fetchall()
        cur.close()
        return render_template('klien.html', klien = klien, paralax=paralax )
    return redirect(url_for('login'))

#--------------------------#
# [Dashboard] Tentang Edit #
#--------------------------#
@app.route('/dashboard/klien/edit/<id>', methods=[ 'POST','GET'])
def klien_edit(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM klien WHERE id = %s', (id,))
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template('klien_edit.html', klien = data[0])
    return redirect(url_for('login'))

#----------------------------#
# [Dashboard] Klien Update #
#----------------------------#
@app.route('/dashboard/klien/update/<id>', methods=[ 'POST'])
def klien_update(id):
    if request.method == 'POST':
        nama = request.form['nama']
        gambar = request.files['gambar']
        gambar.save(os.path.join(UPLOADS_PATH, secure_filename(gambar.filename)))
        gambar = gambar.filename
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE klien SET nama = %s,gambar = %s WHERE id = %s', (nama, gambar, id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('klien'))
    return render_template('klien.html')

#--------------------------#
# [Dashboard] Paralax Edit #
#--------------------------#
@app.route('/dashboard/paralax/edit/<id>', methods=[ 'POST','GET'])
def paralax_edit(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM paralax WHERE id = %s', (id,))
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template('paralax_edit.html', paralax = data[0])
    return redirect(url_for('login'))

#----------------------------#
# [Dashboard] Paralax Update #
#----------------------------#
@app.route('/dashboard/paralax/update/<id>', methods=[ 'POST'])
def paralax_update(id):
    if request.method == 'POST':
        gambar = request.files['gambar']
        gambar.save(os.path.join(UPLOADS_PATH, secure_filename(gambar.filename)))
        gambar = gambar.filename
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE paralax SET gambar = %s WHERE id = %s', (gambar, id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('klien'))
    return render_template('klien.html')

#-----------------------#
# [Dashboard] Pelayanan #
#-----------------------#
@app.route('/dashboard/pelayanan')
def pelayanan():
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM pelayanan')
        data = cur.fetchall()
        cur.close()
        return render_template('pelayanan.html', pelayanan=data )
    return redirect(url_for('login'))

#----------------------------#
# [Dashboard] Pelayanan Edit #
#----------------------------#
@app.route('/dashboard/pelayanan/edit/<id>', methods=[ 'POST','GET'])
def pelayanan_edit(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pelayanan WHERE id = %s', (id,))
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template('pelayanan_edit.html', pelayanan = data[0])
    return redirect(url_for('login'))

#------------------------------#
# [Dashboard] Pelayanan Update #
#------------------------------#
@app.route('/dashboard/pelayanan/update/<id>', methods=[ 'POST'])
def pelayanan_update(id):
    if request.method == 'POST':
        simbol = request.form['simbol']
        judul = request.form['judul']
        isi = request.form['isi']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE pelayanan SET simbol = %s, judul = %s, isi = %s WHERE id = %s', (simbol, judul, isi, id,))
        mysql.connection.commit()

        cursor.close()
        return redirect(url_for('pelayanan'))
    return render_template('pelayanan.html')

#--------------------#
# [Dashboard] Produk #
#--------------------#
@app.route('/dashboard/produk')
def produk():
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM produk')
        data = cur.fetchall()
        cur.close()
        return render_template('produk.html', produk=data )
    return redirect(url_for('login'))

#-------------------------#
# [Dashboard] Produk Edit #
#-------------------------#
@app.route('/dashboard/produk/edit/<id>', methods=[ 'POST','GET'])
def produk_edit(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM produk WHERE id = %s', (id,))
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template('produk_edit.html', produk = data[0])
    return redirect(url_for('login'))

#---------------------------#
# [Dashboard] Produk Update #
#---------------------------#
@app.route('/dashboard/produk/update/<id>', methods=[ 'POST'])
def produk_update(id):
    if request.method == 'POST':
        nama = request.form['nama']
        gambar = request.files['gambar']
        gambar.save(os.path.join(UPLOADS_PATH, secure_filename(gambar.filename)))
        gambar = gambar.filename
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE produk SET nama = %s, gambar = %s WHERE id = %s', (nama, gambar, id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('produk'))
    return render_template('produk.html')

#--------------------------#
# [Dashboard] Hubungi Kami #
#--------------------------#
@app.route('/dashboard/hubungi_kami')
def hubungi_kami():
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM hubungi_kami')
        data = cur.fetchall()
        cur.close()
        return render_template('hubungi_kami.html', hubungi_kami=data )
    return redirect(url_for('login'))

#-------------------------------#
# [Dashboard] Hubungi Kami Edit #
#-------------------------------#
@app.route('/dashboard/hubungi_kami/edit/<id>', methods=[ 'POST','GET'])
def hubungi_kami_edit(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM hubungi_kami WHERE id = %s', (id,))
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template('hubungi_kami_edit.html', hubungi_kami = data[0])
    return redirect(url_for('login'))

#---------------------------------#
# [Dashboard] Hubungi Kami Update #
#---------------------------------#
@app.route('/dashboard/hubungi_kami/update/<id>', methods=[ 'POST'])
def hubungi_kami_update(id):
    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        judul_informasi = request.form['judul_informasi']
        nama_toko = request.form['nama_toko']
        alamat_toko = request.form['alamat_toko']
        kota_toko = request.form['kota_toko']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE hubungi_kami SET judul = %s, isi = %s, judul_informasi = %s, nama_toko = %s, alamat_toko = %s,kota_toko = %s  WHERE id = %s', (judul, isi, judul_informasi, nama_toko, alamat_toko , kota_toko, id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('hubungi_kami'))
    return render_template('hubungi_kami.html')

#------------------------------------------End Main Code Website------------------------------------------#
#-----------------#
# [Flask] Service #
#-----------------#        
if __name__ == "__main__":
    app.run(debug=True)