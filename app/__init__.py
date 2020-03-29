from flask import Flask
from .config import *


app = Flask(__name__)
app.config.from_object(Config)

#db = SQLAlchemy(app)
from .models import *
from .routes import *


#if __name__ == "__main__":
    #app.run()
