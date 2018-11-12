from flask import Flask
from flask import request
import tax_app
app = Flask(__name__)

# TODO: use json to return an object with all info

@app.route('/')
def hello_world():
    return 'Aye!'

@app.route('/after_tax_income')
def after_tax_income():
    income = float(request.args.get('income'))
    #status = request.args.get('status')
    after_tax = str(tax_app.tax(income))
    return after_tax

if __name__ == "__main__":
    app.run(
    #host="0.0.0.0",
    # port=80
    port=5000
    )
