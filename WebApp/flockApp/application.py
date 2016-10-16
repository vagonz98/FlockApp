from flask import Flask
from flask.ext.login import LoginManager, UserMixin, login_required, login_user\
from firebase import firebase
import md5

logged_in = [False]
SECRET = 'Zu1J0i9vls6l1ygDWc3GuL9XsiffXCASSoqAGrXV'
firebase2 = firebase.FirebaseApplication('https://flock-f7e57.firebaseio.com/', authentication=None)
m = md5.new()

def firebase_get(my_base, query_string):
    authentication = firebase.FirebaseAuthentication(SECRET, 'irrelevant')
    firebase2.authentication = authentication
    result = firebase2.get(query_string, None)
    return result

def is_authorized(email, password):
    users = firebase_get(firebase2, '/Users')
    m.update(email)
    if m.hexdigest() in users:
        user_info = users[m.hexdigest()]
        if user_info[u'password'] == password:
            if user_info[u'email'] == email:
                return True
    return False

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('static/login.html')
    
    data = request.form
    email = data[u'username']
    password = data[u'password']

    if is_authorized(email, password):
        global logged_in
        logged_in.pop()
        logged_in.append(True)
        return redirect(url_for(''))

    return redirect(url_for('login'))



@application.route('/logout', methods=['GET'])
def logout():
    global logged_in
    logged_in.pop()
    logged_in.append(False)
    return redirect(url_for('login'))

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)


# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()