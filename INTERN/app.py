from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="BHARATH2005",
    database="test"
)

mycursor = mydb.cursor()

@app.route('/')
def home():
    if 'email' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')  # A home page with links to login and signup

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home')) 
        
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM test_123 WHERE email = %s AND passwrd = %s"
        val = (email, password)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()    
        if result:
            session['email'] = email
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.')
            return redirect(url_for('login'))
    return render_template('login1.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "INSERT INTO users (username, email, passwrd) VALUES (%s, %s, %s)"
        val = (username, email, password)
        mycursor.execute(sql, val)
        mydb.commit()  # Commit the transaction
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return f'Welcome to the dashboard, {session["email"]}!'
    else:
        flash('You are not logged in!')
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
