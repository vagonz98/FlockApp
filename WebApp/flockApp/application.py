import flask
from firebase import firebase
import hashlib


# EB looks for an 'application' callable by default.
application = flask.Flask(__name__)

logged_in = [False]
SECRET = 'Zu1J0i9vls6l1ygDWc3GuL9XsiffXCASSoqAGrXV'
firebase2 = firebase.FirebaseApplication('https://flock-f7e57.firebaseio.com/', authentication=None)


def firebase_get(my_base, query_string):
    authentication = firebase.FirebaseAuthentication(SECRET, 'irrelevant')
    firebase2.authentication = authentication
    result = firebase2.get(query_string, None)
    return result

def is_authorized(email, password):
    users = firebase_get(firebase2, '/Users')
    m = hashlib.md5()
    m.update(email)
    if m.hexdigest() in users:
        user_info = users[m.hexdigest()]
        if user_info[u'password'] == password:
            if user_info[u'email'] == email:
                return True
    return False

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
            return '/test'
                
        return '/login'


@application.route('/test', methods=['GET'])
def testrender():
    return flask.render_template('homepage.html')



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