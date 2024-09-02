# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app/imdb

# Copy the imdb directory contents into the container at /app
COPY . /app/imdb

# Add this to your Dockerfile to ensure the output directory exists
RUN mkdir -p /app/imdb/imdb/output

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Scrapy
RUN pip install scrapy

# Command to run the Scrapy spider when the container launches
CMD ["scrapy", "crawl", "imdb_scraper"]