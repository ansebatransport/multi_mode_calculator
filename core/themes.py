"""Theme management for the calculator app."""
from typing import Optional
import json, os

class ThemeManager:
    """Manages dark/light themes with color palettes."""
    
    def __init__(self, default_theme: str = "dark"):
        self._current_theme = default_theme
        self._custom_themes: dict[str, dict[str, str]] = {}
        self._persist_path = os.path.expanduser("~/.calc_theme.json")
        self._load()
    
    @property
    def current(self) -> str:
        return self._current_theme
    
    def toggle(self) -> str:
        self._current_theme = "light" if self._current_theme == "dark" else "dark"
        self._save()
        return self._current_theme
    
    def set_theme(self, theme: str) -> None:
        if theme not in ("dark", "light") and theme not in self._custom_themes:
            raise ValueError(f"Unknown theme: {theme}")
        self._current_theme = theme
        self._save()
    
    def get_color(self, key: str) -> str:
        colors = self._get_palette()
        return colors.get(key, "#ffffff")
    
    def get_palette(self) -> dict[str, str]:
        return self._get_palette()
    
    def register_custom_theme(self, name: str, palette: dict[str, str]) -> None:
        self._custom_themes[name] = palette
    
    def _get_palette(self) -> dict[str, str]:
        if self._current_theme in self._custom_themes:
            return self._custom_themes[self._current_theme]
        from utils.constants import DARK_THEME, LIGHT_THEME
        return DARK_THEME if self._current_theme == "dark" else LIGHT_THEME
    
    def _load(self) -> None:
        try:
            if os.path.exists(self._persist_path):
                with open(self._persist_path, 'r') as f:
                    data = json.load(f)
                self._current_theme = data.get("theme", "dark")
        except (json.JSONDecodeError, IOError):
            pass
    
    def _save(self) -> None:
        try:
            with open(self._persist_path, 'w') as f:
                json.dump({"theme": self._current_theme}, f)
        except IOError:
            pass
