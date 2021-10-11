from flask import Flask
from flask import render_template
from flask import request
from iexfinance.stocks import Stock
from datetime import date, datetime
import calendar
import pandas as pd

def set_indices(ticker_length):
    if ticker_length == 1:
        ind1 = 5
        ind2 = -1
        ind3 = -4        
    elif ticker_length == 2:
        ind1= 6
        ind2 = -2
        ind3 = -4
    elif ticker_length == 3:
        ind1 = 7
        ind2 = -3
        ind3 = -4
    elif ticker_length == 4:
        ind1 = 8
        ind2 = -4
        ind3 = -4
    elif ticker_length == 5:
        ind1 = 9
        ind2 = -5
        ind3 = -4 
    return ind1, ind2, ind3

def plus_minus(value):
    plmi1 = ""
    plmi2 = ""
    if value > 0:
        plmi1 = "+"
        plmi2 = "+"
    elif value < 0:
        plmi1 = "-"
        plmi2 = ""
    return plmi1, plmi2

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':

        #Input Fields

        ticker = str(request.form['tickerSymbol'])
        
        #Fetch Data

        IEX_TOKEN = "sk_871e182cc9bb41e1adc7449252cc557b"
        ticker_length = len(ticker)
        ind1, ind2, ind3 = set_indices(ticker_length)
        error_message = ""
        tempData = {}
        try:
            stck = Stock(ticker , token = IEX_TOKEN)
            df = pd.DataFrame(data=stck.get_quote())
            current_date = str(date.today().strftime("%B %d"))
            current_time = str(datetime.now().strftime("%H:%M:%S"))
            current_day = str(date.today().strftime("%A"))
            current_year = str(date.today().strftime("%Y"))
            current_timezone = "PDT"
            company_name = df["companyName"].to_string()
            stock_symbol = df["symbol"].to_string()
            stock_price = df["latestPrice"].to_string()
            value_change = df["change"].to_string()
            perc_change = round((float(value_change[-5:]) / float(stock_price[8:])) * 100 , 2)
            pm1, pm2 = plus_minus(perc_change)


            tempData = {'tickerSymbol': ticker, 'currentDay': current_day,
                       'currentDate': current_date, 'currentTime': current_time,
                       'companyName': company_name[ind1:],'currentYear': current_year, 'currentTimezone': current_timezone,
                       'stockSymbol':stock_symbol[ind2:], 'stockPrice':stock_price[ind1:], 'valueChange':value_change[ind3:],
                       'percChange':perc_change, 'pm1':pm1, 'pm2':pm2, 'errorMessage':error_message}

        except:
            error_message = "Invalid Ticker Symbol! Please Enter a valid Symbol!"

        return render_template('index.html', **tempData)

if __name__ == '__main__':
    app.run(debug=True) 