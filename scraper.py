from traits_scraper import traits_scraper
from cham_scraper import cham_scraper
from augment_scraper import augments_scraper

season = 13

for i in range(1, season + 1):
    traits_scraper(i)
    cham_scraper(i)
    augments_scraper(i)