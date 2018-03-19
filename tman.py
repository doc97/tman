from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

from views import *

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
