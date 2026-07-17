"""Mobile Calculator - Flet app for Android/iOS."""
import flet as ft
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.engine import ExpressionEvaluator
from core.expression_parser import ShuntingYardParser

BG = "#1a1a2e"
BG_CARD = "#16213e"
BTN_NUM = "#1a1a2e"
BTN_OP = "#e94560"
BTN_FUNC = "#16213e"
BTN_EQ = "#2ed573"
TXT = "#ffffff"
TXT_DIM = "#a0a0a0"

MODES = [
    ("Standard", ft.Icons.CALCULATE),
    ("Scientific", ft.Icons.SCIENCE),
    ("Programmer", ft.Icons.COMPUTER),
    ("Graph", ft.Icons.SHOW_CHART),
    ("Converter", ft.Icons.SWAP_HORIZ),
    ("Financial", ft.Icons.ACCOUNT_BALANCE),
]


class MobileCalculator:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = BG
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.DARK

        self.engine = ExpressionEvaluator()
        self.parser = ShuntingYardParser()
        self.expression = ""
        self.result = "0"
        self.new_number = True

        self._mode_index = 0
        self._build_display()
        self._build_buttons()
        self._build_bottom_nav()
        self._build_ui()

    def _build_display(self):
        self.expr_text = ft.Text("", size=14, color=TXT_DIM,
                                  text_align=ft.TextAlign.RIGHT, max_lines=1,
                                  overflow=ft.TextOverflow.ELLIPSIS)
        self.result_text = ft.Text("0", size=48, weight=ft.FontWeight.W_300,
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.RIGHT, max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS)

    def _make_btn(self, text, bg=BTN_NUM, color=TXT, font_size=18, height=56, on_click=None):
        return ft.Container(
            content=ft.Text(text, size=font_size, color=color,
                            weight=ft.FontWeight.W_500 if text.isdigit() else ft.FontWeight.W_400),
            height=height,
            bgcolor=bg,
            border_radius=12,
            alignment=ft.Alignment(x=0, y=0),
            padding=ft.Padding(left=16, right=0, top=0, bottom=0),
            expand=True,
            on_click=on_click,
            on_hover=lambda e: self._hover(e, bg),
        )

    def _hover(self, e, orig):
        if e.data == "true":
            e.control.bgcolor = "#252545" if orig == BTN_NUM else (
                "#ff5a75" if orig == BTN_OP else "#35d983" if orig == BTN_EQ else "#1e2d4e")
        else:
            e.control.bgcolor = orig
        if e.control.page:
            e.control.update()

    def _row(self, *btns):
        return ft.Row(btns, spacing=6, alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                      vertical_alignment=ft.CrossAxisAlignment.CENTER)

    def _build_buttons(self):
        btn = self._make_btn
        self.buttons = ft.Column([
            self._row(
                btn("%", BTN_FUNC, TXT_DIM, 14, 52, lambda e: self._action("percent")),
                btn("CE", BTN_FUNC, TXT_DIM, 14, 52, lambda e: self._action("ce")),
                btn("C", BTN_FUNC, TXT_DIM, 14, 52, lambda e: self._action("clear")),
                btn("⌫", BTN_FUNC, TXT_DIM, 18, 52, lambda e: self._action("backspace"))),
            self._row(
                btn("1/x", BTN_FUNC, TXT_DIM, 14, 52, lambda e: self._action("reciprocal")),
                btn("x²", BTN_FUNC, TXT_DIM, 14, 52, lambda e: self._action("square")),
                btn("√", BTN_FUNC, TXT_DIM, 14, 52, lambda e: self._action("sqrt")),
                btn("÷", BTN_OP, TXT, 20, 52, lambda e: self._op("/"))),
            self._row(
                btn("7", on_click=lambda e: self._digit("7")),
                btn("8", on_click=lambda e: self._digit("8")),
                btn("9", on_click=lambda e: self._digit("9")),
                btn("×", BTN_OP, TXT, 20, 52, lambda e: self._op("*"))),
            self._row(
                btn("4", on_click=lambda e: self._digit("4")),
                btn("5", on_click=lambda e: self._digit("5")),
                btn("6", on_click=lambda e: self._digit("6")),
                btn("−", BTN_OP, TXT, 20, 52, lambda e: self._op("-"))),
            self._row(
                btn("1", on_click=lambda e: self._digit("1")),
                btn("2", on_click=lambda e: self._digit("2")),
                btn("3", on_click=lambda e: self._digit("3")),
                btn("+", BTN_OP, TXT, 20, 52, lambda e: self._op("+"))),
            self._row(
                btn("±", BTN_FUNC, TXT_DIM, 16, 52, lambda e: self._action("negate")),
                btn("0", on_click=lambda e: self._digit("0")),
                btn(".", on_click=lambda e: self._digit(".")),
                btn("=", BTN_EQ, "#000000", 22, 52, lambda e: self._action("calculate"))),
        ], spacing=6)

    def _build_bottom_nav(self):
        self.nav_items = []
        for i, (name, icon) in enumerate(MODES):
            is_active = i == self._mode_index
            item = ft.Container(
                content=ft.Column([
                    ft.Icon(icon, size=20,
                            color=ft.Colors.CYAN_200 if is_active else TXT_DIM),
                    ft.Text(name.split()[0], size=9,
                            color=ft.Colors.CYAN_200 if is_active else TXT_DIM,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400),
                ], spacing=2, alignment=ft.MainAxisAlignment.CENTER,
                   horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.Padding(left=4, right=4, top=6, bottom=6),
                on_click=lambda e, idx=i: self._switch_mode(idx),
                expand=True,
            )
            self.nav_items.append(item)

        self.bottom_nav = ft.Container(
            content=ft.Row(self.nav_items, spacing=0, alignment=ft.MainAxisAlignment.SPACE_AROUND),
            bgcolor="#0a1628",
            padding=ft.Padding(left=0, right=0, top=4, bottom=8),
        )

    def _switch_mode(self, index):
        self._mode_index = index
        for i, item in enumerate(self.nav_items):
            is_active = i == index
            for ctrl in item.content.controls:
                if isinstance(ctrl, ft.Icon):
                    ctrl.color = ft.Colors.CYAN_200 if is_active else TXT_DIM
                elif isinstance(ctrl, ft.Text):
                    ctrl.color = ft.Colors.CYAN_200 if is_active else TXT_DIM
                    ctrl.weight = ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400
        self.page.update()

    def _build_ui(self):
        display = ft.Container(
            content=ft.Column([
                ft.Container(content=self.expr_text,
                             padding=ft.Padding(left=0, right=16, top=20, bottom=0)),
                ft.Container(content=self.result_text,
                             padding=ft.Padding(left=0, right=16, top=0, bottom=12)),
            ], spacing=0, alignment=ft.MainAxisAlignment.END),
            bgcolor=BG_CARD,
            border_radius=ft.BorderRadius(top_left=16, top_right=16, bottom_left=0, bottom_right=0),
            height=140,
        )

        buttons_area = ft.Container(
            content=self.buttons,
            padding=ft.Padding(left=10, right=10, top=8, bottom=8),
        )

        self.page.add(
            ft.Column([
                display,
                ft.Container(content=buttons_area, expand=True),
                self.bottom_nav,
            ], spacing=0, expand=True)
        )

    def _digit(self, d):
        if self.new_number:
            self.result = d
            self.new_number = False
        elif self.result in ('0', 'Error'):
            self.result = d
        else:
            self.result += d
        self._update()

    def _op(self, op):
        self.expression += self.result + op
        self.result = "0"
        self.new_number = True
        self._update()

    def _action(self, action):
        if action == 'clear':
            self.expression = ""
            self.result = "0"
            self.new_number = True
        elif action == 'ce':
            self.result = "0"
            self.new_number = True
        elif action == 'backspace':
            self.result = self.result[:-1] if len(self.result) > 1 else "0"
        elif action == 'negate':
            if self.result not in ('0', 'Error'):
                self.result = self.result[1:] if self.result.startswith('-') else '-' + self.result
        elif action == 'square':
            self.result = str(float(self.result) ** 2)
            self.new_number = True
        elif action == 'sqrt':
            self.result = str(float(self.result) ** 0.5)
            self.new_number = True
        elif action == 'reciprocal':
            self.result = str(1 / float(self.result)) if float(self.result) != 0 else "Error"
            self.new_number = True
        elif action == 'percent':
            if self.expression:
                base = float(self.parser.parse(self.expression.rstrip('+-*/'))[0])
                self.result = str(base * float(self.result) / 100)
            else:
                self.result = str(float(self.result) / 100)
            self.new_number = True
        elif action == 'calculate':
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
        self._update()

    def _update(self):
        self.expr_text.value = self.expression
        self.result_text.value = self.result
        self.page.update()


def main(page: ft.Page):
    MobileCalculator(page)


if __name__ == '__main__':
    ft.app(target=main, view=ft.AppView.FLET_APP)
