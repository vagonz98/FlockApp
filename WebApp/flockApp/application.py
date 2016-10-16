import flask
from firebase import firebase
import hashlib


# EB looks for an 'application' callable by default.
application = flask.Flask(__name__)

logged_in = [False]
SECRET = 'Zu1J0i9vls6l1ygDWc3GuL9XsiffXCASSoqAGrXV'
firebase2 = firebase.FirebaseApplication('https://flock-f7e57.firebaseio.com/', authentication=None)


def firebase_get(query_string):
    authentication = firebase.FirebaseAuthentication(SECRET, 'irrelevant')
    firebase2.authentication = authentication
    result = firebase2.get(query_string, None)
    return result

def is_authorized(email, password):
    users = firebase_get('/Users')
    m = hashlib.md5()
    m.update(email)
    if m.hexdigest() in users:
        user_info = users[m.hexdigest()]
        if user_info[u'password'] == password:
            if user_info[u'email'] == email:
                return True
    return False

@application.route('/')
def start():
    if logged_in[0] == True:
        return flask.redirect(flask.url_for('home'))
    return flask.redirect(flask.url_for('login'))

@application.route('/login', methods=['GET', 'POST'])
def login():

    if flask.request.method == 'GET':
        return flask.render_template('login_page.html')
    if flask.request.method == 'POST':
        email = flask.request.form['username']
        password = flask.request.form['password']
        
        if is_authorized(email, password):
            global logged_in
            logged_in.pop()
            logged_in.append(True)
            return '/home'
                
        return '/login'

@application.route('/signup', methods=['GET'])
def signup():
    return flask.render_template('sign-up.html')

@application.route('/home', methods=['GET'])
def home():
    return flask.render_template('homepage.html')

@application.route('/event_data', methods=['POST'])
def gather_event_data():
    trips = firebase_get('/Trips')
    airport_trips = firebase_get('/Filters/airport')
    food_trips = firebase_get('/Filters/food')

    
    return None

@application.route('/logout', methods=['GET'])
def logout():
    global logged_in
    logged_in.pop()
    logged_in.append(False)
    return flask.redirect(flask.url_for('login'))


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()