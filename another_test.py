from classes import *
tickers_list = get_tickers()
n = 0
errors = []
for ticker in tickers_list:
    n += 1
    print(n)
    try:
        generate_data(ticker)
    except:
        errors.append([n, ticker])
print(errors)