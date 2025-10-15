"""
Color Configuration Document

This document defines the complete color scheme for the dashboard
"""

# Primary Color Configuration
PRIMARY_COLOR = "rgb(30, 45, 190)"  # Primary Color
SECONDARY_COLOR = "rgb(200, 48, 60)"  # Secondary Color

# Chart and Bar Chart Color Configuration
CHART_COLORS = [
    "rgb(30, 45, 190)",    # Primary Color
    "rgb(200, 48, 60)",    # Secondary Color
    "rgb(5, 189, 189)",    # Cyan
    "rgb(228, 148, 40)",   # Orange
    "rgb(150, 10, 85)",    # Magenta
    "rgb(84, 135, 60)"     # Green
]

# Frequency Analysis Gradient Color Configuration
FREQUENCY_GRADIENT_COLORS = [
    "rgb(190, 220, 250)",   # +4 (Removed overly light colors)
    "rgb(130, 175, 220)",  # +3
    "rgb(90, 135, 205)",   # +2
    "rgb(50, 100, 200)",   # +1
    "rgb(30, 45, 190)",    # ILO BLUE (Main Color)
    "rgb(21, 31, 133)",    # -1
    "rgb(35, 0, 80)"       # DARK BLUE
]

# Hexadecimal Format Colors
PRIMARY_COLOR_HEX = "#1E2DBE"
SECONDARY_COLOR_HEX = "#C8303C"

CHART_COLORS_HEX = [
    "#1E2DBE",  # Primary Color
    "#C8303C",  # Secondary Color
    "#05BDBD",  # Cyan
    "#E49428",  # Orange
    "#960A55",  # Magenta
    "#54873C"   # Green
]

# Color Usage Description
COLOR_USAGE = {
    "PRIMARY_COLOR": "Main brand color, used for titles, important buttons, and primary chart elements",
    "SECONDARY_COLOR": "Secondary accent color, used for auxiliary chart elements and highlighting important information",
    "CHART_COLORS[2]": "Cyan, used for the third category in data visualization",
    "CHART_COLORS[3]": "Orange, used for the fourth category in data visualization",
    "CHART_COLORS[4]": "Magenta, used for the fifth category in data visualization",
    "CHART_COLORS[5]": "Green, used for the sixth category in data visualization"
}

# Export Functions
def get_primary_color():
    """Returns the primary color"""
    return PRIMARY_COLOR

def get_secondary_color():
    """Returns the secondary color"""
    return SECONDARY_COLOR

def get_chart_colors():
    """Returns the list of chart colors"""
    return CHART_COLORS

def get_chart_colors_hex():
    """Returns the list of chart colors (hexadecimal format)"""
    return CHART_COLORS_HEX

def get_color_by_index(index):
    """Returns a color by its index"""
    if 0 <= index < len(CHART_COLORS):
        return CHART_COLORS[index]
    return PRIMARY_COLOR

def get_color_hex_by_index(index):
    """Returns a color by its index (hexadecimal format)"""
    if 0 <= index < len(CHART_COLORS_HEX):
        return CHART_COLORS_HEX[index]
    return PRIMARY_COLOR_HEX

def get_frequency_gradient_colors():
    """Returns the list of gradient colors for frequency analysis"""
    return FREQUENCY_GRADIENT_COLORS