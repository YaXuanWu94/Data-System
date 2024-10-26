from flask import Flask
from create import create_bp
from read import read_bp
from update import update_bp
from delete import delete_bp
from join import join_blueprint

app = Flask(__name__)

# Register the blueprints
app.register_blueprint(create_bp, url_prefix='/create')  # Make sure this is registered with the correct prefix
app.register_blueprint(read_bp)
app.register_blueprint(update_bp, url_prefix='/update')
app.register_blueprint(delete_bp, url_prefix='/delete')
app.register_blueprint(join_blueprint, url_prefix='/join')

if __name__ == '__main__':
    app.run(debug=True)