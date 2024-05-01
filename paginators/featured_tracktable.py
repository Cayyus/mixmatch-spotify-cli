import curses
from tabulate import tabulate

from parsers.parse import api
from shared.er import hide_error


def create_table(stdscr, headers, data, page_size=10):
    current_page = 0
    num_pages = (len(data) + page_size - 1) // page_size

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Press q to quit, > for next page, < for previous page")

        max_rows, max_cols = stdscr.getmaxyx()

        # Adjust page size based on available space
        max_table_rows = max_rows - 4  # Leave space for header, footer, and controls
        adjusted_page_size = min(page_size, max_table_rows)

        page_data = data[current_page * adjusted_page_size: (current_page + 1) * adjusted_page_size]
        table = tabulate(page_data, headers=headers)

        stdscr.addstr(2, 0, table)

        stdscr.refresh()

        c = stdscr.getch()

        if c == 27:
            break
        elif c == curses.KEY_RIGHT and current_page < num_pages - 1:
            current_page += 1
        elif c == curses.KEY_LEFT and current_page > 0:
            current_page -= 1


def parse_featured_tracks(stdscr, pl_arg):
    try:
        data = api.get_featured_tracks(pl_arg)
    except Exception as e:
        hide_error(str(e))
    tracks = data['tracks']['items']
    parsed_data = []

    for track in tracks:
        track_name = track['track']['name']
        duration_ms = track['track']['duration_ms']
        duration_min = duration_ms / 60000  
        artists = [artist['name'] for artist in track['track']['artists']]
        artists = ','.join(artists)
        spotify_link = track['track']['external_urls']['spotify']
        parsed_data.append([track_name, duration_min, artists, spotify_link])

    headers = ["Track Name", "Duration (min)", "Artists", 'Spotify Link']
    create_table(stdscr, headers, parsed_data)

def fs_wrap(pl_arg):
    curses.wrapper(parse_featured_tracks, pl_arg)

