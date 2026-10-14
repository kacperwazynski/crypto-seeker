# Crypto Seeker

A full-stack web application for tracking cryptocurrency market data, calculating portfolio values, and browsing crypto news.

Built with **Flask**, **PostgreSQL**, and the **CryptoCompare API**.

---

## Features

- **Live market overview** – Top coins by market cap with price, 24h / 7d / 30d changes, volume, and market cap
- **Sorting** – Sort by ticker, daily change, weekly change, monthly change, or rank
- **Portfolio calculator** – Add holdings and see real-time portfolio value + allocation percentages (with dominant color extracted from each coin icon)
- **Coin detail pages** – Extended metrics (algorithm, proof type, supply, ratings, etc.)
- **News feed** – Latest crypto news from CryptoCompare
- **Rate-limit awareness** – Shows remaining daily API calls and enforces a cool-down between bulk downloads

---

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Backend      | Python 3, Flask                     |
| Database     | PostgreSQL + SQLAlchemy + Flask-Migrate |
| External API | [CryptoCompare](https://www.cryptocompare.com/) |
| Frontend     | Jinja2 templates, Spectre.css       |
| Icons        | [cryptocurrency-icons](https://github.com/ErikThiart/cryptocurrency-icons) |

---

## Screenshots

> Main Page <img width="1071" height="1327" alt="Main page" src="https://github.com/user-attachments/assets/316613da-bdcc-43cb-aac3-30f7bf3992fd" />
> Coin Info <img width="1078" height="752" alt="Coin info" src="https://github.com/user-attachments/assets/84d85b20-bb6c-492e-971e-aa84b60b3f90" />
> Portfolio Calculator <img width="1072" height="817" alt="Portfolio Calculator" src="https://github.com/user-attachments/assets/179f5e30-cd3e-4a85-aecf-39cd57e4fe6d" />
> News Aggregator <img width="1065" height="1712" alt="News Agregator" src="https://github.com/user-attachments/assets/5f6c2c86-8df8-4d9c-b86a-e9775b48ecd8" />

---

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL running locally (or a remote instance)
- A free [CryptoCompare API key](https://www.cryptocompare.com/cryptopian/api-keys)

### 1. Clone the repository

```bash
git clone https://github.com/kacperwazynski/crypto-seeker.git
cd crypto-seeker
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set:

```env
CRYPTOCOMPARE_API_KEY=your_real_api_key
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/crypto_seeker
SECRET_KEY=any-random-string
```

Create the database if it does not exist:

```bash
createdb crypto_seeker          # or use pgAdmin / psql
```

### 5. Run the application

```bash
python main.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

On first visit, click **“download data”** (top right) to pull the initial coin list.  
A 10-minute cool-down is enforced between downloads to respect API rate limits.

---

## Project Structure

```
crypto-seeker/
├── main.py                 # Flask routes & app factory
├── manager.py              # Business logic (API calls, sorting, portfolio)
├── models.py               # SQLAlchemy models (Coins, Articles)
├── style.css               # Custom styles
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
│   ├── main_site.html      # Market overview
│   ├── portfolio_calculator.html
│   ├── news_feed.html
│   └── coin.html           # Individual coin detail
└── static/                 # Coin icons (see attribution below)
```

---

## API Notes

- Coin data is fetched from CryptoCompare’s `top/mktcapfull` endpoint (currently limited to top 50).
- Historical prices for 7-day / 30-day change calculations use `cryptocompare.get_historical_price`.
- News is pulled from the free CryptoCompare news endpoint.
- The free tier has daily call limits; the UI displays remaining calls.

---

## Icon Attribution

Coin icons in `/static` are from the excellent open-source project:

**[cryptocurrency-icons](https://github.com/ErikThiart/cryptocurrency-icons)** by Erik Thiart  
Licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## Contact

Kacper Ważyński – kacperwazynski@gmail.com

Project Link: [https://github.com/kacperwazynski/crypto-seeker](https://github.com/kacperwazynski/crypto-seeker)
