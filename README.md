# IMDb Top 50 Movies Scraper
**This project utilizes Scrapy to extract detailed information about the top 50 movies from IMDb. The spider collects essential data, including movie names, release years, directors, and stars.**


# Scrapy Project with Docker

## Setup

1. **Ensure Docker is Installed**

   Make sure Docker is installed on your system. You can follow the [official Docker installation guide](https://docs.docker.com/get-docker/) for instructions.

2. **Build the Docker Image**

   Navigate to the root directory of your project where the `Dockerfile` is located and build the Docker image:

   ```bash
   docker build -t scrapy-imdb .
   ```
   
3. **To run the Scrapy spider and save the output to a file, use the following command**

   ```bash
   docker run -v $(pwd)/imdb/output:/app/output --name scrapy-container scrapy-imdb scrapy crawl imdb_scraper -o /app/output/test.json
   ```