import flet as ft

def main(page: ft.Page):
    # Bloomberg Termainal Style Colors
    page.bgcolor = "#0A0A0F"  # Deep dark background
    page.title = "Money Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Text styles
    page.fonts = {
        "SF Pro Display": "https://raw.githubusercontent.com/google/fonts/main/ofl/sfprodisplay/SFProDisplay-Bold.ttf"
    }
    
    # App Bar
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.MENU, color="#FF9500"),
        leading_width=40,
        title=ft.Text("MONEY TRACKER", size=16, weight=ft.FontWeight.BOLD, color="#E8E8EC"),
        center_title=True,
        bgcolor="#16161D",
        actions=[
            ft.IconButton(ft.icons.SEARCH, icon_color="#FF9500"),
            ft.IconButton(ft.icons.NOTIFICATIONS, icon_color="#FF9500"),
        ],
    )

    # Balance Card
    balance_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("TOTAL ASSETS", color="#8888A0", size=12, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text("● LIVE", color="#00FF88", size=10, weight=ft.FontWeight.BOLD),
                    padding=ft.padding.only(left=200) # Spacer hack for now
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text("¥ 25,800.00", size=36, weight=ft.FontWeight.W_900, color="#FF9500"),
            ft.Row([
                ft.Text("▲ +¥32,000", color="#00FF88", weight=ft.FontWeight.BOLD),
                ft.Text("▼ -¥6,200", color="#FF3B5C", weight=ft.FontWeight.BOLD),
            ], spacing=20)
        ]),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#16161D", "#1A1A24"],
        ),
        border=ft.border.all(1, "#30FF9500"),
        border_radius=16,
        padding=20,
        margin=10,
    )

    page.add(
        balance_card,
        ft.Text("Tap + to add transaction", color="#5A5A70", size=12, text_align=ft.TextAlign.CENTER)
    )

    # Floating Action Button
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        bgcolor="#FF9500",
        content=ft.Icon(ft.icons.ADD, color="white"),
    )

ft.app(target=main)
