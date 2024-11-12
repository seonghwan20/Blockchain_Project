from flask import Flask, render_template
from route import transaction_bp, utxo_verify_bp

app = Flask(__name__)

app.register_blueprint(transaction_bp, url_prefix = '/transaction')
app.register_blueprint(utxo_verify_bp, url_prefix = '/utxo_verify')

@app.route('/')
def index():
    return render_template('form.html')

if __name__ == "__main__":
    app.run()