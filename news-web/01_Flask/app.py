from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import make_response
from flask import abort

app = Flask(__name__)

app.config.update({
    'SECRET_KEY': 'a random string'
})

print(app.config['SECRET_KEY'])

#useragent = request.headers.get('User-Agent')
#print(useragent)
#page = request.args.get('page')
#per_page = request.args.get('per_page')
#print('{}+{}'.format(page, per_page))

@app.route('/')
def index():
    username = request.cookies.get('username')
    return 'Hello World!, Hello {}!'.format(username)

@app.route('/user/<username>')
def user_index(username):
    return 'Hello {}'.format(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post {}'.format(post_id)

@app.route('/usr/<username>')
def usr_index(username):
    if username == 'invalid':
        abort(404)
    resp = make_response(render_template('user_index.html', username=username))
    resp.set_cookie('username', username)
    return resp

@app.route('/default')
def default_index():
    return redirect(url_for('user_index', username='default'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
if __name__ == '__main__':
    app.run()
