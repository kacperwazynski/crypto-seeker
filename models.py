from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageurl = db.Column(db.String(1500), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(1500), nullable=False)
    body = db.Column(db.String(8500), nullable=False)
    source_name = db.Column(db.String(1500), nullable=False)
    source_info = db.Column(db.String(1500), nullable=False)
    source_img = db.Column(db.String(1500), nullable=False)


class Coins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coinname = db.Column(db.String(30), nullable=False)
    prooftype = db.Column(db.String(30), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False)
    one_week_price = db.Column(db.Float, nullable=False)
    week_direction = db.Column(db.String(10), nullable=False)
    week_change = db.Column(db.Float, nullable=False)
    month_direction = db.Column(db.String(10), nullable=False)
    month_change = db.Column(db.Float, nullable=False)
    one_month_price = db.Column(db.Float, nullable=False)
    info_icon = db.Column(db.String(20), nullable=False)
    circulating_supply = db.Column(db.String(50), nullable=False)
    daily_volume = db.Column(db.String(50), nullable=False)
    day_change = db.Column(db.String(50), nullable=False)
    day_change_percentage = db.Column(db.Float, nullable=False)
    day_direction = db.Column(db.String(50), nullable=False)
    marketcap = db.Column(db.String(50), nullable=False)
    supply = db.Column(db.String(50), nullable=False)
    algorithm = db.Column(db.String(50), nullable=False)
    blocknumber = db.Column(db.String(50), nullable=False)
    assetlaunchdate = db.Column(db.String(50), nullable=False)
    maxsupply = db.Column(db.String(50), nullable=False)
    blocktime = db.Column(db.String(50), nullable=False)
    blockreward = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(50), nullable=False)
    technologyadoptionrating = db.Column(db.String(50), nullable=False)
    marketperformancerating = db.Column(db.String(50), nullable=False)


def add_article(imageurl, title, url, body, source_name, source_info, source_img):
    return Articles(
        imageurl=imageurl,
        title=title,
        url=url,
        body=body,
        source_name=source_name,
        source_info=source_info,
        source_img=source_img,
    )


def add_coin(
    id,
    coinname,
    prooftype,
    symbol,
    price,
    image,
    one_week_price,
    week_direction,
    week_change,
    month_direction,
    month_change,
    one_month_price,
    circulating_supply,
    daily_volume,
    day_change,
    day_change_percentage,
    marketcap,
    info_icon,
    day_direction,
    supply,
    algorithm,
    blocknumber,
    assetlaunchdate,
    maxsupply,
    blocktime,
    blockreward,
    rating,
    technologyadoptionrating,
    marketperformancerating,
):
    return Coins(
        id=id,
        coinname=coinname,
        prooftype=prooftype,
        symbol=symbol,
        price=price,
        image=image,
        one_week_price=one_week_price,
        week_direction=week_direction,
        week_change=week_change,
        month_direction=month_direction,
        month_change=month_change,
        one_month_price=one_month_price,
        circulating_supply=circulating_supply,
        daily_volume=daily_volume,
        day_change=day_change,
        info_icon=info_icon,
        day_change_percentage=day_change_percentage,
        marketcap=marketcap,
        day_direction=day_direction,
        supply=supply,
        algorithm=algorithm,
        blocknumber=blocknumber,
        assetlaunchdate=assetlaunchdate,
        maxsupply=maxsupply,
        blocktime=blocktime,
        blockreward=blockreward,
        rating=rating,
        technologyadoptionrating=technologyadoptionrating,
        marketperformancerating=marketperformancerating,
    )
