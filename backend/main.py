from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)  # Corrected '__name__' instead of '_name_'

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///messages.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app) # to allow cross origin resource sharing

# Define the Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)

    def __repr__(self):  # Corrected '__repr__' instead of '_repr_'
        return f"<Message {self.id}>"

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def is_alive():
    return jsonify('live')

@app.route('/api/msg/<string:msg>', methods=['POST'])
def msg_post_api(msg):
    new_msg = Message(message=msg)
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({'msg_id': new_msg.id})

@app.route('/api/msg/<int:msg_id>', methods=['GET'])
def msg_get_api(msg_id):
    msg = Message.query.get(msg_id)
    if msg:
        return jsonify({'msg': msg.message})
    else:
        return jsonify({'error': 'Message not found'}), 404


if __name__ == '__main__':  # Corrected '__name__' and '__main__' instead of '_name_' and '_main_'
    app.run(debug=True, host='0.0.0.0', port=8080)
