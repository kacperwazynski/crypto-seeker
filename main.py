import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from manager import manager
from models import db

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/crypto_seeker",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")

db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def main():
    manager.load_coin_data()
    if request.method == "POST":
        btn = request.form.get("btn")
        sort_map = {
            "7day_asc": "7day_asc",
            "7day_dsc": "7day_dsc",
            "30day_dsc": "30day_dsc",
            "30day_asc": "30day_asc",
            "asc": "ticker_asc",
            "dsc": "ticker_dsc",
            "today_dsc": "today_dsc",
            "today_asc": "today_asc",
            "placeasc": "placeasc",
            "placedsc": "placedsc",
        }
        if btn in sort_map:
            manager.sortmethod = sort_map[btn]
            manager.sort_dict()
        elif btn == "download data":
            manager.download_coin_data()
            manager.load_coin_data()

    return render_template(
        "main_site.html",
        coindict=manager.coindict,
        limit_day=manager.rate_limit_day,
        nextdownloadtime=f"{manager.nextdownload.hour}:{manager.nextdownload.minute:02d}",
        lastdownloadtime=manager.lastdownload.strftime("%m/%d/%Y %H:%M"),
    )


@app.route("/portfolio_calculator/", methods=["GET", "POST"])
def portfolio():
    manager.load_coin_list()
    if request.method == "POST":
        btn = request.form.get("btn", "")
        if btn == "Add":
            exists = False
            position = 0
            for coin in manager.portfolio_calculator:
                if coin[1] == request.form["ticker"]:
                    exists = True
                    break
                position += 1

            price = 0.0
            for coin in manager.coindict.values():
                if coin["symbol"] == request.form["ticker"]:
                    price = float(
                        coin["price"].replace(" ", "").replace("$", "").replace(",", "")
                    )
                    break

            amount = float(request.form["amount"])
            if not exists:
                manager.portfolio_calculator_value += amount * price
                manager.portfolio_calculator.append(
                    [
                        amount,
                        request.form["ticker"],
                        round(amount * price, 2),
                        manager.get_hex(request.form["ticker"]),
                        0,
                    ]
                )
            else:
                manager.portfolio_calculator_value += amount * price
                manager.portfolio_calculator[position][0] = (
                    float(manager.portfolio_calculator[position][0]) + amount
                )
                manager.portfolio_calculator[position][2] = int(
                    manager.portfolio_calculator[position][2]
                ) + round(amount * price, 2)

            for coin in manager.portfolio_calculator:
                if manager.portfolio_calculator_value > 0:
                    coin[4] = round(
                        (coin[2] / manager.portfolio_calculator_value) * 100, 2
                    )

        elif btn.startswith("remove"):
            ticker = btn.replace("remove", "")
            position = 0
            for item in manager.portfolio_calculator:
                if item[1] == ticker:
                    manager.portfolio_calculator_value -= item[2]
                    manager.portfolio_calculator.pop(position)
                    break
                position += 1
            if len(manager.portfolio_calculator) == 0:
                manager.portfolio_calculator_value = 0
            for coin in manager.portfolio_calculator:
                if manager.portfolio_calculator_value > 0:
                    coin[4] = round(
                        (coin[2] / manager.portfolio_calculator_value) * 100, 2
                    )

    return render_template(
        "portfolio_calculator.html",
        list=manager.coinlist,
        portfolio_data=manager.portfolio_calculator,
        value=round(manager.portfolio_calculator_value, 2),
    )


@app.route("/news_feed", methods=["GET", "POST"])
def news():
    manager.load_news_articles()
    if request.method == "POST":
        if request.form.get("btn") == "download articles":
            manager.download_news_articles()
            manager.load_news_articles()

    return render_template(
        "news_feed.html",
        articles_data=manager.articledict,
        limit_day=manager.rate_limit_day,
    )


@app.route("/coin/<symbol>", methods=["GET", "POST"])
def coin(symbol):
    position = 0
    if request.method == "POST":
        position = int(request.form.get("click", 0))
    # Fallback: find by symbol if position is not provided
    coin_data = manager.coindict.get(position)
    if coin_data is None:
        for data in manager.coindict.values():
            if data.get("symbol") == symbol:
                coin_data = data
                break
    return render_template("coin.html", symbol=symbol, coindict=coin_data)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
