from flask import Flask
from app.routes import refill_blueprint

app = Flask(__name__)
app.register_blueprint(refill_blueprint)

if __name__ == '__main__':
    print("🚀 Starting Refill Agent API...")
    app.run(debug=True)
