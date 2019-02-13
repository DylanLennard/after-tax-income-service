from flask import Flask
from flask import request
from tax_app import get_tax_info, other_tax
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Aye!'


@app.route('/after_tax_income')
def after_tax_income_handler():
    # get params and handle appropriately
    income = float(request.args.get('income'))
    status = request.args.get('selfemploymentstatus')
    status = bool(status) if status.lower() == 'true' else False

    fed_tax, state_tax = get_tax_info(income=income, state="CA")
    federal_amount = fed_tax.calculate(income)
    state_amount = state_tax.calculate(income)
    other_amount = other_tax(income, status)

    after_tax = income - federal_amount - state_amount - other_amount
    after_tax = round(after_tax, 2)

    reponse = dict(
        AfterTaxIncome=after_tax,
        FederalTaxesPaid=federal_amount,
        StateTaxesPaid=state_amount,
        OtherTaxesPaid=other_amount
    )
    return json.dumps(reponse)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
