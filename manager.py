import cryptocompare
import datetime
import requests
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
from models import *
from sqlalchemy import delete
from datetime import timedelta
from PIL import Image
    
class Manager:
    def __init__(self):
        self.actions = {}
        self.portfolios = []
        self.ticker = ""
        self.price = 0
        self.currency = "USD"
        self.lastdownload = datetime.datetime.now() + relativedelta(days=-1)
        self.nextdownload = datetime.datetime.now()
        self.datetime = datetime.datetime.now()
        self.month_period = 24
        self.dca_amount = 0
        self.coindict = {}
        self.articledict = {}
        self.sortmethod = ""
        self.portfolio_calculator = []
        self.portfolio_calculator_value = 0
        self.rate_limit_day = 0
        self.coinlist = []
        
    #loads coins that the user has selected for portfolio calculations
    def load_coin_list(self):
        coinlist = []
        for data in self.coindict.items():
            coinlist.append(data[1]["symbol"])
        self.coinlist = coinlist

    #downloads news articles from cryptocompare and saves it on the PG databes
    def download_news_articles(self):
        stmt = (delete(Articles).where(Articles.id >= 0))
        db.session.execute(stmt)
        db.session.commit()
        URL = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        request = requests.get(url=URL)
        data = request.json()
        for article in data["Data"]:
            new_article = add_article(article["imageurl"],article["title"],article["url"],article["body"],
                                      article["source_info"]["name"],article["title"],article["source_info"]["img"])
            db.session.add(new_article)
        db.session.commit()
        self.load_rate_limit()

    #loads article data from the server to the managers storage
    def load_news_articles(self):
        articles = Articles.query.all()
        art_number = 0
        for art in articles:
            self.articledict[art_number] = {"imageurl":art.imageurl,"title":art.title,"url":art.url,"body":art.body,
                                            "source_name":art.source_name,"source_img":art.source_img}
            art_number += 1

    #downloads coin metrics from crypto compare and saves it on the database
    def download_coin_data(self):
        if datetime.datetime.now() - manager.lastdownload > timedelta(minutes=10):
            stmt = (delete(Coins).where(Coins.id >= 0))
            db.session.execute(stmt)
            db.session.commit()
            URL = "https://min-api.cryptocompare.com/data/top/mktcapfull?limit=50&tsym=USD"
            req = requests.get(url=URL)
            data = req.json()
            week_past = self.datetime + relativedelta(days=-7)
            month_past = self.datetime + relativedelta(months=-1)
            id = 1
            for coin in data["Data"]:
                self.ticker = coin["CoinInfo"]["Name"]
                one_week_price = cryptocompare.get_historical_price(self.ticker, self.currency, week_past)[self.ticker][self.currency]
                one_month_price = cryptocompare.get_historical_price(self.ticker, self.currency, month_past)[self.ticker][self.currency]
                week_direction = "down" if coin["RAW"]["USD"]["PRICE"] < one_week_price else "up"
                month_direction = "down" if coin["RAW"]["USD"]["PRICE"] < one_month_price else "up"
                day_direction = "down" if float(coin["DISPLAY"]["USD"]["CHANGEPCTDAY"]) < 0 else "up"
                week_change = round((((one_week_price-coin["RAW"]["USD"]["PRICE"])/one_week_price) * 100),2) if week_direction == "down" else round((((coin["RAW"]["USD"]["PRICE"]-one_week_price)/one_week_price) * 100),2)
                month_change = round((((one_month_price-coin["RAW"]["USD"]["PRICE"])/one_month_price) * 100),2) if month_direction == "down" else round((((coin["RAW"]["USD"]["PRICE"]-one_month_price)/one_month_price) * 100),2)

                new_coin = add_coin(id,coin["CoinInfo"]["FullName"],coin["CoinInfo"]["ProofType"],coin["CoinInfo"]["Name"],
                                    coin["DISPLAY"]["USD"]["PRICE"],"/static/"+coin["CoinInfo"]["Name"]+".png",one_week_price,week_direction,
                                    week_change,month_direction,month_change,one_month_price,coin["DISPLAY"]["USD"]["MKTCAP"],
                                    coin["DISPLAY"]["USD"]["TOTALVOLUME24HTO"],coin["DISPLAY"]["USD"]["CHANGEDAY"],
                                    float(coin["DISPLAY"]["USD"]["CHANGEPCTDAY"]),coin["DISPLAY"]["USD"]["MKTCAP"],"/static/info.png",day_direction=day_direction,
                                    supply=str(coin["DISPLAY"]["USD"]["SUPPLY"]),algorithm=str(coin["CoinInfo"]["Algorithm"]),blocknumber=str(coin["CoinInfo"]["BlockNumber"]),
                                    assetlaunchdate=str(coin["CoinInfo"]["AssetLaunchDate"]), maxsupply=str(coin["CoinInfo"]["MaxSupply"]),
                                    blocktime=str(coin["CoinInfo"]["BlockTime"]),blockreward=str(coin["CoinInfo"]["BlockReward"]),
                                    rating=str(coin["CoinInfo"]["Rating"]["Weiss"]["Rating"]),
                                    technologyadoptionrating=str(coin["CoinInfo"]["Rating"]["Weiss"]["TechnologyAdoptionRating"]),
                                    marketperformancerating=str(coin["CoinInfo"]["Rating"]["Weiss"]["MarketPerformanceRating"]))
                db.session.add(new_coin)
                id += 1
            db.session.commit()
            self.load_rate_limit()
            self.lastdownload = datetime.datetime.now()
            self.nextdownload = datetime.datetime.now() + relativedelta(minutes=10)
        else:
            print("10 minutes till last download haven't passed yet")

    #loads coin data from the server to the managers storage
    def load_coin_data(self):
        coins = Coins.query.all()
        self.coindict.clear()
        id = 1
        for coin in coins:
            self.coindict[coin.id] = {"id":id,"coinname":coin.coinname,"prooftype":coin.prooftype,"symbol":coin.symbol,
                                    "price":coin.price,"image":coin.image,"one_week_price":coin.one_week_price,
                                    "week_direction":coin.week_direction,"week_change":coin.week_change,
                                    "month_direction":coin.month_direction,"month_change":coin.month_change,
                                    "one_month_price":coin.one_month_price,"info_icon":coin.info_icon,
                                    "circulating_supply":coin.circulating_supply,"daily_volume":coin.daily_volume,
                                    "day_change":coin.day_change,"day_change_percentage":coin.day_change_percentage,
                                    "day_direction":coin.day_direction,"marketcap":coin.marketcap,
                                    "supply":coin.supply,"algorithm":coin.algorithm,"blocknumber":coin.blocknumber,
                                    "assetlaunchdate":coin.assetlaunchdate,"maxsupply":coin.maxsupply,
                                    "blocktime":coin.blocktime,"blockreward":coin.blockreward,"rating":coin.rating,
                                    "technologyadoptionrating":coin.technologyadoptionrating,
                                    "marketperformancerating":coin.marketperformancerating,
                                    }
            id += 1

    #downloads rate limit of the api
    def load_rate_limit(self):
        URL = "https://min-api.cryptocompare.com/stats/rate/limit"
        r = requests.get(url=URL)
        self.rate_limit_day = r.json()["Data"]["calls_left"]['day']

    def get_hex(self, ticker):
        img = Image.open("./static/"+ticker+".png")
        max_colors = 10000
        dict = img.getcolors(max_colors)
        max = 0
        colour_hex_max = [0, 0, 0]
        colour_hex = [0, 0, 0]
        for colour in dict:
            if not isinstance(colour[1],tuple):
                colour_hex = [0,0,0,0]
            else:
                colour_hex = list(colour[1])
                colour_hex.pop()
            if colour[0] >= max and colour_hex != [255, 255, 255]:
                max = colour[0]
                colour_hex_max = colour_hex
        return '%02x%02x%02x' % (colour_hex_max[0],colour_hex_max[1],colour_hex_max[2])

    def sort_dict(self):
        def sort_by_price(period,direction):
            order_list = []
            tuple_list = []
            for key in self.coindict.keys():
                if self.coindict[key][f"{period}_direction"] == "up":
                    value = self.coindict[key][f"{period}_change"]
                    if period == "day":
                        value = self.coindict[key]['day_change_percentage']
                    tuple = (key,value)
                    tuple_list.append(tuple)
                else:
                    value = self.coindict[key][f"{period}_change"]
                    if period == "day":
                        value = -self.coindict[key]['day_change_percentage']
                    tuple = (key,-value)
                    tuple_list.append(tuple)
            tuple_list.sort(key = lambda x: x[1], reverse=True if direction == "asc" else False)
            for name in tuple_list:
                order_list.append(name[0])

            dict_sorted = {}
            for name in order_list:
                for key in self.coindict.keys():
                    if key == name:
                        dict_sorted[key] = self.coindict[key]
            self.coindict = dict_sorted

        if self.sortmethod == "7day_asc":
            sort_by_price("week","asc")
        elif self.sortmethod == "7day_dsc":
            sort_by_price("week","dsc")
        elif self.sortmethod == "30day_asc":
            sort_by_price("month","asc")
        elif self.sortmethod == "30day_dsc":
            sort_by_price("month","dsc")
        elif self.sortmethod == "today_dsc":
            sort_by_price("day","dsc")
        elif self.sortmethod == "today_asc":
            sort_by_price("day","asc")
        elif self.sortmethod == "ticker_asc":
            dict_sorted = OrderedDict(sorted(self.coindict.items()))
            self.coindict = dict_sorted
        elif self.sortmethod == "ticker_dsc":
            dict_sorted = OrderedDict(sorted(self.coindict.items(),reverse=True))
            self.coindict = dict_sorted
        elif self.sortmethod == "placeasc":
            dict_sorted = OrderedDict(sorted(self.coindict.items()))
            self.coindict = dict_sorted
        elif self.sortmethod == "placedsc":
            dict_sorted = OrderedDict(sorted(self.coindict.items(),reverse=True))
            self.coindict = dict_sorted

manager = Manager()
manager.load_rate_limit()
manager.load_coin_list()
