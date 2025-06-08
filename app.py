from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from models import db
from bleu_print import bp
from flask_cors import CORS   
from admin_blueprint import admin_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coworking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(bp)
app.register_blueprint(admin_bp)

CORS(app)  

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.execute(text('SELECT 1'))
        db.session.commit()
    app.run(debug=True,host="0.0.0.0")