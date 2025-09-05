# Proxy Validator & Data Scraper

A multithreaded Python tool for validating proxies and scraping web data using BeautifulSoup.


---

## Overview

This project validates a list of HTTP proxies using Python's threading and queue modules. Valid proxies are saved for web scraping activities. The script fetches sample pages from Flipkart using proxies. BeautifulSoup is used to parse and extract key data from the target pages. Ideal for anyone needing reliable proxies and robust data extraction from protected sites.

---

## Features

- Multi-threaded proxy checking
- Automated validation (HTTP status)
- Saves all working proxies to `valid_proxies.txt`
- Data parsing using BeautifulSoup
- Easily customizable for different websites

---

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/your-username/proxy-validator-scraper.git
    cd proxy-validator-scraper
    ```

2. Install dependencies:
    ```
    pip install requests beautifulsoup4
    ```

3. Add a list of proxies to `proxy-list.txt` (one per line).

---

## Usage

1. Run the script:
    ```
    python proxy_validator.py
    ```
2. Valid proxies get saved to `valid_proxies.txt`.

3. Example BeautifulSoup parsing:
    ```
    from bs4 import BeautifulSoup

    # after a successful request
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='product-title-class')
    for prod in products:
        print(prod.text)
    ```

---

## Technologies Used

- Python
- threading, queue
- requests
- beautifulsoup4

---

## Project Structure

