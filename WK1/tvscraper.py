#!/usr/bin/env python
# Name:
# Student number:
'''
This script scrapes IMDB and outputs a CSV file with highest rated tv series.
'''
import csv

from pattern.web import URL, DOM

TARGET_URL = "http://www.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&start=1&title_type=tv_series"
BACKUP_HTML = 'tvseries.html'
OUTPUT_CSV = 'tvseries.csv'


def extract_tvseries(dom):
    '''
    Extract a list of highest rated TV series from DOM (of IMDB page).

    Each TV series entry should contain the following fields:
    - TV Title
    - Rating
    - Genres (comma separated if more than one)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    '''

    # https://www.clips.uantwerpen.be/pages/pattern-web
    
   
    film_info = []
    for elke_film in range(50):
        film_info.append([])

    number = 0;

    #print dom.body.content
    for e in dom.by_tag("div.lister-item-content")[:50]: # Top 5 film titles.

        film_info[number].append(e.by_tag("h3.lister-item-header")[0].by_tag("a")[0].content.encode("UTF8")) #title
       
        film_info[number].append(e.by_tag("div.ratings-bar")[0].by_tag("div.inline-block")[0]
            .by_tag("strong")[0].content.encode("UTF8")) # rating
        
        film_info[number].append(e.by_class("text-muted ")[0].by_class("genre")[0].content.strip(" ").strip("\n").encode("UTF8")) # genre
        
        actors = ""
        for a in e.by_tag("p")[2].by_tag("a"):
            if actors == "":
                actors = a.content.encode("UTF8")
            else:
                actors = actors + ', ' + a.content.encode("UTF8")
        film_info[number].append(actors) #acteurs
        
        film_info[number].append(e.by_class("text-muted ")[0].by_class("runtime")[0].content.split(" ")[0].encode("UTF8")) #runtime

        
        number = number +1;
    return film_info





    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED TV-SERIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

   


def save_csv(f, tvseries):
    '''
    Output a CSV file containing highest rated TV-series.
    '''
    writer = csv.writer(f)
    writer.writerow(['Title', 'Rating', 'Genre', 'Actors', 'Runtime'])
    for film in tvseries:
        writer.writerow(film)

    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE TV-SERIE S TO DISK

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