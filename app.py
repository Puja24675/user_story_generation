from flask import Flask
from flask_cors import CORS
from routes.story_routes import story_bp

app = Flask(__name__)
CORS(app)

# Register blueprint
app.register_blueprint(story_bp)

if __name__ == '__main__':
    app.run(debug=True)
 