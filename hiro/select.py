import argparse
import curses
import datetime
import os
import subprocess
import sys
import time

def get_cal_output(timestamp):
    # Format the timestamp to 'YY-MM-DD' and execute cal command
    date_str = timestamp.strftime('%Y-%m-%d')
    command = f'cal -3 --color=always {date_str}'
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode('utf-8')
    
    # Replace ANSI escape sequences with custom placeholders
    output = output.replace(" \x1b[7m", "⟦").replace("\x1b[27m ", "⟧")
    
    return output

def display_timestamp(screen, timestamp):
    screen.erase()

    # Get calendars using cal utility
    cal_output = get_cal_output(timestamp)

    # Calculate width of calendar for centering
    cal_width = max(len(line) for line in cal_output.splitlines())
    screen_width = curses.COLS  # Get the screen width
    start_col = (screen_width - cal_width) // 2  # Calculate the start column for centering

    # Center the title relative to the calendar's width
    title = "Timestamp Editor (Vim-like Controls)"
    title_start_col = start_col + (cal_width - len(title)) // 2
    screen.addstr(2, title_start_col, title)

    # Display controls
    control_start_row = 4
    screen.addstr(control_start_row, start_col, "Press Ctrl-u/Ctrl-d to increase/decrease day")
    screen.addstr(control_start_row + 1, start_col, "Press 'h'/'l' to decrease/increase hour")
    screen.addstr(control_start_row + 2, start_col, "Press 'j'/'k' to increase/decrease minute")
    screen.addstr(control_start_row + 3, start_col, "Press Ctrl-b/Ctrl-f to decrease/increase month")
    screen.addstr(control_start_row + 4, start_col, "Press 'Enter' to select the current timestamp and exit")
    screen.addstr(control_start_row + 5, start_col, "Press 'q' to abort")

    # Center the current timestamp label and value relative to the calendar's width
    timestamp_label = "Current Timestamp:"
    timestamp_value = timestamp.strftime('%Y-%m-%d %H:%M:%S%z')

    timestamp_label_start_col = start_col + (cal_width - len(timestamp_label)) // 2
    timestamp_value_start_col = start_col + (cal_width - len(timestamp_value)) // 2

    screen.addstr(control_start_row + 7, timestamp_label_start_col, timestamp_label)
    screen.addstr(control_start_row + 8, timestamp_value_start_col, timestamp_value)

    # Display the calendar centered horizontally below the controls
    y = control_start_row + 10
    for line in cal_output.splitlines():
        screen.addstr(y, start_col, line)
        y += 1

    screen.refresh()

def cmain(screen, initial_timestamp):
    curses.curs_set(0)  # hide cursor
    timestamp = initial_timestamp

    while True:
        display_timestamp(screen, timestamp)

        key = screen.getch()

        if key == 21:  # Ctrl-u
            timestamp -= datetime.timedelta(days=1)
        elif key == 4:  # Ctrl-d
            timestamp += datetime.timedelta(days=1)
        elif key == 2:  # Ctrl-b
            if timestamp.month == 1:
                timestamp = timestamp.replace(year=timestamp.year-1, month=12)
            else:
                timestamp = timestamp.replace(month=timestamp.month-1)
        elif key == 6:  # Ctrl-f
            if timestamp.month == 12:
                timestamp = timestamp.replace(year=timestamp.year+1, month=1)
            else:
                timestamp = timestamp.replace(month=timestamp.month+1)
        elif key == ord('h'):
            timestamp -= datetime.timedelta(hours=1)
        elif key == ord('l'):
            timestamp += datetime.timedelta(hours=1)
        elif key == ord('j'):
            timestamp += datetime.timedelta(minutes=1)
        elif key == ord('k'):
            timestamp -= datetime.timedelta(minutes=1)
        elif key == 10:  # Enter key
            return timestamp.strftime('%Y-%m-%d %H:%M:%S%z')
        elif key == ord('q'):
            return None

def main():
    parser = argparse.ArgumentParser(description="Timestamp Editor with Vim-like Controls.")
    parser.add_argument("timestamp",
                        nargs="?",
                        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S%z'),
                        default=datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds=-time.timezone))).strftime('%Y-%m-%d %H:%M:%S%z'),
                        help="Timestamp in format '2023-10-16 08:21:32+02:00'")
    args = parser.parse_args()

    # Save original stdout file descriptor and redirect stdout to stderr
    original_stdout_fd = os.dup(1)
    os.dup2(2, 1)

    try:
        output = curses.wrapper(cmain, args.timestamp)
    finally:
        # Restore original stdout
        os.dup2(original_stdout_fd, 1)
        os.close(original_stdout_fd)

    if output is not None:
        print(output)

