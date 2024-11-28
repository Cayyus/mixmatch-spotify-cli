from tabulate import tabulate
import curses

class PlaylistTable:
    def __init__(self, stdscr, data):
        self.stdscr = stdscr
        self.data = data
        self.page_size = 10  
        self.current_page = 0
        self.num_pages = (len(data) + self.page_size - 1) // self.page_size
        self.headers = ["Track", "URL", "Artist", "Duration (min)"]
        self.max_widths = [100, 100, 43, 100]  # Define maximum widths for each column
        self.track_max_width = 26  # Adjust this as needed for the track column

    def truncate(self, text, width):
        """Truncate text to fit within a specified width."""
        return text if len(text) <= width else text[:width - 3] + "..."

    def format_page_data(self):
        """Format the current page of data as a table string with grid lines."""
        start_idx = self.current_page * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.data))
        page_data = [
            [
                self.truncate(str(row[0]), self.track_max_width),  # Truncate track name if needed
                str(row[1]),  # URL
                str(row[2]),  # Artist
                str(row[3])   # Duration
            ]
            for row in self.data[start_idx:end_idx]
        ]
        
        # Use tabulate to create a table string with grid lines
        table_str = tabulate(page_data, headers=self.headers, tablefmt="grid")
        return table_str.splitlines()  # Split into lines for curses display

    def display_page(self):
        """Display the current page of data with grid lines."""
        self.stdscr.clear()  # Clear the screen

        # Get formatted table data
        formatted_data = self.format_page_data()

        # Display each line in the formatted table
        for i, line in enumerate(formatted_data, start=1):
            self.stdscr.addstr(i, 0, line)

        # Display page navigation info further down
        bottom_line = len(formatted_data) + 3
        self.stdscr.addstr(bottom_line, 0, f"Page {self.current_page + 1}/{self.num_pages}")
        self.stdscr.addstr(bottom_line + 1, 0, "Press '>' for next page, '<' for previous, 'q' to quit")
        self.stdscr.refresh()

    def next_page(self):
        """Go to the next page if possible."""
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            self.display_page()

    def previous_page(self):
        """Go to the previous page if possible."""
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def run(self):
        """Main loop to handle user input and page navigation."""
        self.display_page()
        while True:
            key = self.stdscr.getch()

            if key == ord("q"):  # Press 'q' to quit
                break
            elif key == curses.KEY_RIGHT:  # Press '>' to go to the next page
                self.next_page()
            elif key == curses.KEY_LEFT:  # Press '<' to go to the previous page
                self.previous_page()
