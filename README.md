
# Flet Multi Countdown Timer (Async + Navigation Drawer)

An asynchronous multi-countdown timer built with [Flet](https://flet.dev), demonstrating `page.run_task()`,
independent timers, and navigation via **Navigation Drawer** (instead of Tabs).

## Features
- Three independent timers (Timer 1, Timer 2, Timer 3)
- Start value input (in seconds) per timer
- **Start**, **Pause**, and **Reset** buttons
- Remaining time display (`HH:MM:SS` or `MM:SS`)
- Progress ring showing completion from 0 → 1
- Timers continue running in the background while you switch between them (uses `page.run_task()`)
- Uses **Navigation Drawer** (AppBar menu) so you can quickly switch timers

## How to run

1. Install dependencies:
   ```bash
   pip install flet
   ```

2. Run the app (any of the following works):
   ```bash
   python main.py
   # or
   flet run main.py
   ```

3. In the app, use the **menu (☰)** in the AppBar to open the Navigation Drawer and switch between timers.

## Notes
- Editing the **Start value (seconds)** updates the initial value. If the timer is **paused**, the remaining time will align with the new start value; if it's **running**, the current countdown continues (so you can pause/reset to apply).
- Progress ring shows completion ratio from `0.0` (just started) to `1.0` (finished).

## Why Navigation Drawer instead of Tabs?
The assignment suggested using Tabs but asked to "try to use navigation drawer instead of tabs". This project implements a Navigation Drawer to switch among the three timers while keeping background tasks running independently, which showcases Flet's async patterns and page-level navigation.

## File list
- `main.py` — the Flet app source code.
- `README.md` — this instructions file.
