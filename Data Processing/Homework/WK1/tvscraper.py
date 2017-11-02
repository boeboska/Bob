#!/usr/bin/env python
#
# Name: Bob Borsboom
# Student number: 10802975
# Data Processing WK1
#
#   Extract a list of highest rated TV series from DOM (of IMDB page).
#   This script scrapes IMDB and outputs a CSV file with highest rated tv series.
#   Each TV series entry should contain the following fields:
#   - TV Title
#   - Rating
#   - Genres (comma separated if more than one)
#   - Actors/actresses (comma separated if more than one)
#   - Runtime (only a number!)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv
from pattern.web import URL, DOM

TARGET_URL = "http://www.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&start=1&title_type=tv_series"
BACKUP_HTML = 'tvseries.html'
OUTPUT_CSV = 'tvseries.csv'


def extract_tvseries(dom):

    # define variables
    ALL_FILMS = 50
    FILM_NR = 0

    # create array 
    film_info = []
    for elke_film in range(ALL_FILMS):
        film_info.append([])

    # loop throw top 50 film titles
    for e in dom.by_tag("div.lister-item-content")[:ALL_FILMS]: 

        # add film title to array
        film_info[FILM_NR].append(e.by_tag("h3.lister-item-header")
            [0].by_tag("a")[0].content.encode("UTF8"))

        # add film rating to array
        film_info[FILM_NR].append(e.by_tag("div.ratings-bar")[0].by_tag
            ("div.inline-block")[0].by_tag("strong")[0].content.encode("UTF8"))

        # add film genre to array
        film_info[FILM_NR].append(e.by_class("text-muted ")[0].by_class
            ("genre")[0].content.strip(" ").strip("\n").encode("UTF8")) 

        # create empty variable
        actors = ""

        # loop throw all film actors
        for a in e.by_tag("p")[2].by_tag("a"):
            if actors == "":

                # add the first actor
                actors = a.content.encode("UTF8")
            else:
                # add a comma and the other actors
                actors = actors + ', ' + a.content.encode("UTF8")

        # add all the actors to array
        film_info[FILM_NR].append(actors)

        # add runtime to array
        film_info[FILM_NR].append(e.by_class("text-muted ")[0].by_class
            ("runtime")[0].content.split(" ")[0].encode("UTF8"))

        # search for the next film
        FILM_NR = FILM_NR +1

    return film_info
    

def save_csv(f, tvseries):
    '''
    Output a CSV file containing highest rated TV-series.
    '''
    writer = csv.writer(f)
    writer.writerow(['Title', 'Rating', 'Genre', 'Actors', 'Runtime'])

    # loop throw all the movies
    for film in tvseries:

        # add movie info to the excel file
        writer.writerow(film)

if __name__ == '__main__':
    # Download the HTML file
    url = URL(TARGET_URL)
    html = url.download()

    # Save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # Parse the HTML file into a DOM representation
    dom = DOM(html)

    # Extract the tv series (using the function you implemented)
    tvseries = extract_tvseries(dom)

    # Write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'wb') as output_file:
        save_csv(output_file, tvseries)