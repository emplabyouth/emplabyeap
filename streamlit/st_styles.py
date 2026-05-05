import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional
import pandas as pd

class StreamlitStyleManager:
    """Streamlit Style Manager - Simplified Version"""
    
    def __init__(self):
        """Initialize style manager"""
        self.theme_colors = {
            'primary': '#1E2DBE',
            'secondary': '#FA3C4B', 
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#05D2D2',
            'light': '#7f7f7f',
            'dark': '#bcbd22'
        }
        
        self.chart_colors = [
            '#1E2DBE', '#FA3C4B', '#05D2D2', '#FFCD2D', '#960A55', '#8CE164', 
            '#34495E', '#F1C40F', '#E67E22', '#95A5A6'
        ]
        
        self.global_chart_config = {
            'layout': {
                'font': {
                    'family': "'Noto Sans SC', 'Microsoft YaHei', sans-serif",
                    'size': 12,
                    'color': '#333333'
                },
                'title': {
                    'font': {
                        'family': "'Noto Sans SC', 'Microsoft YaHei', sans-serif",
                        'size': 16,
                        'color': '#1f1f1f'
                    },
                    'x': 0.5,  # Center title
                    'xanchor': 'center',  # Center title anchor
                    'pad': {'b': 10}
                },
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'margin': dict(l=40, r=40, t=70, b=40)
            }
        }
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get theme colors"""
        return self.theme_colors
    
    def get_chart_colors(self) -> List[str]:
        """Get chart colors"""
        return self.chart_colors
    
    def get_global_chart_config(self, chart_type: str = None) -> dict:
        """Get global chart configuration"""
        if chart_type and chart_type in self.global_chart_config:
            return self.global_chart_config[chart_type]
        return self.global_chart_config
    
    def apply_custom_css(self):
        """Apply custom CSS styles - Simplified Version"""
        st.markdown(f"""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&family=Noto+Sans:wght@400;700&display=swap');
        
        /* Global font settings */
        .stApp {{
            font-family: 'Noto Sans', 'Noto Sans SC', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}

        /* Body font utility classes and generic applications */
        .yeap-body-text, .yeap-body-text p, .yeap-body-text li, .yeap-body-text span {{
            font-family: 'Noto Sans', 'Noto Sans SC', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-size: 15px;
            line-height: 1.6;
            color: #333333;
        }}

        /* Default Markdown body font synchronization (consistent with yeap-body-text) */
        .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span, .markdown-text-container {{
            font-family: 'Noto Sans', 'Noto Sans SC', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-size: 15px;
            line-height: 1.6;
            color: #333333;
        }}

        /* Cancel bold style for body text */
        .yeap-body-text b, .yeap-body-text strong {{ font-weight: 400 !important; }}
        .stMarkdown b, .stMarkdown strong, .markdown-text-container b, .markdown-text-container strong {{ font-weight: 400 !important; }}

        /* Root variables */
        :root {{
            --primary-color: {self.theme_colors['primary']};
            --secondary-color: {self.theme_colors['secondary']};
            --success-color: {self.theme_colors['success']};
            --warning-color: {self.theme_colors['warning']};
            --info-color: {self.theme_colors['info']};
            --light-color: {self.theme_colors['light']};
            --dark-color: {self.theme_colors['dark']};
        }}
        
        /* Main container styles */
        .main .block-container {{
            padding-top: 0rem; /* Remove top padding to ensure flush top after page switch */
            padding-bottom: 2rem;
            max-width: 1200px;
        }}
        
        /* Title styles */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 600;
            color: #1f1f1f;
        }}
        
        /* Table styles */
        .dataframe {{
            font-size: 12px;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        
        .dataframe th {{
            background-color: #f8f9fa;
            font-weight: 600;
            padding: 8px 12px;
            border: 1px solid #dee2e6;
        }}
        
        .dataframe td {{
            padding: 8px 12px;
            border: 1px solid #dee2e6;
        }}
        
        /* Metric card styles */
        .metric-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid var(--primary-color);
        }}
        
        /* Chart container styles */
        .chart-container {{
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def create_metric_card(self, title: str, value: str, delta: str = None, 
                          delta_color: str = "normal") -> str:
        """Create metric card"""
        delta_html = ""
        if delta:
            color = self.theme_colors.get('success' if delta_color == 'normal' else delta_color, '#666')
            delta_html = f'<div style="color: {color}; font-size: 0.9rem; margin-top: 0.5rem;">{delta}</div>'
        
        return f"""
        <div class="metric-card">
            <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">{title}</div>
            <div style="font-size: 2rem; font-weight: 600; color: #1f1f1f;">{value}</div>
            {delta_html}
        </div>
        """
    
    def create_data_table(self, df: pd.DataFrame, title: str = None) -> str:
        """Create data table"""
        title_html = f'<h3 style="margin-bottom: 1rem;">{title}</h3>' if title else ""
        
        return f"""
        <div class="chart-container">
            {title_html}
            {df.to_html(classes='dataframe', escape=False, index=False)}
        </div>
        """
    
    def create_horizontal_bar_chart(self, df: pd.DataFrame, x_col: str, y_col: str, 
                                   title: str = None, color_col: str = None,
                                   max_label_length: int = 20) -> go.Figure:
        """Create horizontal bar chart"""
        # Handle label length
        if max_label_length and len(df) > 0:
            df = df.copy()
            df[y_col] = df[y_col].astype(str).apply(
                lambda x: x[:max_label_length] + '...' if len(x) > max_label_length else x
            )
        
        # Create chart
        if color_col and color_col in df.columns:
            fig = px.bar(df, x=x_col, y=y_col, color=color_col,
                        orientation='h', title=title,
                        color_discrete_sequence=self.chart_colors)
        else:
            fig = px.bar(df, x=x_col, y=y_col, orientation='h', title=title,
                        color_discrete_sequence=[self.chart_colors[0]])
        
        # Apply global configuration
        fig.update_layout(self.global_chart_config['layout'])
        
        return fig

    def create_plotly_theme(self) -> dict:
        """Provide theme structure compatible with visualization layer"""
        return {'layout': self.global_chart_config['layout']}

    def _wrap_title(self, title: str, max_chars: int = 120) -> str:
        """Wrap long titles to prevent overflow"""
        if not title:
            return ''
        parts = []
        line = ''
        for word in str(title).split():
            if len(line) + len(word) + 1 > max_chars:
                parts.append(line)
                line = word
            else:
                line = f"{line} {word}".strip()
        if line:
            parts.append(line)
        return '<br>'.join(parts)

    def _to_title_case(self, s: str) -> str:
        """Capitalize the first letter of label text (preserve short acronyms like ILO, UN)."""
        if s is None:
            return ''
        s = str(s)
        def _cap_word(w: str) -> str:
            # Preserve fully capitalized and short acronyms
            if w.isupper() and len(w) <= 5:
                return w
            # Process hyphenated words
            return '-'.join(sub.capitalize() if sub else '' for sub in w.split('-'))
        return ' '.join(_cap_word(part) for part in s.split())

    # Custom: Fixed-width vertical legend (simulated using annotations)
    def _wrap_legend_text(self, text: str, max_chars: int = 18) -> str:
        """Simple line wrap by character count, returns text with <br>"""
        words = str(text).split()
        lines = []
        current = ''
        for w in words:
            if len(current) + len(w) + (1 if current else 0) <= max_chars:
                current = f"{current} {w}".strip()
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        return '<br>'.join(lines)

    def add_fixed_width_vertical_legend(self, fig: go.Figure, labels: List[str], colors: List[str], *,
                                        x: float = 0.88, y: float = 1.0, max_chars: int = 18,
                                        font_size: int = 12, row_gap: float = 0.06, draw_box: bool = False) -> None:
        """
        Add custom vertical legend to the right of the chart:
        - Fixed text width, wraps automatically when exceeded
        - Completely abandon geometric shapes, use the text character (■) to render color blocks, ensuring 100% vertical alignment and preventing deformation stretching
        """
        wrapped_labels = [self._wrap_legend_text(lbl, max_chars=max_chars) for lbl in labels]
        total_lines = sum(wl.count('<br>') + 1 for wl in wrapped_labels)

        y_cursor = y
        x_text = x
        symbol_x = x_text - 0.025  # Place color block to the left of the text
        
        for idx, wrapped in enumerate(wrapped_labels):
            # 1. Text annotation
            fig.add_annotation(
                xref='paper', yref='paper',
                x=x_text, y=y_cursor,
                text=wrapped,
                showarrow=False,
                align='left',
                xanchor='left',
                yanchor='top',
                font=dict(size=font_size, color='#333'),
            )
            
            # 2. Color block annotation (🌟 Core fix: Directly use the ■ character as an annotation)
            # Because it is also text, it shares the same coordinate point (y_cursor) and anchor (top) with the text next to it
            # The rendering engine will place them on the same baseline, precisely aligning with the first line!
            fig.add_annotation(
                xref='paper', yref='paper',
                x=symbol_x, y=y_cursor,
                text='■',
                showarrow=False,
                align='left',
                xanchor='left',
                yanchor='top',
                font=dict(size=font_size + 2, color=colors[idx % len(colors)]), # Slightly increase the font size to make the block fuller
            )
            
            # 3. Move cursor down
            lines = wrapped.count('<br>') + 1
            y_cursor -= row_gap + (lines - 1) * (row_gap * 0.75)

        if draw_box:
            height_est = total_lines * row_gap * 0.85 + 0.04
            fig.add_shape(
                type="rect",
                xref="paper", yref="paper",
                x0=max(0.0, symbol_x - 0.02), y0=min(1.0, y + 0.02),
                x1=min(0.995, x_text + 0.18), y1=max(0.0, y - height_est),
                line=dict(color="rgba(0,0,0,0.2)", width=1),
                fillcolor="rgba(255,255,255,0.9)",
                layer="below"
            )

    def create_standardized_chart(self, data, chart_type: str, title: str, preserve_order: bool = False) -> go.Figure:
        """Standardized chart creation, unified style, supports pie/bar/horizontal_bar, uses gradients for regional charts"""
        # Support Series or dict
        if isinstance(data, pd.Series):
            series = data.dropna()
            data_dict = series.to_dict()
        elif isinstance(data, dict):
            data_dict = {str(k): int(v) if pd.notna(v) else 0 for k, v in data.items()}
        else:
            data_dict = {}
        
        # Sort (unless preserving original order is requested)
        if not preserve_order and chart_type in ['bar', 'horizontal_bar']:
            data_dict = dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))
        
        labels = [self._to_title_case(lbl) for lbl in list(data_dict.keys())]
        values = list(data_dict.values())
        
        # Check if it is a region-related, Partnership-type, or frequency analysis chart; use gradient colors
        is_region_chart = any(keyword in title.lower() for keyword in ['region', 'regions', 'across regions'])
        is_partnership_chart = any(keyword in title.lower() for keyword in ['partnership', 'advocacy'])
        is_frequency_chart = any(keyword in title.lower() for keyword in ['types of', 'outputs delivered', 'frequency', 'distribution'])
        
        if (is_region_chart or is_partnership_chart or is_frequency_chart) and chart_type == 'bar':
            # Use gradient color scheme
            gradient_colors_hex = [
                '#BEDCfa',  # rgb(190, 220, 250) - lightest
                '#82AFDC',  # rgb(130, 175, 220)
                '#5A87CD',  # rgb(90, 135, 205)
                '#3264C8',  # rgb(50, 100, 200)
                '#1E2DBE',  # rgb(30, 45, 190) - ILO BLUE (main color)
                '#151F85',  # rgb(21, 31, 133)
                '#230050'   # rgb(35, 0, 80) - darkest
            ]
            
            # Allocate color based on value (larger value = darker color)
            if values:
                max_val = max(values)
                min_val = min(values)
                val_range = max_val - min_val if max_val != min_val else 1
                
                colors = []
                for val in values:
                    # Calculate color index (larger value = larger index, darker color)
                    normalized_val = (val - min_val) / val_range
                    color_idx = int(normalized_val * (len(gradient_colors_hex) - 1))
                    colors.append(gradient_colors_hex[color_idx])
            else:
                colors = [gradient_colors_hex[0]] * len(labels)
            
            fig = go.Figure(data=[go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=values,
                textposition='auto',
                hovertemplate='%{x}<br>%{y}<extra></extra>',
                width=0.6,  # Adjust column width to make it thinner
                showlegend=False  # Ensure the bar chart does not show a legend
            )])
            
            # Add gradient legend bar (optimize display effect)
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(
                    colorscale=[[i/(len(gradient_colors_hex)-1), color] for i, color in enumerate(gradient_colors_hex)],
                    showscale=True,
                    cmin=min_val if values else 0,
                    cmax=max_val if values else 1,
                    colorbar=dict(
                        title={'text': ''},  # Completely remove the title to avoid trace 0
                        x=1.02,
                        len=0.8,
                        thickness=15,
                        outlinewidth=0,
                        tickmode='linear',
                        tick0=min_val if values else 0,
                        dtick=(max_val - min_val) / 4 if values and max_val != min_val else 1,
                        showticklabels=False
                    )
                ),
                showlegend=False,
                name=' ',  # Prevent Plotly from falling back to trace 0
                hoverinfo='skip'
            ))
        else:
            # Use standard colors
            colors = self.get_chart_colors()
            
            if chart_type == 'pie':
                fig = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    marker_colors=colors[:len(labels)]
                )])
                # Disable built-in legend, use custom vertical fixed-width legend instead
                fig.update_layout(
                    margin=dict(l=20, r=180, t=60, b=20),
                    autosize=True,
                    showlegend=False
                )
                # Add custom legend (fixed width, word wrap, row by row display)
                self.add_fixed_width_vertical_legend(
                    fig,
                    labels=labels,
                    colors=colors[:len(labels)],
                    x=0.88,
                    y=1.0,
                    max_chars=14,
                    font_size=12,
                    row_gap=0.06,
                    draw_box=False
                )
            elif chart_type == 'horizontal_bar':
                fig = go.Figure(data=[go.Bar(
                    x=values,
                    y=labels,
                    orientation='h',
                    marker_color=colors[0],
                    text=values,
                    textposition='auto',
                    hovertemplate='%{y}<br>%{x}<extra></extra>'
                )])
                fig.update_layout(height=max(400, len(labels) * 30))
            else:  # bar
                fig = go.Figure(data=[go.Bar(
                    x=labels,
                    y=values,
                    marker_color=colors[0],
                    text=values,
                    textposition='auto',
                    hovertemplate='%{x}<br>%{y}<extra></extra>'
                )])
        
        # Apply uniform layout and title wrapping
        layout_config = self.get_global_chart_config('layout').copy()
        title_config = layout_config.get('title', {}).copy()
        title_config['text'] = self._wrap_title(title)
        layout_config['title'] = title_config
        fig.update_layout(**layout_config)
        # Unify hover label style, ensure consistency with global font
        fig.update_layout(hoverlabel=dict(
            bgcolor='white',
            bordercolor='#dee2e6',
            font=dict(
                family=layout_config.get('font', {}).get('family', "'Noto Sans', 'Noto Sans SC', sans-serif"),
                size=12,
                color='#333333'
            )
        ))
        
        return fig
    
    def create_smart_chart(self, data, chart_type: str, title: str, preserve_order: bool = False) -> go.Figure:
        """
        Smart generic chart function:
        - If data is 1D (single year), draw normal chart according to chart_type
        - If data is 2D (nested dictionary, representing 'All' years), automatically draw 100% stacked chart or multi-line chart
        """
        import pandas as pd
        import plotly.graph_objects as go
        
        if isinstance(data, pd.Series):
            data_dict = data.dropna().to_dict()
        elif isinstance(data, dict):
            data_dict = data
        else:
            data_dict = {}
            
        is_2d = False
        if data_dict:
            first_val = next(iter(data_dict.values()))
            if isinstance(first_val, dict):
                is_2d = True
                
        if not is_2d:
            return self.create_standardized_chart(data_dict, chart_type, title, preserve_order)
            
        # ---------------- ALL Years: Automatically generate generic 2D charts ----------------
        df = pd.DataFrame(data_dict).T.fillna(0)
        df.index.name = 'Year'
        df.sort_index(inplace=True)
        
        # Force preserve column order (to handle custom sorting requirements like Q11 partnership types)
        if preserve_order and data_dict:
            ordered_cols = []
            for y in data_dict:
                for col in data_dict[y]:
                    if col not in ordered_cols:
                        ordered_cols.append(col)
            # Append other columns not in the sorting list to the end
            for col in df.columns:
                if col not in ordered_cols:
                    ordered_cols.append(col)
            df = df[[col for col in ordered_cols if col in df.columns]]
        
        fig = go.Figure()
        colors = self.get_chart_colors()
        
        layout_config = self.get_global_chart_config('layout').copy()
        title_config = layout_config.get('title', {}).copy()
        title_config['text'] = self._wrap_title(title)
        layout_config['title'] = title_config
        layout_config['margin'] = dict(t=80, b=80, l=40, r=40)
        
        # 🌟 Branch 1: Draw Multi-Line Chart
        if chart_type == 'line':
            for i, option in enumerate(df.columns):
                display_name = self._to_title_case(str(option))
                fig.add_trace(go.Scatter(
                    name=display_name,
                    x=df.index,
                    y=df[option],
                    mode='lines+markers',     # Points + lines
                    marker=dict(size=8),      # Dot size
                    line=dict(width=3),       # Line thickness
                    marker_color=colors[i % len(colors)],
                    hovertemplate='<b>Year: %{x}</b><br>' + display_name + '<br>Count: %{y}<extra></extra>'
                ))
            
            fig.update_layout(
                **layout_config,
                yaxis=dict(title="Count (Absolute Value)"),
                xaxis=dict(type='category', title=""),
                legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5)
            )
            
        # 🌟 Branch 2: Draw 100% Stacked Bar Chart
        else:
            for i, option in enumerate(df.columns):
                display_name = self._to_title_case(str(option))
                fig.add_trace(go.Bar(
                    name=display_name,
                    x=df.index,
                    y=df[option],
                    marker_color=colors[i % len(colors)],
                    text=df[option],
                    textposition='inside',
                    hovertemplate='<b>Year: %{x}</b><br>' + display_name + '<br>Count: %{text}<extra></extra>'
                ))
            
            fig.update_layout(
                **layout_config,
                barmode='stack',
                barnorm='percent',
                yaxis=dict(title="Percentage (%)", ticksuffix="%", range=[0, 100]),
                xaxis=dict(type='category', title=""),
                legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5)
            )
            
        return fig

# Global style manager instance (for import by other modules)
style_manager = StreamlitStyleManager()

# Compatible page style application function (for import by other modules)
def apply_page_style():
    try:
        style_manager.apply_custom_css()
    except Exception:
        pass

# Compatible standardized chart function (for import by other modules)
def create_standardized_chart(data, chart_type: str, title: str, preserve_order: bool = False) -> go.Figure:
    return style_manager.create_standardized_chart(data, chart_type, title, preserve_order=preserve_order)

# Compatible table creation function (for import by other modules)
def create_table(df: pd.DataFrame, title: Optional[str] = None) -> str:
    return style_manager.create_data_table(df, title)

# Compatible metric card function (for import by other modules)
def create_metrics(metrics: List[Dict[str, Any]]) -> List[str]:
    cards = []
    for m in metrics or []:
        cards.append(style_manager.create_metric_card(
            m.get('title', ''), m.get('value', ''), m.get('delta'), m.get('delta_color', 'normal')
        ))
    return cards

# Compatible unified chart creation entry point (for import by other modules)
# Modify the original create_chart function at the bottom of st_styles.py
def create_chart(data, chart_type: str = 'bar', title: str = '', **kwargs) -> go.Figure:
    preserve_order = kwargs.get('preserve_order', False)
    # Direct traffic to the new smart chart function
    return style_manager.create_smart_chart(data, chart_type, title, preserve_order=preserve_order)

    # Custom: Fixed-width vertical legend (simulated using annotations)
    def _wrap_legend_text(self, text: str, max_chars: int) -> str:
        """Simple line wrap by character count, returns text with <br>"""
        words = str(text).split()
        lines = []
        current = ''
        for w in words:
            if len(current) + len(w) + (1 if current else 0) <= max_chars:
                current = f"{current} {w}".strip()
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        return '<br>'.join(lines)

    def add_fixed_width_vertical_legend(self, fig: go.Figure, labels: List[str], colors: List[str], *,
                                        x: float = 1.02, y: float = 1.0, max_chars: int = 24,
                                        font_size: int = 12, row_gap: float = 0.05) -> None:
        """
        Add custom vertical legend to the right of the chart:
        - Fixed text width (approximate by character count), wraps automatically when exceeded
        - Each legend item on a separate line, height adapts automatically
        - Use annotations to represent colored blocks and text
        """
        # Starting position (paper coordinates)
        y_cursor = y
        symbol_x = x - 0.02  # Place color block to the left of the text
        for idx, label in enumerate(labels):
            wrapped = self._wrap_legend_text(label, max_chars=max_chars)
            # Text annotation
            fig.add_annotation(
                xref='paper', yref='paper',
                x=x, y=y_cursor,
                text=wrapped,
                showarrow=False,
                align='left',
                xanchor='left',
                yanchor='top',
                font=dict(size=font_size, color='#333'),
            )
            # Color block annotation (simulating ■ using text block)
            fig.add_annotation(
                xref='paper', yref='paper',
                x=symbol_x, y=y_cursor,
                text='■',
                showarrow=False,
                yanchor='top',
                font=dict(size=font_size+4, color=colors[idx % len(colors)])
            )
            # Move cursor down based on the number of lines
            lines = wrapped.count('<br>') + 1
            y_cursor -= row_gap + (lines - 1) * (row_gap * 0.8)