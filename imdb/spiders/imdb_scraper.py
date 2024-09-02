import scrapy
import json


class ImdbScraperSpider(scrapy.Spider):
    """
        A Scrapy spider for scraping detailed information about IMDb's Top 50 movies.

        This spider starts by scraping the IMDb page listing the top 100 movies, extracts
        the necessary data such as movie names, release years, and movie URLs etc.

        Attributes:
            name (str): The name of the spider, used for running the spider.
            allowed_domains (list): List of domains the spider is allowed to crawl.
            start_urls (list): The initial URL to start scraping from.
            custom_settings (dict): Custom settings for the spider, such as download delay
                and concurrent requests.
            headers (dict): Custom headers to simulate a real browser request.
    """
    name = "imdb_scraper"
    allowed_domains = ["imdb.com"]
    # The initial URL to start scraping fro
    start_url = "https://www.imdb.com/search/title/?groups=top_100"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 8,
    }
    # Custom headers to simulate a real browser request
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Cookie': 'uu=eyJpZCI6InV1NjdkNmI2YzgyOGI0NDMzMjhhZGMiLCJwcmVmZXJlbmNlcyI6eyJmaW5kX2luY2x1ZGVfYWR1bHQiOmZhbHNlfX0=; session-id=146-7955278-3336250; ubid-main=130-1273115-0126250; session-id-time=2082787201l; mp_f99fd93d342102be249005dee41b33da_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A18ddfdbff69fa1-0b683b892da25b-15462c6f-ff000-18ddfdbff6afa1%22%2C%22%24device_id%22%3A%20%2218ddfdbff69fa1-0b683b892da25b-15462c6f-ff000-18ddfdbff6afa1%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%7D; session-token=yTsYfi/2Cqb69FtATm9KRGNwpAL0AyRKK2ye4NRY4C5gaSr/b8jRFlVILUk33ybjnUGXglvu7aGh3M9GYlFv1gEItGlM0au3bwpeRAZw0bIsulCBQtfnJ6f/wXKe/iPTKL/k1RzNbsZsDzAvn9ACPVZm+roy1bEYLUGBkl1lh+4aDEvCgP+7NWSxAscHaxlGRf1L02DuBYVm89Yy+f/4o7EnwvkoOX5gWnAQh2nXQ6Ykdks1pXMKCEMgh3wSSJNtX/QkRHqP/l6Inr9hvefQOsSla6PVjYulaF5g+9x9QMeQ9sDEn/Yq7Trr/vTuORafIcjCFP9OQ8FwzWViasNtfG500Mu5eWKF',
        'Priority': 'u=0, i',
        'Sec-CH-UA': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"Linux"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        """Yielding a request with custom headers and callback to parse the response"""
        yield scrapy.Request(url=self.start_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        """Parse the response to extract movie data from the page.
        Extracting JSON data from the script tag containing movie information"""
        script = json.loads(response.css("script#__NEXT_DATA__::text").get())
        items = script['props']['pageProps']['searchResults']['titleResults']['titleListItems']
        for i, item in enumerate(items, start=1):
            movie_name = item['originalTitleText']
            year_of_release = item['releaseYear']
            movie_url = f'https://www.imdb.com/title/{item["titleId"]}/?ref_=sr_t_{i}'
            meta = response.meta
            meta.update({
                "movie name": movie_name,
                "year of release": year_of_release,
            })
            """Yielding a request to get additional details for each movie"""
            yield scrapy.Request(url=movie_url, callback=self.parse_more_fields, dont_filter=True, meta=meta, headers=self.headers)

    # Parses additional details for each movie
    def parse_more_fields(self, response):
        """Extracting director and stars from the movie's detail page"""
        director = response.xpath('//div[@class="sc-1f50b7c-3 gLpgJQ"]/div/ul/li[1]//li/a/text()').get()
        stars = response.xpath('//div[@class="sc-1f50b7c-3 gLpgJQ"]/div/ul/li[3]//li//a/text()').getall()
        """Yields the final movie details"""
        yield {
            "movie name ": response.meta.get("movie name"),
            "year of release": response.meta.get("year of release"),
            "director": director,
            "stars": stars
        }
