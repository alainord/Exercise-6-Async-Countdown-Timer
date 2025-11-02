import asyncio
import flet as ft

class TimerState:
    def __init__(self, name: str, start_seconds: int = 60):
        self.name = name
        self.start_seconds = start_seconds
        self.remaining = start_seconds
        self.running = False
        self._task = None  # Handle for the background task

        # UI controls (filled later)
        self.input_seconds: ft.TextField | None = None
        self.remaining_text: ft.Text | None = None
        self.progress: ft.ProgressRing | None = None
        self.start_btn: ft.ElevatedButton | None = None
        self.pause_btn: ft.ElevatedButton | None = None
        self.reset_btn: ft.ElevatedButton | None = None

    def ratio(self) -> float:
        if self.start_seconds <= 0:
            return 0.0
        return max(0.0, min(1.0, (self.start_seconds - max(0, self.remaining)) / self.start_seconds))

    def formatted_remaining(self) -> str:
        s = max(0, int(self.remaining))
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"

async def main(page: ft.Page):
    page.title = "Multi Countdown Timer • Flet (async)"
    page.theme_mode = "light"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # --- AppBar + Navigation Drawer ---
    def open_drawer(e):
        page.drawer.open = True
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Multi Countdown Timer"),
        leading=ft.IconButton(ft.Icons.MENU, on_click=open_drawer),
        center_title=False,
        bgcolor=ft.Colors.PRIMARY_CONTAINER
    )

    # Create timers
    timers: list[TimerState] = [
        TimerState("Timer 1", 90),
        TimerState("Timer 2", 150),
        TimerState("Timer 3", 300),
    ]

    # Content container for the selected timer view
    content = ft.Container(expand=True, padding=20)

    # Helper: build a view for a single timer
    def build_timer_view(t: TimerState) -> ft.Column:
        if t.input_seconds is None:
            t.input_seconds = ft.TextField(
                label="Start value (seconds)",
                value=str(t.start_seconds),
                width=220,
                keyboard_type=ft.KeyboardType.NUMBER,
                on_change=lambda e, tt=t: on_change_start_value(tt)
            )
            t.remaining_text = ft.Text(
                t.formatted_remaining(),
                size=48,
                weight=ft.FontWeight.W_600
            )
            t.progress = ft.ProgressRing(value=t.ratio(), width=80, height=80)
            t.start_btn = ft.ElevatedButton(
                "Start",
                icon=ft.Icons.PLAY_ARROW,
                on_click=lambda e, tt=t: on_start(tt)
            )
            t.pause_btn = ft.ElevatedButton(
                "Pause",
                icon=ft.Icons.PAUSE,
                on_click=lambda e, tt=t: on_pause(tt)
            )
            t.reset_btn = ft.OutlinedButton(
                "Reset",
                icon=ft.Icons.RESTART_ALT,
                on_click=lambda e, tt=t: on_reset(tt)
            )

        return ft.Column(
            controls=[
                ft.Text(t.name, size=24, weight=ft.FontWeight.BOLD),
                ft.Row([t.input_seconds], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [t.start_btn, t.pause_btn, t.reset_btn],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                ft.Row(
                    [
                        t.remaining_text,
                        ft.Container(width=16),
                        t.progress
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        )

    # --- Timer logic ---
    def on_change_start_value(t: TimerState):
        try:
            val = int(t.input_seconds.value.strip() or "0")
            val = max(0, val)
            t.start_seconds = val
            if not t.running:
                t.remaining = val
            update_timer_ui(t)
        except ValueError:
            pass
        page.update()

    def update_timer_ui(t: TimerState):
        if t.remaining_text:
            t.remaining_text.value = t.formatted_remaining()
        if t.progress:
            t.progress.value = t.ratio()

    async def tick(t: TimerState):
        while t.running and t.remaining > 0:
            await asyncio.sleep(1)
            if not t.running:
                break
            t.remaining -= 1
            update_timer_ui(t)
            page.update()
        if t.remaining <= 0:
            t.running = False
            update_timer_ui(t)
            t.running = False

    def on_start(t: TimerState):
        if t.remaining <= 0:
            t.remaining = t.start_seconds
        if not t.running:
            t.running = True
            # ¡IMPORTANTE! pasar la función y el arg por separado
            t._task = page.run_task(tick, t)
            update_timer_ui(t)


    def on_pause(t: TimerState):
        t.running = False
        update_timer_ui(t)
        page.update()

    def on_reset(t: TimerState):
        t.running = False
        t.remaining = t.start_seconds
        update_timer_ui(t)
        page.update()

    # --- Drawer destinations ---
    def set_view(index: int):
        content.content = build_timer_view(timers[index])
        page.drawer.selected_index = index
        page.drawer.open = False
        page.update()

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(icon=ft.Icons.TIMER, label="Timer 1"),
            ft.NavigationDrawerDestination(icon=ft.Icons.TIMER_OUTLINED, label="Timer 2"),
            ft.NavigationDrawerDestination(icon=ft.Icons.HOURGLASS_BOTTOM, label="Timer 3"),
        ],
        on_change=lambda e: set_view(e.control.selected_index),
    )

    set_view(0)

    # Footer / note
    page.add(
        content,
        ft.Divider(),
        ft.Text(
            "Tip: Open the menu (☰) to switch timers. Each timer runs independently in the background using page.run_task().",
            size=12,
            italic=True,
            color=ft.Colors.ON_SURFACE
        ),
    )

if __name__ == "__main__":
    ft.app(target=main)
