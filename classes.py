class IndicatorsData:
    """Gets Indicatr Values and return them from the function"""
    def __init__(self, df):
        self.df = df
        self.stock_price = self.df["close"][-1]

    def trend_indicators_data(self, indicator=None):
        import ta.trend
        trend = ta.trend
        if indicator == "EMA25":
            ema_25_data = trend.EMAIndicator(close=self.df["close"], window=25).ema_indicator()
            return ema_25_data
        if indicator == "EMA50":
            ema_50_data = trend.EMAIndicator(close=self.df["close"], window=50).ema_indicator()
            return ema_50_data
        if indicator == "MACD":
            macd_data = trend.MACD(close=self.df["close"]).macd()
            return macd_data
        if indicator == "MACD-SIG":
            macd_signal_data = trend.MACD(close=self.df["close"]).macd_signal()
            return macd_signal_data

    def momentum_indicators_data(self, indicator=None):
        import ta.momentum
        momentum = ta.momentum
        if indicator == "RSI":
            rsi_data = momentum.RSIIndicator(close=self.df['close']).rsi()
            return rsi_data
        if indicator == "STOCH":
            stochastic_data = momentum.StochasticOscillator(high=self.df["high"], low=self.df["low"], close=self.df["close"]).stoch()
            return stochastic_data
        if indicator == "STOCH-SIG":
            stochastic_signal_data = momentum.StochasticOscillator(high=self.df["high"], low=self.df["low"], close=self.df["close"]).stoch_signal()
            return stochastic_signal_data

    def volatility_indicators_data(self, indicator=None):
        import ta.volatility
        volatility = ta.volatility
        if indicator == "BB-HIGH":
            bb_high_data = volatility.BollingerBands(close=self.df["close"]).bollinger_hband()
            return bb_high_data
        if indicator == "BB-LOW":
            bb_low_data = volatility.BollingerBands(close=self.df["close"]).bollinger_lband()
            return bb_low_data
        if indicator == "BB-MID":
            bb_middle_data = volatility.BollingerBands(close=self.df["close"]).bollinger_mavg()
            return bb_middle_data


class CandlestickData:
    """Gets Candlestick True/False values and returns them"""
    def create(self, df):
        from candlestick import candlestick
        inverted_hammer = candlestick.inverted_hammer(df, target='result')["result"][-1]
        hammer = candlestick.hammer(df, target='result')["result"][-1]
        hanging_man = candlestick.hanging_man(df, target='result')["result"][-1]
        bearish_harami = candlestick.bearish_harami(df, target='result')["result"][-1]
        bullish_harami = candlestick.bullish_harami(df, target='result')["result"][-1]
        dark_cloud_cover = candlestick.dark_cloud_cover(df, target='result')["result"][-1]
        doji = candlestick.doji(df, target='result')["result"][-1]
        doji_star = candlestick.doji_star(df, target='result')["result"][-1]
        dragonfly_doji = candlestick.dragonfly_doji(df, target='result')["result"][-1]
        gravestone_doji = candlestick.gravestone_doji(df, target='result')["result"][-1]
        bearish_engulfing = candlestick.bearish_engulfing(df, target='result')["result"][-1]
        bullish_engulfing = candlestick.bullish_engulfing(df, target='result')["result"][-1]
        morningstar = candlestick.morning_star(df, target='result')["result"][-1]
        morningstar_doji = candlestick.morning_star_doji(df, target='result')["result"][-1]
        piercing_pattern = candlestick.piercing_pattern(df, target='result')["result"][-1]
        rain_drop = candlestick.rain_drop(df, target='result')["result"][-1]
        rain_drop_doji = candlestick.rain_drop_doji(df, target='result')["result"][-1]
        star = candlestick.star(df, target='result')["result"][-1]
        shooting_star = candlestick.shooting_star(df, target='result')["result"][-1]
        candlestick_list = [inverted_hammer,
                            hammer,
                            hanging_man,
                            bearish_harami,
                            bullish_harami,
                            dark_cloud_cover,
                            doji,
                            doji_star,
                            dragonfly_doji,
                            gravestone_doji,
                            bearish_engulfing,
                            bullish_engulfing,
                            morningstar,
                            morningstar_doji,
                            piercing_pattern,
                            rain_drop,
                            rain_drop_doji,
                            star,
                            shooting_star]
        return candlestick_list


class AnalyseAndReturn:
    def __init__(self, df, ticker):
        self.df = df
        self.ticker = ticker
        self.indicators = IndicatorsData(df=self.df)
        self.stock_price = self.df["close"][-1]
        self.ta_b = [0, []]
        self.ta_s = [0, []]

    def analyse_all_indicators(self):
        ema_cross_signal = None
        macd_signal = None
        rsi_signal = False
        stoch_signal = None
        bb_signal = None
        # --------------------------------------------CREATES-----------------------------------------
        # -------------TREND-INDICATORS------------------
        ema25 = self.indicators.trend_indicators_data(indicator="EMA25")
        ema50 = self.indicators.trend_indicators_data(indicator="EMA50")
        # Oscillates between20 and -20
        macd = self.indicators.trend_indicators_data(indicator="MACD")  # Blue Line
        macd_sig_line = self.indicators.trend_indicators_data(indicator="MACD-SIG")  # Orange Line
        # -------------MOMENTUM-INDICATORS----------------
        rsi = self.indicators.momentum_indicators_data(indicator="RSI")
        stoch = self.indicators.momentum_indicators_data(indicator="STOCH")  # Blue Line
        stoch_sig_line = self.indicators.momentum_indicators_data(indicator="STOCH-SIG")  # Orange Line
        # -------------VOLATILITY-INDICATORS--------------
        bb_high = self.indicators.volatility_indicators_data(indicator="BB-HIGH")
        bb_low = self.indicators.volatility_indicators_data(indicator="BB-LOW")
        bb_mid = self.indicators.volatility_indicators_data(indicator="BB-MID")
        # ------------------------------------IF----------------------------------
        # -------------TREND-INDICATORS------------------
        if ema25[-1] >= ema50[-1]:
            # print("BUY: EMA 25 above EMA 50.")
            ema_cross_signal = "BUY"
            self.ta_b[0] += 1
            self.ta_b[1].append("EMA")
        elif ema25[-1] <= ema50[-1]:
            ema_cross_signal = "SELL"
            # print("SELL: EMA 25 below EMA 50.")
            self.ta_s[0] += 1
            self.ta_s[1].append("EMA")
        else:
            ema_cross_signal = "HOLD"
            # print("HOLD: EMA CROSSOVER")
        # For Shorting
        if macd[-1] > 0:  # Strong SELL
            if macd[-1] < macd_sig_line[-1]:  # Strong SELL
                macd_signal = "STRONG SELL"
                # print("STRONG SELL: MACD above 0 and Negative Divergence.")
                self.ta_s[0] += 1
                self.ta_s[1].append("MACD")
            else:  # SELL
                macd_signal = "SELL"
                # print("SELL: MACD above 0.")
                self.ta_s[0] += 1
                self.ta_s[1].append("MACD")
        # For Buying
        elif macd[-1] < 0:  # BUY
            if macd[-1] > macd_sig_line[-1]:  # Strong BUY
                macd_signal = "STRONG BUY"
                # print("STRONG BUY: MACD below 0 and Positive Divergence.")
                self.ta_b[0] += 1
                self.ta_b[1].append("MACD")
            else:  # BUY
                macd_signal = "BUY"
                # print("BUY: MACD below 0 and Negative Divergence.")
                self.ta_b[0] += 1
                self.ta_b[1].append("MACD")
        else:
            macd_signal = "HOLD"
            # print("HOLD: MACD")
        # -------------MOMENTUM-INDICATORS----------------
        if rsi[-1] >= 70:
            # print("SELL: RSI Looks Overbought.")
            rsi_signal = "SELL"
            self.ta_s[0] += 1
            self.ta_s[1].append("RSI")
        # For Buying
        elif rsi[-1] <= 30:
            rsi_signal = "BUY"
            # print("BUY: RSI Looks Oversold.")
            self.ta_b[0] += 1
            self.ta_b[1].append("RSI")
        else:
            rsi_signal = "HOLD"
            # print("HOLD: RSI")
        # For Buying
        if stoch[-1] and stoch_sig_line[-1] <= 30:
            if stoch[-1] > stoch_sig_line[-1]:
                stoch_signal = "STRONG BUY"
                # print("STRONG BUY: STOCHASTIC")
                self.ta_b[0] += 1
                self.ta_b[1].append("STOCHASTIC")
            else:
                stoch_signal = "BUY"
                # print("BUY: STOCHASTIC")
                self.ta_b[0] += 1
                self.ta_b[1].append("STOCHASTIC")
        # For Shorting
        elif stoch[-1] and stoch_sig_line[-1] >= 70:
            if stoch[-1] < stoch_sig_line[-1]:
                stoch_signal = "STRONG SELL"
                # print("STRONG SELL: STOCHASTIC")
                self.ta_s[0] += 1
                self.ta_s[1].append("STOCHASTIC")
            else:
                stoch_signal = "SELL"
                # print("SELL: STOCHASTIC")
                self.ta_b[0] += 1
                self.ta_b[1].append("STOCHASTIC")
        else:
            stoch_signal = "HOLD"
            # print("HOLD: STOCHASTIC")
        # -------------VOLATILITY-INDICATORS--------------
        a = bb_high[-1] - bb_low[-1]
        b = a / 5
        bc = bb_high[-1] - b
        sc = bb_low[-1] + b
        # For Shorting
        if self.stock_price > bc:
            if bb_high[-1] <= self.stock_price:
                bb_signal = "STRONG SELL"
                # print("STRONG SELL: STOCK PRICE near BB HIGH.")
                self.ta_b[0] += 1
                self.ta_b[1].append("BB")
            else:
                bb_signal = "SELL"
                # print("SELL: STOCK PRICE near BB HIGH.")
                self.ta_b[0] += 1
                self.ta_b[1].append("BB")
        # For Buying
        if self.stock_price < sc:
            if bb_low[-1] <= self.stock_price:
                bb_signal = "STRONG BUY"
                # print("STRONG BUY: STOCK PRICE near BB LOW.")
                self.ta_b[0] += 1
                self.ta_b[1].append("BB")
            else:
                bb_signal = "BUY"
                # print("BUY: STOCK PRICE near BB LOW.")
                self.ta_b[0] += 1
                self.ta_b[1].append("BB")
        # ----------------------------RETURNS---------------------
        return {"SIGNALS":
                    {"EMA CROSS": ema_cross_signal,
                     "MACD": macd_signal,
                     "RSI": rsi_signal,
                     "STOCH": stoch_signal,
                     "BB": bb_signal},
                "INDICATOR VALUES":
                    {"EMA25": ema25,
                     "EMA50": ema50,
                     "MACD": macd,
                     "MACD SIG LINE": macd_sig_line,
                     "RSI": rsi,
                     "STOCH": stoch,
                     "STOCH SIG LINE": stoch_sig_line,
                     "BB HIGH": bb_high,
                     "BB MID": bb_mid,
                     "BB LOW": bb_low}
                }

    def return_indicator_values(self, indicator_values):
        print(f"STOCK PRICE: {self.stock_price}")
        print(f"EMA 25 at {indicator_values['EMA25'][-1].round(2)}".lower())
        print(f"EMA 50 at {indicator_values['EMA50'][-1].round(2)}".lower())
        print(f"MACD(Blue Line) at {indicator_values['MACD'][-1].round(2)}".lower())
        print(f"MACD SIGNAL LINE(Orange Line) at {indicator_values['MACD SIG LINE'][-1].round(2)}".lower())
        print(f"RSI at {indicator_values['RSI'][-1].round(2)}".lower())
        print(f"STOCHASTIC(Blue Line) at {indicator_values['STOCH'][-1].round(2)}".lower())
        print(f"STOCHASTIC SIGNAL LINE(Orange Line) at {indicator_values['STOCH SIG LINE'][-1].round(2)}".lower())
        print(f"BB HIGH at {indicator_values['BB HIGH'][-1].round(2)}".lower())
        print(f"BB MID at {indicator_values['BB MID'][-1].round(2)}".lower())
        print(f"BB LOW at {indicator_values['BB LOW'][-1].round(2)}".lower())

    def return_signal_why(self):
        pass

    def analyse_candlesticks(self):
        candle_b = 0
        candle_s = 0
        candle_indecision = 0
        candle_b_list = []
        candle_s_list = []
        candle_indecision_list = []
        candlestick_names = ['inverted_hammer', 'hammer', 'hanging_man', 'bearish_harami', 'bullish_harami',
                             'dark_cloud_cover', "doji", "doji_star", "dragonfly_doji", "gravestone_doji",
                             "bearish_engulfing", "bullish_engulfing", "morningstar", "morningstar_doji",
                             "piercing_pattern", "rain_drop", "rain_drop_doji", "star", "shooting_star"]
        candlestick_data = [{"inverted_hammer": {"found_in_downtrend/uptrend": "downtrend", "signifies": "uptrend"}},
                            {"hammer": {"found_in_downtrend/uptrend": "downtrend", "signifies": "uptrend"}},
                            {"hanging_man": {"found_in_downtrend/uptrend": "uptrend", "signifies": "downtrend"}},
                            {"bearish_harami": {"found_in_downtrend/uptrend": "uptrend", "signifies": "downtrend"}},
                            {"bullish_harami": {"found_in_downtrend/uptrend": "downtrend", "signifies": "uptrend"}},
                            {"dark_cloud_cover": {"found_in_downtrend/uptrend": "uptrend", "signifies": "downtrend"}},
                            {"doji": {"found_in_downtrend/uptrend": "both", "signifies": "both"}},
                            {"doji_star": {"found_in_downtrend/uptrend": "downtrend", "signifies": "uptrend"}},
                            {"dragonfly_doji": {"found_in_downtrend/uptrend": "downtrend", "signifies": "uptrend"}},
                            {"gravestone_doji": {"found_in_downtrend/uptrend": "uptrend", "signifies": "downtrend"}},
                            {"bearish_engulfing": {"found_in_downtrend/uptrend": "uptrend", "signifies": "downtrend"}},
                            {"bullish_engulfing": {"found_in_downtrend/uptrend": "downtrend", "signifies": "uptrend"}},
                            {"morningstar": {"found_in_downtrend/uptrend": "downtrend", "signifies": "uptrend"}},
                            {"morningstar_doji": {"found_in_downtrend/uptrend": "downtrend", "signifies": "uptrend"}},
                            {"piercing_pattern": {"found_in_downtrend/uptrend": "downtrend", "signifies": "uptrend"}},
                            {"rain_drop": {"found_in_downtrend/uptrend": "NA", "signifies": "NA"}},
                            {"rain_drop_doji": {"found_in_downtrend/uptrend": "NA", "signifies": "NA"}},
                            {"star": {"found_in_downtrend/uptrend": "both", "signifies": "both"}},
                            {"shooting_star": {"found_in_downtrend/uptrend": "uptrend", "signifies": "downtrend"}}]
        candlestick_found = [{'inverted_hammer': 'downtrend'}, {'hammer': 'downtrend'}, {'hanging_man': 'uptrend'},
                             {'bearish_harami': 'uptrend'}, {'bullish_harami': 'downtrend'},
                             {'dark_cloud_cover': 'uptrend'}, {'doji': 'both'}, {'doji_star': 'downtrend'},
                             {'dragonfly_doji': 'downtrend'}, {'gravestone_doji': 'uptrend'},
                             {'bearish_engulfing': 'uptrend'}, {'bullish_engulfing': 'downtrend'},
                             {'morningstar': 'downtrend'}, {'morningstar_doji': 'downtrend'},
                             {'piercing_pattern': 'downtrend'}, {'rain_drop': 'NA'}, {'rain_drop_doji': 'NA'},
                             {'star': 'both'}, {'shooting_star': 'uptrend'}]
        candlestick_signifies = [{'inverted_hammer': 'uptrend'}, {'hammer': 'uptrend'}, {'hanging_man': 'downtrend'},
                                 {'bearish_harami': 'downtrend'}, {'bullish_harami': 'uptrend'},
                                 {'dark_cloud_cover': 'downtrend'}, {'doji': 'both'}, {'doji_star': 'uptrend'},
                                 {'dragonfly_doji': 'uptrend'}, {'gravestone_doji': 'downtrend'},
                                 {'bearish_engulfing': 'downtrend'}, {'bullish_engulfing': 'uptrend'},
                                 {'morningstar': 'uptrend'}, {'morningstar_doji': 'uptrend'},
                                 {'piercing_pattern': 'uptrend'}, {'rain_drop': 'NA'}, {'rain_drop_doji': 'NA'},
                                 {'star': 'both'}, {'shooting_star': 'downtrend'}]
        c = CandlestickData()
        b = c.create(df=self.df)
        bool_list = []
        n = -1
        for i in b:
            n += 1
            bool_list.append({candlestick_names[n]: b[n]})
        length_of_list = 19
        s = None
        for i in range(length_of_list):
            if bool_list[i][candlestick_names[i]]:
                if candlestick_signifies[i][candlestick_names[i]] == "downtrend":
                    candle_s += 1
                    candle_s_list.append(candlestick_names[i])
                elif candlestick_signifies[i][candlestick_names[i]] == "uptrend":
                    candle_b += 1
                    candle_b_list.append(candlestick_names[i])
                else:
                    if candlestick_names[i] != "rain_drop" or "rain_drop_doji":
                        candle_indecision += 1
                        candle_indecision_list.append(candlestick_names[i])
        return [candle_b, candle_b_list, candle_indecision, candle_indecision_list, candle_s, candle_s_list]


def generate_data(ticker):  # Generates Stock Data
    """Generates Stock Data as per Ticker Symbol"""
    import yahoo_fin.stock_info as si
    df = {"close": [None]}
    try:
        df = si.get_data(ticker=f"{ticker}.NS", start_date="2022-02-28")  # Y/M/D 2022-01-01
    except:  # AssertionError
        try:
            df = si.get_data(ticker=f"{ticker}", start_date="2022-01-01")
        except:  # AssertionError
            print("Symbol does not exist")
    return df


def get_tickers():
    from nsetools import Nse
    nse = Nse()
    all_stock_codes = nse.get_stock_codes()
    ticker_list = []
    for i in all_stock_codes:
        ticker_list.append(i)
    return ticker_list

stocks_to_be_analysed = []
def get_and_analyse_stocks(start, end):
    if end == "":
        end = 1753
    tickers_list = get_tickers()
    print(len(tickers_list))
    valid_stocks_to_be_analysed = []
    n = 0
    for stock_ticker in tickers_list:
        n += 1
        if n >= start:  # 100 1000
            if n <= end:
                print(n)
                data = generate_data(stock_ticker)
                if data["close"][-1] != None:
                    if data["close"][-1] >= 50:
                        if data["volume"][-1] >= 5000:
                            valid_stocks_to_be_analysed.append(stock_ticker)
    for i in valid_stocks_to_be_analysed:
        stocks_to_be_analysed.append(i)


def create_table(indicators_signals, ticker):
    from prettytable import PrettyTable
    ema_cross_buy_there = indicators_signals["EMA CROSS"]
    macd_buy_there = indicators_signals["MACD"]
    rsi_buy_there = indicators_signals["RSI"]
    stoch_buy_there = indicators_signals["STOCH"]
    bb_buy_there = indicators_signals["BB"]
    table = PrettyTable()
    table.field_names = ["Indicator Names", "ACTION"]
    table.add_row(["EMA CROSS(lagging-strong)", ema_cross_buy_there])
    table.add_row(["MACD(lagging-strong)", macd_buy_there])
    table.add_row(["RSI(both-weak)", rsi_buy_there])
    table.add_row(["STOCH(both-strong)", stoch_buy_there])
    table.add_row(["BB(both-weak)", bb_buy_there])
    table.align = "l"
    return [table, ticker]
