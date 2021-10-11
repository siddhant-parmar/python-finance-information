
from flask import Flask,render_template,requestpip
from iexfinance.stocks import Stock
from datetime import date, datetime
import calendar
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':

        #Input Fields
        ind1 = ind2 = ind3 =0
        ticker = str(request.form['tickerSymbol'])
        ticker_length = len(ticker)
        if ticker_length == 1:
            ind1 = 5
            ind2 = -1
            ind3 = -4
        elif ticker_length == 2:
            ind1 = 6
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

            #Fetch Data

        IEX_TOKEN = "sk_871e182cc9bb41e1adc7449252cc557b"
        error_message = ""
        tempData = {}

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

        pm1 = ""
        pm2 = ""
        if perc_change > 0:
            pm1 = "+"
            pm2 = "+"
        elif perc_change < 0:
            pm1 = "-"
            pm2 = ""


        tempData = {'tickerSymbol': ticker, 'currentDay': current_day,
                    'currentDate': current_date, 'currentTime': current_time,
                    'companyName': company_name[ind1:],'currentYear': current_year, 'currentTimezone': current_timezone,
                    'stockSymbol':stock_symbol[ind2:], 'stockPrice':stock_price[ind1:], 'valueChange':value_change[ind3:],
                    'percChange':perc_change, 'pm1':pm1, 'pm2':pm2, 'errorMessage':error_message}

        return render_template('index.html', **tempData)

if __name__ == '__main__':
    app.run(debug=True) 