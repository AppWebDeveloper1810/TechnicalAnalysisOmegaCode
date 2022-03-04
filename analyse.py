from classes import *
import pprint
from datetime import datetime
import pyttsx3
# stocks_to_be_analysed = get_and_analyse_stocks(0, 1700)
engine = pyttsx3.init()
stocks_to_be_analysed = get_tickers()
for i in stocks_to_be_analysed:
    if i == "NIRAJISPAT":
        stocks_to_be_analysed.remove("NIRAJISPAT")
        stocks_to_be_analysed.remove("SYMBOL")
print(stocks_to_be_analysed)

all_stocks_to_be_bought_5 = []
all_stocks_to_be_strong_bought_5 = []
all_stocks_to_be_strong_sold_5 = []
all_stocks_to_be_sold_5 = []
all_stocks_to_be_bought_4 = []
all_stocks_to_be_strong_bought_4 = []
all_stocks_to_be_strong_sold_4 = []
all_stocks_to_be_sold_4 = []
all_stocks_to_be_overall_bought = []
all_stocks_to_be_overall_sold = []
stock_tables = []


def calculate_matched_tickers(start, end):
    n = 1
    if end == "":
        ticker_list = get_tickers()
        end = len(ticker_list)
    for ticker in stocks_to_be_analysed:
        if start <= n:
            if end >= n:
                try:
                    print(n)
                    print(ticker)
                    dataframe = generate_data(ticker=ticker)
                    analyse = AnalyseAndReturn(df=dataframe, ticker=ticker)
                    indicators_data = analyse.analyse_all_indicators()
                    indicator_values = indicators_data["INDICATOR VALUES"]
                    indicator_signals = indicators_data["SIGNALS"]
                    indicator_signal_list = [indicator_signals["EMA CROSS"],
                                             indicator_signals["MACD"],
                                             indicator_signals["RSI"],
                                             indicator_signals["STOCH"],
                                             indicator_signals["BB"]]
                    # Checks for signals
                    if indicator_signal_list.count("STRONG BUY") >= 5:
                        all_stocks_to_be_strong_bought_5.append(ticker)
                    elif indicator_signal_list.count("BUY") >= 5:
                        all_stocks_to_be_bought_5.append(ticker)
                    elif indicator_signal_list.count("STRONG SELL") >= 5:
                        all_stocks_to_be_strong_sold_5.append(ticker)
                    elif indicator_signal_list.count("SELL") >= 5:
                        all_stocks_to_be_sold_5.append(ticker)

                    elif indicator_signal_list.count("STRONG BUY") >= 4:
                        all_stocks_to_be_strong_bought_4.append(ticker)
                    elif indicator_signal_list.count("BUY") >= 4:
                        all_stocks_to_be_bought_4.append(ticker)
                    elif indicator_signal_list.count("STRONG SELL") >= 4:
                        all_stocks_to_be_strong_sold_4.append(ticker)
                    elif indicator_signal_list.count("SELL") >= 4:
                        all_stocks_to_be_sold_4.append(ticker)

                    for signal in indicator_signal_list:
                        if signal == "STRONG SELL" or "SELL":
                            if all_stocks_to_be_overall_sold.count(ticker) == 0:
                                all_stocks_to_be_overall_sold.append(ticker)
                        elif signal == "STRONG BUY" or "BUY":
                            if all_stocks_to_be_overall_bought.count(ticker) == 0:
                                all_stocks_to_be_overall_bought.append(ticker)

                    # analyse.return_indicator_values(indicator_values=indicator_values)
                    table_data = create_table(indicators_signals=indicator_signals, ticker=ticker)
                    stock_tables.append(table_data)
                    # print(table_data[0])
                    all_signals = []
                    all_signals.append(f"TIME: {datetime.now()}")
                    n += 1
                except:
                    print("Can't Do")


def print_matched_tickers():
    matched_tickers = {"Buy 5":
            all_stocks_to_be_bought_5,
            "Strong Buy  5":
            all_stocks_to_be_strong_bought_5,
            "Strong Sell 5":
            all_stocks_to_be_strong_sold_5,
            "Sell 5":
            all_stocks_to_be_sold_5,
            "Buy 4":
            all_stocks_to_be_bought_4,
            "Strong Buy 4":
            all_stocks_to_be_strong_bought_4,
            "Strong Sell 4":
            all_stocks_to_be_strong_sold_4,
            "Sell 4":
            all_stocks_to_be_sold_4,
            "Overall Buy":
            all_stocks_to_be_overall_bought,
            "Overall Sell":
            all_stocks_to_be_overall_sold, }
    print(matched_tickers)
    return matched_tickers


def run_analyzation():
    engine.say("Analyzation Starting")
    engine.runAndWait()
    calculate_matched_tickers(1, 4)
    matched_tickers = print_matched_tickers()
    engine.say("Analyzation Complete")
    engine.runAndWait()
    engine.say("Signals Printed")
    engine.runAndWait()
    return matched_tickers


