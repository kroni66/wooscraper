 Product Scraper

This application is a web scraper designed to extract product information from an e-commerce website. It collects product titles, prices, and image URLs, and stores them in a XML feed.

## Features

- Scrapes product data from a specified domain.
- Collects product titles, prices, and image URLs.
- Supports pagination to scrape multiple pages.
- Limits the number of products scraped to a specified maximum.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/product-scraper.git
   cd product-scraper
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the scraper, use the following command:
```bash
python scraper.py [example.com]
```
