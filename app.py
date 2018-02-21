from flask import Flask, current_app, request

app = Flask(__name__)
config = {
    'DEBUG': False
    'TESTING': False
    'CSRF_ENABLED': True
    'SECRET_KEY': 'this-really-needs-to-be-changed'
    'SQLALCHEMY_DATABASE_URI': os.environ['DATABASE_URL']
}
app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print(request.json)
        return 'Thanks for returning!'
    if request.method == 'GET':
        return current_app.send_static_file('index.html')
