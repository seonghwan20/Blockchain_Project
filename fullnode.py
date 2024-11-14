from flask import Flask, render_template, request
from route import transaction_bp, utxo_verify_bp
from waitress import serve

app = Flask(__name__)

app.register_blueprint(transaction_bp, url_prefix = '/transaction')
app.register_blueprint(utxo_verify_bp, url_prefix = '/utxo_verify')

@app.route('/')
def index():
    return render_template('form.html')

if __name__ == "__main__":
    # serve(app, host="127.0.0.1", port = 5000)
    app.run()