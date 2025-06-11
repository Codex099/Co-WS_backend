import base64
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from models import db
from bleu_print import bp
from flask_cors import CORS   
from admin_bcnslg_bleu import admin_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coworking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(bp)
app.register_blueprint(admin_bp)
migrate = Migrate(app, db)

CORS(app)  

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return ''

@app.template_filter('zfill')
def zfill_filter(s, width=2):
    return str(s).zfill(width)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.execute(text('SELECT 1'))
        db.session.commit()
    app.run(debug=True,host="0.0.0.0")