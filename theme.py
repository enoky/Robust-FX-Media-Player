from __future__ import annotations

from PySide6 import QtGui

from models import Theme, THEMES
from utils import adjust_color


def build_palette(theme: Theme) -> QtGui.QPalette:
    window_color = QtGui.QColor(theme.window)
    base_color = QtGui.QColor(theme.base)
    text_color = QtGui.QColor(theme.text)
    highlight_color = QtGui.QColor(theme.highlight)
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, window_color)
    palette.setColor(QtGui.QPalette.ColorRole.WindowText, text_color)
    palette.setColor(QtGui.QPalette.ColorRole.Base, base_color)
    palette.setColor(QtGui.QPalette.ColorRole.AlternateBase, window_color.darker(110))
    palette.setColor(QtGui.QPalette.ColorRole.Text, text_color)
    palette.setColor(QtGui.QPalette.ColorRole.Button, window_color)
    palette.setColor(QtGui.QPalette.ColorRole.ButtonText, text_color)
    palette.setColor(QtGui.QPalette.ColorRole.Highlight, highlight_color)
    palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor("#ffffff"))
    return palette


def build_stylesheet(theme: Theme) -> str:
    border = adjust_color(theme.card, lighter=120)
    button = adjust_color(theme.card, lighter=112)
    button_hover = adjust_color(button, lighter=108)
    accent = theme.accent
    slider_track = adjust_color(theme.text, darker=220)
    slider_border = adjust_color(slider_track, darker=130)
    slider_handle_border = adjust_color(accent, darker=150)
    
    # Pre-calc colors
    base_lighter_102 = adjust_color(theme.base, lighter=102)
    base_lighter_105 = adjust_color(theme.base, lighter=105)
    base_lighter_110 = adjust_color(theme.base, lighter=110)
    text_lighter_110 = adjust_color(theme.text, lighter=110)
    
    parts = []
    
    parts.append(f"""
        QMainWindow {{
            background: {theme.window};
        }}
        QToolButton, QPushButton {{
            padding: 6px 10px;
            border-radius: 8px;
            background: {button};
            border: 1px solid {border};
        }}
        QToolButton:hover, QPushButton:hover {{
            background: {button_hover};
        }}
        QToolButton:checked {{
            background: {accent};
            color: #0b0b0b;
        }}
    """)
    
    parts.append(f"""
        QSlider::handle:horizontal {{
            width: 14px;
            height: 14px;
            margin: -4px 0;
            border-radius: 7px;
            background: {accent};
            border: 1px solid {slider_handle_border};
        }}
        QSlider::handle:vertical {{
            width: 16px;
            height: 16px;
            margin: 0 -5px;
            border-radius: 8px;
            background: {accent};
            border: 1px solid {slider_handle_border};
        }}
        QSlider::groove:horizontal {{
            height: 6px;
            background: {slider_track};
            border: 1px solid {slider_border};
            border-radius: 3px;
        }}
        QSlider::groove:vertical {{
            width: 6px;
            background: {slider_track};
            border: 1px solid {slider_border};
            border-radius: 3px;
        }}
        QSlider::sub-page:horizontal {{
            background: {accent};
            border-radius: 3px;
        }}
        QSlider::add-page:horizontal {{
            background: {slider_track};
            border-radius: 3px;
        }}
        QSlider::sub-page:vertical {{
            background: {slider_track};
            border-radius: 3px;
        }}
        QSlider::add-page:vertical {{
            background: {slider_track};
            border-radius: 3px;
        }}
    """)

    parts.append(f"""
        QGroupBox {{
            margin-top: 16px;
            padding: 12px;
            background: {theme.card};
            border: 1px solid {border};
            border-radius: 12px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 6px;
            margin-left: 8px;
            font-weight: 600;
        }}
        QComboBox {{
            padding: 4px 10px;
            border-radius: 8px;
            background: {theme.base};
            border: 1px solid {border};
        }}
        QComboBox::drop-down {{
            width: 22px;
            border-left: 1px solid {border};
        }}
        QComboBox QAbstractItemView {{
            background: {theme.base};
            color: {theme.text};
            border: 1px solid {border};
            selection-background-color: {theme.highlight};
            selection-color: #0b0b0b;
        }}
        QMenu {{
            background: {theme.base};
            color: {theme.text};
            border: 1px solid {border};
            padding: 4px;
            border-radius: 6px;
        }}
        QMenu::item {{
            padding: 6px 24px 6px 12px;
            border-radius: 4px;
            margin: 2px;
        }}
        QMenu::item:selected {{
            background: {theme.highlight};
            color: #0b0b0b;
        }}
        QMenu::separator {{
            height: 1px;
            background: {border};
            margin: 4px 8px;
        }}
    """)

    parts.append(f"""
        QListWidget {{
            padding: 8px;
            border-radius: 10px;
            border: 1px solid {border};
            background: {theme.base};
        }}
        QListWidget::item {{
            margin: 0px;
            padding: 0px;
            border: none;
        }}
        QListWidget::item:selected {{
            border: none;
        }}
        QListWidget::item:hover {{
            border: none;
        }}
        QLabel#track_title {{
            font-size: 18px;
            font-weight: 700;
            color: {theme.text};
        }}
        QLabel#track_artist {{
            font-size: 14px;
            font-weight: 600;
            color: {adjust_color(theme.text, lighter=112)};
        }}
        QLabel#track_album {{
            font-size: 13px;
            color: {adjust_color(theme.text, lighter=108)};
        }}
        QLabel#track_meta {{
            font-size: 12px;
            color: {adjust_color(theme.text, lighter=120)};
        }}
    """)

    parts.append(f"""
        QLabel#status_label {{
            color: {adjust_color(theme.text, lighter=120)};
        }}
        QFrame#header_frame {{
            border: 1px solid {border};
            border-radius: 14px;
            background: {theme.card};
            padding: 12px;
        }}
        QFrame#media_frame {{
            border: 1px solid {border};
            border-radius: 16px;
            background: {adjust_color(theme.base, lighter=106)};
        }}
        QLabel#playlist_header {{
            font-size: 14px;
            font-weight: 600;
            color: {theme.text};
        }}
        QSplitter::handle {{
            background: {adjust_color(theme.window, lighter=110)};
        }}
    """)

    # Library Specifics
    parts.append(f"""
        QLineEdit#search_bar {{
            background: {base_lighter_105};
            color: {theme.text};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 4px 12px;
            font-size: 13px;
        }}
        QLineEdit#search_bar:focus {{
            border: 1px solid {accent};
            background: {theme.base};
        }}
        QTableView {{
            background: {base_lighter_102};
            color: {theme.text};
            gridline-color: {border};
            selection-background-color: {adjust_color(accent, alpha=60)};
            selection-color: #ffffff;
            border: 1px solid {border};
            border-radius: 8px;
            outline: none;
        }}
        QTableView::item {{
            padding: 2px 6px;
            border: none;
        }}
        QTableView::item:selected {{
            background: {adjust_color(accent, alpha=60)};
            color: #ffffff;
            border-radius: 4px;
        }}
    """)

    parts.append(f"""
        QHeaderView::section {{
            background: {base_lighter_105};
            color: {theme.text};
            padding: 6px;
            border: none;
            border-bottom: 2px solid {border};
            border-right: 1px solid {adjust_color(theme.base, lighter=115)};
            font-weight: 700;
            font-size: 12px;
            text-transform: uppercase;
        }}
        QTreeWidget {{
            background: {base_lighter_102};
            color: {theme.text};
            border: 1px solid {border};
            border-radius: 8px;
            padding: 4px;
            outline: none;
        }}
        QTreeWidget::item {{
            padding: 8px; /* Taller items */
            border-radius: 6px;
            color: {text_lighter_110};
        }}
        QTreeWidget::item:hover {{
            background: {base_lighter_110};
            color: {theme.text};
        }}
        QTreeWidget::item:selected {{
            background: {adjust_color(accent, alpha=40)};
            color: {theme.text};
            border: 1px solid {adjust_color(accent, alpha=60)};
        }}
    """)

    parts.append(f"""
        QScrollBar:vertical {{
            background: {theme.base};
            width: 16px;
            margin: 0px;
            border-radius: 8px;
        }}
        QScrollBar::handle:vertical {{
            background: {adjust_color(theme.card, lighter=120)};
            min-height: 20px;
            border-radius: 8px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {accent};
        }}
        QLabel#track_count_label {{
            color: {adjust_color(theme.text, lighter=120)};
            font-weight: 600;
            font-size: 12px;
            padding: 4px 8px;
            background: {theme.card};
            border: 1px solid {border};
            border-radius: 6px;
        }}
        QFrame#library_toolbar {{
            background: transparent;
            border-bottom: 1px solid {border};
            margin-bottom: 4px;
        }}
    """)
    
    return "\n".join(parts)
