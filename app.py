from flask import Flask
import git
from src.business_logic.process_query import create_business_logic

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return f'Hello fellow investor! Use "/get_stock_val/" or "/get_stock_change" to check the stock value for tomorrow.'


@app.route('/get_stock_change/<ticker>', methods=['GET'])
def get_stock_change(ticker):
    bl = create_business_logic()
    prediction = bl.do_predictions_for(ticker)[0]

    if prediction < 0:
        return f'The price of {ticker} is going to decrease by {prediction*-1: .2f}.\n You should sell {ticker} stock.'

    if prediction > 0:
        return f'The price of {ticker} is going to increase by {prediction: .2f}.\n You should buy {ticker} stock.'

@app.route('/get_stock_val/<ticker>', methods=['GET'])
def get_stock_value(ticker):
    bl = create_business_logic()
    prediction = bl.do_predictions_for(ticker)[1]

    return f"{prediction: .2f}"


@app.route('/getversion/')
def getversion():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    return f'{sha}\n'

@app.route('/get_accuracy/<ticker>', methods=['GET'])
def get_accuracy(ticker):
    bl = create_business_logic()
    accuracy = bl.get_accuracy(ticker)
    return f'The accuracy of the model is {accuracy: .2f}.\n'

if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=8080, debug=True)
