from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import re  # Import regular expression module for validation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitter_followed.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)

@app.route('/follow', methods=['POST'])
def follow_user():
    username = request.form.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    # Check if username starts with '@'
    if not username.startswith('@'):
        return jsonify({"error": "Username must start with '@'"}), 400
    
    # Remove '@' for storage, if you prefer to store it without
    clean_username = username.lstrip('@')
    
    # Check if the username already exists in the database
    if User.query.filter_by(username=clean_username).first():
        return jsonify({"message": "Already followed"}), 400
    
    # Add the new user to the database
    new_user = User(username=clean_username)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Followed successfully"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
