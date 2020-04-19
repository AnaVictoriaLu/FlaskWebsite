import csv
import bcrypt
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask import Flask,render_template,url_for,flash,redirect, session
from forms import RegistrationForm, LoginForm, ConferenceForm, ForgotForm

app = Flask(__name__)
app.secret_key = '202977e7b6cb385ae79442a0492fb179'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True


class User(UserMixin):
    def __init__(self, username, email, password=None):
        self.username = username
        self.id = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    user = find_user(user_id)
    if user:
        user.password = None
    return user

def find_user(email):
    with open('data/users.csv')as f:
        for user in csv.reader(f):
            if len(user)>= 2 and email == user[1]:
                return User(*user)
    return None


@app.route('/')
def index():
    return render_template('index.html', email=session.get('email'))


@app.route('/team')
@login_required
def team():
    return render_template('team.html', title='Team')

@app.route('/collection')
@login_required
def collection():
    return render_template('collection.html', title="Collection")

@app.route('/blog')
#this page is the only non-protected page
def blog():
    prefix = '/static'
    with open('data/blogTopics.csv') as f:
        topic_list = list(csv.reader(f))[1:]
    return render_template('blog.html', title='Blog', topic_list = topic_list, prefix = prefix)

@app.route('/conferences', methods=['GET','POST'])
@login_required
def conferences():
    form = ConferenceForm()
    if form.validate_on_submit():
        if form.date.data == '2020-06-01' or form.date.data == '2020-08-10':
            with open('data/messages.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([form.name.data,
                                form.email.data,
                                form.date.data])
            return redirect(url_for('response', name = form.name.data))
        else:
            flash('Enter one of the dates available in the calendar', 'danger')
    return render_template('conferences.html',title ='Conferences', form = form)

@app.route('/response/<name>')
@login_required
def response(name):
    emailList = []
    #Taking the emails fromt he messages.csv file and add it to a list in the emails.csv file
    with open('data/emails.csv', 'w') as f1:
     with open('data/messages.csv', 'r') as f:
        for row in f:
            if len(row)>= 2:
                temp = row[:-1].split(",")
                emailList.append(temp[1])
        f1.write(str(emailList))
    return render_template('response.html', name = name)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user(form.email.data)
        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
            login_user(user)
            flash('You are logged in!', 'success')
            next_page = session.get('next', '/')
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Check Email or Password', 'danger')
    return render_template('login.html', title='Login',form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #Using the email instead of username as user id
        user = find_user(form.email.data)
        if not user:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode(), salt)
            with open('data/users.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([form.username.data, form.email.data, password.decode()])
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect('/login')
        else:
            flash('This email already exists', 'danger')
    return render_template('register.html', title='Register',form = form)


@app.route("/forgot", methods=['GET','POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        user = find_user(form.email.data)
        if user:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode(), salt)
            users = []
            #opening users file putting the users in a list
            with open('data/users.csv', 'r') as f:
                for row in f:
                    users.append(row)
            #opening ursers file copying the entire users list with changed password
            with open('data/users.csv', 'w') as f:
                writer = csv.writer(f)
                for row in users:
                    row = row[:-1].split(",")
                    if len(row)>= 2 and form.email.data == row[1]:
                           row[2] = password.decode()
                           writer.writerow(row)
                    elif len(row) >= 2:
                        writer.writerow(row)
            flash(f'Password for {form.email.data} has been changed!', 'success')
            return redirect('/login')
        else:
            flash('This email does not exist. Try again.', 'danger')
    return render_template('forgot.html', title='Forgot', form = form)

if __name__ == '__main__':
    app.run(debug = True)
