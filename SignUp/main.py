from flask import Flask, render_template, request, redirect, url_for, session, Response
import secrets
import csv

app = Flask(__name__)
app.secret_key = '951d9f8150792ff6ed734d80b91508e3'


def is_valid_signup(firstname, lastname, email, username, password):
  with open('signup.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
      if row[0] == firstname and row[1] == lastname and row[
          2] == email and row[3] == username and row[4] == password:
        return True
  return False


#Route to signup page
@app.route('/', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    if is_valid_signup(firstname, lastname, email, username, password):
      return redirect(url_for('login'))
    else:
      with open('signup.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([firstname, lastname, email, username, password])
      return redirect(url_for('login'))

  return render_template('signuppage.html')


#Route to login page
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    with open('signup.csv', 'r') as file:
      reader = csv.reader(file)
      for row in reader:
        if row[3] == username and row[4] == password:
          session['username'] = username
          return redirect(url_for('dashboard'))
  return render_template('login.html')


#Route to dashbord page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
  if 'username' in session:
    return Response(f'Welcome,{session["username"]}! This is your dashboard', )
  else:
    return redirect(url_for('login'))


#Route to logout
@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('login'))
