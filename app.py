from flask import Flask  ,Blueprint ,render_template
import os
from database import connect_db
from flask_mail import Mail
from flask_mail import Message

from login import login_blueprint
from user_page import user_blueprint

app = Flask(__name__)
app.register_blueprint(login_blueprint)
app.register_blueprint(user_blueprint)
db_pass =  os.getenv("db_pass")
db_name  = os.getenv("db_name")
# print('t')

# # db = client[db_name]
# # collection_name = 'test1'
# # records = db[collection_name]


app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '4755426d24063e'
app.config['MAIL_PASSWORD'] = 'a6dcc06077e8a8'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.secret_key = "testing1"
mail = Mail(app)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
