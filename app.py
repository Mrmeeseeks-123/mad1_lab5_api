

from flask import Flask ,request
from models import *
from resources import *
from flask_cors import CORS


app = Flask(__name__)


current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "api_database.sqlite3") 

db.init_app(app)
api.init_app(app)
CORS(app)
app.app_context().push()


@app.route("/",methods=["GET"])
def index():
    return "hello_world"

    
    
if __name__ == '__main__':
    # Run the Flask app
    with app.app_context():
        db.create_all()
    app.run(
    host='0.0.0.0',
    debug=True,
    port=5000
    ) 
