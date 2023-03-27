from flask import Flask, request, render_template, send_file
import database
from PIL import Image
from img2vect import extract
from OpenSSL import SSL
app = Flask(__name__)


@app.route('/')
def hello():  # put application's code here
    return render_template('homepage.html')

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'GET':
        return render_template('send_photo.html')
    elif request.method == 'POST':
        id = request.form['username']
        try:
            img = request.files['photo'].stream
            vect = extract(img)
        except Exception as e:
            print(e)
            return render_template('problem.html', prob= 'not a photo or bad image format')
        try:
            if database.check_to_user(id, vect):
                return render_template('match.html')
            else:
                return render_template('not-match.html')
        except Exception as e:
            print(e)
            return render_template('problem.html', prob= 'unknown user')
    else:
        hello()

@app.route('/new-account', methods=['GET', 'POST'])
def new_account():
    if request.method == 'GET':
        return render_template('new_account.html')
    elif request.method == 'POST':
        id = request.form['username']
        imgs = [request.files[f'photo{i}'] for i in range(1,6)]
        while None in imgs:
            imgs.remove(None)
        try:
            vects = [extract(img.stream) for img in imgs]
        except Exception as e:
            print(e)
            return render_template('problem.html', prob= 'not a photo or bad image format')
        try:
            database.check_to_user(id,vects[0])
        except:
            database.add_user(id,*vects)
            return render_template('problem.html', prob = 'user added')
        else:
            return render_template('problem.html', prob = 'old user')

@app.route('/favicon', methods = ['GET'])
def favicon():
    return send_file('mini-logo.png')
if __name__ == '__main__':
    context = SSL.Context(SSL.SSLv3_METHOD)
     #   ('server.crt', 'server.key')  # certificate and key files
    context.use_privatekey_file('localhost.key')
    context.use_certificate_file('localhost.crt')
    app.run(ssl_context='adhoc', host='0.0.0.0', port=50100, debug=True)
    # app.run()
