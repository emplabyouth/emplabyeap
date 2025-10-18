import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional
import pandas as pd

class StreamlitStyleManager:
    """Streamlit样式管理器 - 简化版本"""
    
    def __init__(self):
        """初始化样式管理器"""
        self.theme_colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#17becf',
            'light': '#7f7f7f',
            'dark': '#bcbd22'
        }
        
        self.chart_colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
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
                    }
                },
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'margin': dict(l=40, r=40, t=60, b=40)
            }
        }
    
    def get_theme_colors(self) -> Dict[str, str]:
        """获取主题颜色"""
        return self.theme_colors
    
    def get_chart_colors(self) -> List[str]:
        """获取图表颜色"""
        return self.chart_colors
    
    def get_global_chart_config(self, chart_type: str = None) -> dict:
        """获取全局图表配置"""
        if chart_type and chart_type in self.global_chart_config:
            return self.global_chart_config[chart_type]
        return self.global_chart_config
    
    def apply_custom_css(self):
        """应用自定义CSS样式 - 简化版本"""
        st.markdown(f"""
        <style>
        /* 导入Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&family=Noto+Sans:wght@400;700&display=swap');
        
        /* 全局字体设置 */
        .stApp {{
            font-family: 'Noto Sans', 'Noto Sans SC', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}

        /* 根变量 */
        :root {{
            --primary-color: {self.theme_colors['primary']};
            --secondary-color: {self.theme_colors['secondary']};
            --success-color: {self.theme_colors['success']};
            --warning-color: {self.theme_colors['warning']};
            --info-color: {self.theme_colors['info']};
            --light-color: {self.theme_colors['light']};
            --dark-color: {self.theme_colors['dark']};
        }}
        
        /* 主容器样式 */
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }}
        
        /* 标题样式 */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 600;
            color: #1f1f1f;
        }}
        
        /* 表格样式 */
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
        
        /* 指标卡片样式 */
        .metric-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid var(--primary-color);
        }}
        
        /* 图表容器样式 */
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
        """创建指标卡片"""
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
        """创建数据表格"""
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
        """创建水平条形图"""
        # 处理标签长度
        if max_label_length and len(df) > 0:
            df = df.copy()
            df[y_col] = df[y_col].astype(str).apply(
                lambda x: x[:max_label_length] + '...' if len(x) > max_label_length else x
            )
        
        # 创建图表
        if color_col and color_col in df.columns:
            fig = px.bar(df, x=x_col, y=y_col, color=color_col,
                        orientation='h', title=title,
                        color_discrete_sequence=self.chart_colors)
        else:
            fig = px.bar(df, x=x_col, y=y_col, orientation='h', title=title,
                        color_discrete_sequence=[self.chart_colors[0]])
        
        # 应用全局配置
        fig.update_layout(self.global_chart_config['layout'])
        
        return fig