"""Desktop Calculator - Flet app for Windows/macOS/Linux."""
import flet as ft
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.engine import ExpressionEvaluator
from core.expression_parser import ShuntingYardParser

BG = "#1a1a1a"
CARD_BG = "#2d2d2d"
BTN_NUM = "#3b3b3b"
BTN_OP = "#323232"
BTN_FUNC = "#323232"
BTN_EQ = "#4cc2ff"
TXT = "#ffffff"
TXT_DIM = "#d4d4d4"

MODES = {
    "standard": ("Standard", ft.Icons.CALCULATE),
    "scientific": ("Scientific", ft.Icons.SCIENCE),
    "programmer": ("Programmer", ft.Icons.COMPUTER),
    "graph": ("Graph", ft.Icons.SHOW_CHART),
    "converter": ("Converter", ft.Icons.SWAP_HORIZ),
    "financial": ("Financial", ft.Icons.ACCOUNT_BALANCE),
}

COMPACT_WIDTH = 340


class DesktopCalculator:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = BG
        self.page.padding = 0
        self.page.spacing = 0
        self.page.theme_mode = ft.ThemeMode.DARK

        self.engine = ExpressionEvaluator()
        self.parser = ShuntingYardParser()
        self.expression = ""
        self.result = "0"
        self.new_number = True
        self.is_maximized = False
        self.current_mode = "standard"
        self._nav_open = False

        self._build_title_bar()
        self._build_nav_bar()
        self._build_standard_page()
        self._build_ui()
        self._bind_keyboard()

    def _build_title_bar(self):
        self.title_bar = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.CALCULATE, size=14, color=ft.Colors.CYAN_200),
                    ft.Text("Calculator", size=12, color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE)),
                ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    self._ctrl_btn(ft.Icons.REMOVE),
                    self._ctrl_btn(ft.Icons.CHECK_BOX_OUTLINE_BLANK),
                    self._ctrl_btn(ft.Icons.CLOSE, hover_color="#e81123"),
                ], spacing=0),
            ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
            height=32, bgcolor="#252525",
            padding=ft.Padding(left=8, right=0, top=0, bottom=0),
        )

    def _ctrl_btn(self, icon, hover_color="#3e3e3e"):
        return ft.Container(
            content=ft.Icon(icon, size=12, color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE)),
            width=46, height=32,
            alignment=ft.Alignment(x=0, y=0),
            on_hover=lambda e, hc=hover_color: self._ctrl_hover(e, hc),
        )

    def _ctrl_hover(self, e, color):
        e.control.bgcolor = color if e.data == "true" else None
        if e.control.page:
            e.control.update()

    def _build_nav_bar(self):
        self.mode_label = ft.Text("Standard", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE)
        self.nav_bar = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.MENU, size=20,
                                    color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE)),
                    width=40, height=40,
                    alignment=ft.Alignment(x=0, y=0),
                    on_click=lambda e: self._toggle_nav(),
                    border_radius=4,
                    on_hover=lambda e: self._icon_hover(e),
                ),
                self.mode_label,
            ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.Padding(left=4, right=8, top=4, bottom=4),
            bgcolor="#252525",
            border=ft.Border(bottom=ft.BorderSide(1, "#3a3a3a")),
        )

    def _icon_hover(self, e):
        e.control.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE) if e.data == "true" else None
        if e.control.page:
            e.control.update()

    def _toggle_nav(self):
        self._nav_open = not self._nav_open
        if self._nav_open:
            items = []
            for key, (name, icon) in MODES.items():
                is_active = key == self.current_mode
                item = ft.Container(
                    content=ft.Row([
                        ft.Icon(icon, size=18,
                                color=ft.Colors.CYAN_200 if is_active else ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
                        ft.Text(name, size=13,
                                color=ft.Colors.WHITE if is_active else ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
                                weight=ft.FontWeight.W_500 if is_active else ft.FontWeight.W_400),
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding(left=12, right=12, top=10, bottom=10),
                    border_radius=6,
                    on_click=lambda e, k=key: self._switch_mode(k),
                    data=key,
                )
                items.append(item)

            self.nav_overlay = ft.Container(
                content=ft.Column(items, spacing=2),
                bgcolor="#2d2d2d",
                border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left=0, bottom_right=8),
                padding=ft.Padding(left=4, right=4, top=4, bottom=8),
                width=220,
            )
            self.nav_bg = ft.Container(
                visible=True,
                bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
                on_click=lambda e: self._toggle_nav(),
            )
            self.page.overlay.append(self.nav_bg)
            self.page.overlay.append(self.nav_overlay)
        else:
            if self.nav_bg in self.page.overlay:
                self.page.overlay.remove(self.nav_bg)
            if self.nav_overlay in self.page.overlay:
                self.page.overlay.remove(self.nav_overlay)
        self.page.update()

    def _switch_mode(self, key):
        self.current_mode = key
        self.mode_label.value = MODES[key][0]
        self._toggle_nav()

    def _build_standard_page(self):
        self.expr_text = ft.Text("", size=13, color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE),
                                  text_align=ft.TextAlign.RIGHT, max_lines=1,
                                  overflow=ft.TextOverflow.ELLIPSIS)
        self.result_text = ft.Text("0", size=42, weight=ft.FontWeight.W_300, color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.RIGHT, max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS)

        def btn(text, bg=BTN_NUM, color=TXT, fs=15):
            return ft.Container(
                content=ft.Text(text, size=fs, color=color,
                                weight=ft.FontWeight.W_500 if text.isdigit() else ft.FontWeight.W_400),
                height=52, bgcolor=bg, border_radius=6,
                alignment=ft.Alignment(x=0, y=0),
                padding=ft.Padding(left=16, right=0, top=0, bottom=0),
                expand=True,
                on_click=lambda e, t=text: self._on_button(t),
                on_hover=lambda e, obg=bg: self._btn_hover(e, obg),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=2,
                                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 1)),
            )

        def _bh(e, obg):
            if e.data == "true":
                e.control.bgcolor = "#4a4a4a" if obg == BTN_NUM else (
                    "#5cd0ff" if obg == BTN_EQ else "#404040")
            else:
                e.control.bgcolor = obg
            if e.control.page:
                e.control.update()

        self._btn_hover = _bh

        def row(*controls):
            return ft.Row(controls, spacing=3, alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                          vertical_alignment=ft.CrossAxisAlignment.CENTER)

        buttons = ft.Column([
            row(btn("%", BTN_FUNC, TXT_DIM, 14), btn("CE", BTN_FUNC, TXT_DIM, 14),
                btn("C", BTN_FUNC, TXT_DIM, 14), btn("⌫", BTN_FUNC, TXT_DIM, 16)),
            row(btn("1/x", BTN_FUNC, TXT_DIM, 14), btn("x²", BTN_FUNC, TXT_DIM, 14),
                btn("√", BTN_FUNC, TXT_DIM, 14), btn("÷", BTN_OP, TXT, 18)),
            row(btn("7", fs=18), btn("8", fs=18), btn("9", fs=18), btn("×", BTN_OP, TXT, 18)),
            row(btn("4", fs=18), btn("5", fs=18), btn("6", fs=18), btn("−", BTN_OP, TXT, 18)),
            row(btn("1", fs=18), btn("2", fs=18), btn("3", fs=18), btn("+", BTN_OP, TXT, 18)),
            row(btn("±", BTN_FUNC, TXT_DIM, 16), btn("0", fs=18), btn(".", fs=18),
                btn("=", BTN_EQ, "#1a1a1a", 20)),
        ], spacing=3)

        self.page_content = ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Container(content=self.expr_text,
                                 padding=ft.Padding(left=0, right=16, top=14, bottom=0)),
                    ft.Container(content=self.result_text,
                                 padding=ft.Padding(left=0, right=16, top=0, bottom=10)),
                ], spacing=0, alignment=ft.MainAxisAlignment.END),
                height=115, bgcolor=CARD_BG,
            ),
            ft.Container(content=buttons,
                         padding=ft.Padding(left=8, right=8, top=4, bottom=8)),
        ], spacing=0)

    def _build_ui(self):
        calc_card = ft.Container(
            content=ft.Column([self.nav_bar, self.page_content], spacing=0),
            width=COMPACT_WIDTH,
            bgcolor=CARD_BG,
            border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left=8, bottom_right=8),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=20,
                                color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
                                offset=ft.Offset(0, 4)),
        )

        centered = ft.Row(
            [ft.Container(expand=True), calc_card, ft.Container(expand=True)],
            spacing=0, vertical_alignment=ft.CrossAxisAlignment.START,
        )

        self.page.add(
            ft.Column([
                self.title_bar,
                ft.Container(content=centered, expand=True, bgcolor=BG),
            ], spacing=0, expand=True)
        )

    def _bind_keyboard(self):
        self.page.on_keyboard_event = self._on_keyboard

    def _on_keyboard(self, e: ft.KeyboardEvent):
        key = e.key
        key_map = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '.': '.', '+': '+', '-': '-', '*': '*', '/': '/',
            'Enter': '=', 'Backspace': '⌫', 'Escape': 'C', 'Delete': 'CE',
        }
        if key in key_map:
            self._on_button(key_map[key])
            self.page.update()

    def _on_button(self, text):
        if text == 'C':
            self.expression = ""
            self.result = "0"
            self.new_number = True
        elif text == 'CE':
            self.result = "0"
            self.new_number = True
        elif text == '⌫':
            self.result = self.result[:-1] if len(self.result) > 1 else "0"
        elif text == '=':
            if self.expression:
                try:
                    full = self.expression + self.result
                    tokens = self.parser.parse(full)
                    val = self.engine.evaluate(tokens)
                    self.result = str(int(val)) if isinstance(val, float) and val == int(val) else str(val)
                    self.expression = ""
                    self.new_number = True
                except Exception:
                    self.result = "Error"
                    self.new_number = True
        elif text in ('+', '-', '*', '/'):
            self.expression += self.result + text
            self.result = "0"
            self.new_number = True
        elif text == '±':
            if self.result not in ('0', 'Error'):
                self.result = self.result[1:] if self.result.startswith('-') else '-' + self.result
        elif text == '√':
            self.result = str(float(self.result) ** 0.5)
            self.new_number = True
        elif text == 'x²':
            self.result = str(float(self.result) ** 2)
            self.new_number = True
        elif text == '1/x':
            self.result = str(1 / float(self.result)) if float(self.result) != 0 else "Error"
            self.new_number = True
        elif text == '%':
            if self.expression:
                try:
                    base = float(self.parser.parse(self.expression.rstrip('+-*/'))[0])
                    self.result = str(base * float(self.result) / 100)
                except Exception:
                    self.result = str(float(self.result) / 100)
            else:
                self.result = str(float(self.result) / 100)
            self.new_number = True
        else:
            if self.new_number or self.result in ('0', 'Error'):
                self.result = text
                self.new_number = False
            else:
                self.result += text
        self.expr_text.value = self.expression
        self.result_text.value = self.result
        if self.page:
            self.page.update()


def main(page: ft.Page):
    DesktopCalculator(page)


if __name__ == '__main__':
    ft.app(target=main, view=ft.AppView.FLET_APP, width=420, height=700)
