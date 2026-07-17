"""Mobile Calculator - Entry point."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from apps.mobile.app import main
import flet as ft

if __name__ == '__main__':
    ft.app(target=main, view=ft.AppView.FLET_APP)
