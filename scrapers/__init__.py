from scrapers.expedia import ExpediaScraper
from scrapers.orbitz import OrbitzScraper
from scrapers.priceline import PricelineScraper
from scrapers.travelocity import TravelocityScraper
from scrapers.hilton import HiltonScraper


SCRAPERS = [
    ExpediaScraper,
    OrbitzScraper,
    PricelineScraper,
    TravelocityScraper,
    HiltonScraper,
]
SCRAPER_MAP = {s.provider.lower(): s for s in SCRAPERS}


def get_scraper(provider):
    return SCRAPER_MAP.get(provider.lower())
