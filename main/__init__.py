from flask import Flask

app = Flask(__name__)
app.secret_key = 'placeholder'

import database
import login_management
import views