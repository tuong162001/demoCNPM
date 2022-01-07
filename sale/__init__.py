from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = '128917896*%^&%(*&($%&%&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Death231@localhost/labsaledb1?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name = 'drwuls0nf',
    api_key = '391988715622621',
    api_secret = '56mjVcux-VFcfW4-w_R_SrO-r3E'
)

login = LoginManager(app=app)