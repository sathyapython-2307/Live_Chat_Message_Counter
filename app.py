from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def chat():
    messages = Message.query.order_by(Message.timestamp.desc()).limit(10).all()
    return render_template("chat.html", messages=messages)

@app.route("/api/messages/count")
def message_count():
    count = Message.query.count()
    return jsonify({"count": count})

@app.route("/send", methods=["POST"])
def send():
    username = request.form["username"]
    text = request.form["text"]
    msg = Message(username=username, text=text)
    db.session.add(msg)
    db.session.commit()
    return ("", 204)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if Message.query.count() == 0:
            db.session.add_all([
                Message(username="Alice", text="Hello!"),
                Message(username="Bob", text="Hi there!")
            ])
            db.session.commit()
    app.run(debug=True)