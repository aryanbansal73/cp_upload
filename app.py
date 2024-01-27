from flask import Flask  
import os
from extensions import mail
from login import login_blueprint
from user_page import user_blueprint
from dotenv import load_dotenv
load_dotenv(override=True)
app = Flask(__name__)
app.register_blueprint(login_blueprint)
app.register_blueprint(user_blueprint)


app.config['MAIL_SERVER']=  os.getenv("smtp_server")
app.config['MAIL_PORT'] =  os.getenv("smtp_port")
app.config['MAIL_USERNAME'] = os.getenv("username")
app.config['MAIL_PASSWORD'] = os.getenv("api_key")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.secret_key = "testing1"
mail.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
