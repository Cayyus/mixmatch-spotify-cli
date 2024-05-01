import curses
from tabulate import tabulate

from parsers.parse import api
from shared.er import hide_error

try:
    data = api.get_user_saved_tracks()
except Exception as e:
    hide_error(str(e))


class TrackTable:
    def __init__(self, stdscr, data):
        self.stdscr = stdscr
        self.data = data
        self.page_size = 10  
        self.current_page = 0
    

    def truncate_text(self, text, max_chars) -> str:
        if len(text) > max_chars:
            return text[:max_chars-3] + "..."
        return text

    def draw_table(self) -> None:
        start_idx = self.current_page * self.page_size
        end_idx = (self.current_page + 1) * self.page_size
        page_data = self.data['items'][start_idx:end_idx]
        table_data = []

        for item in page_data:
            track = item['track']

            album_name = self.truncate_text(track['album']['name'], 15) #max chars in name

            track_name = self.truncate_text(track['name'], 15)  
            track_link = track['external_urls']['spotify']
            artists_name = ', '.join(artist['name'] for artist in track['artists'])

            duration_ms = track['duration_ms']
            duration_min = duration_ms // 60000

            table_data.append([f"{track_name}\n{track_link}", f"{album_name}", artists_name, duration_min])

    
        headers = ["Track Name", "Album", "Artists", "Duration (min)"]

        try:
            # Get the size of the terminal
            max_rows, max_cols = self.stdscr.getmaxyx()

            # Check if there's enough space to display the table
            if max_rows >= len(table_data) + 4 and max_cols >= 50:
                table = tabulate(table_data, headers, tablefmt="grid")
                self.stdscr.addstr(2, 2, table)
                self.stdscr.addstr(max_rows - 1, 2, f"Page {self.current_page + 1} of {len(self.data['items']) // self.page_size + 1}")
            else:
                self.stdscr.addstr(2, 2, "Terminal too small. Resizing...")

                # Resize the terminal to fit the table
                curses.resize_term(len(table_data) + 5, 100) 

                # Redraw the table with the new size
                self.stdscr.clear()
                self.draw_table()
        except curses.error:
            pass


    def handle_input(self) -> None | bool:
        key = self.stdscr.getch()

        if key == curses.KEY_RIGHT and (self.current_page + 1) * self.page_size < len(self.data['items']):
            self.current_page += 1
        elif key == curses.KEY_LEFT and self.current_page > 0:
            self.current_page -= 1
        elif key == 27:  #27 - ESC
            return True

    def run(self) -> None:
        while True:
            self.stdscr.clear()
            self.draw_table()
            should_exit = self.handle_input()
            self.stdscr.refresh()

            if should_exit:
                break

def write(stdscr, data):
    curses.curs_set(0)
    stdscr.clear()

    table = TrackTable(stdscr, data)
    table.run()

def st_wrap():
    curses.wrapper(write, data)
