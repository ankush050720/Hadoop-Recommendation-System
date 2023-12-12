import imdb
import webbrowser
import os 
import sys
import time

constant_userid = input("Enter the userID: ")
itemids_array = []

directory = './ContentOut/'

for filename in os.listdir(directory):
    if filename.startswith("part-r-"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            user_found = False
            for line in file:
                userid, itemid = line.strip().split('\t')
                if userid == constant_userid:
                    itemids_array.append(itemid)
                    user_found = True
                    for _ in range(5):
                        next_line = next(file, None)
                        if next_line:
                            next_userid, next_itemid = next_line.strip().split('\t')
                            if next_userid == constant_userid:
                                itemids_array.append(next_itemid)
                            else:
                                break
                    break 
            if user_found:
                break

u_item_file = './Datasets/u.item'

movies_dict = {}

with open(u_item_file, 'r', encoding='latin-1') as file:
    for line in file:
        parts = line.strip().split('|')
        itemid = parts[0]
        movie_name = parts[1]
        movies_dict[itemid] = movie_name
movie_names_list = []

for itemid in itemids_array:
    if itemid in movies_dict:
        movie_names_list.append(movies_dict[itemid])

def get_movie_imdb_info(movie_name):
    ia = imdb.IMDb()
    # Search for the movie by name
    movies = ia.search_movie(movie_name)
    if not movies:
        print(f"No movie found with the name '{movie_name}'")
        return
    # Get the first result (you can choose a specific one if there are multiple results)
    movie = ia.get_movie(movies[0].getID())

    # Get the IMDb URL of the movie
    imdb_url = ia.get_imdbURL(movie)
    print(f"IMDb URL for '{movie_name}': {imdb_url}")

    # Get the poster URL
    poster_url = movie.data['cover url']
    print(f"Poster URL for '{movie_name}': {poster_url}")
    
    return imdb_url, poster_url


movies = movie_names_list

imdb_urls = []
poster_urls = []
for movie in movies:
    imdb_url, poster_url = get_movie_imdb_info(movie)
    imdb_urls.append(imdb_url)
    poster_urls.append(poster_url)

print('\nCreating your recommended movies list , just wait ...')
time.sleep(5)

# Create or modify the HTML file with the IMDb URLs and poster URLs
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recomended Movies</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}

        h1 {{
            text-align: center;
        }}

        .row {{
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }}

        .poster {{
            width: calc(20% - 10px); /* 20% width with 10px margin */
            margin-right: 10px; /* Adjusted margin between posters */
            margin-bottom: 10px;
            cursor: pointer;
        }}

        .poster:last-child {{
            margin-right: 0; /* Remove margin for the last poster in each row */
        }}

        .poster img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>

<h1>Recommended Movies</h1>

"""

# Split the posters into rows
num_images_per_row = 5
for i in range(0, len(imdb_urls), num_images_per_row):
    row_imdb_urls = imdb_urls[i:i + num_images_per_row]
    row_poster_urls = poster_urls[i:i + num_images_per_row]

    html_content += '<div class="row">\n'
    for imdb_url, poster_url in zip(row_imdb_urls, row_poster_urls):
        html_content += f'    <div class="poster" onclick="window.location.href=\'{imdb_url}\'">\n'
        html_content += f'        <img src="{poster_url}" alt="Movie Poster">\n'
        html_content += '    </div>\n'
    html_content += '</div>\n'

html_content += """</body>
</html>
"""

# Save the HTML content to a file
with open("movie_info.html", "w", encoding="utf-8") as html_file:
    html_file.write(html_content)

# Open the HTML file in the default web browser
webbrowser.open("movie_info.html")