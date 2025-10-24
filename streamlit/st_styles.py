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
                    'x': 0.5,  # 标题居中
                    'xanchor': 'center',  # 标题锚点居中
                    'pad': {'b': 10}
                },
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'margin': dict(l=40, r=40, t=70, b=40)
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

        /* 正文字体工具类与通用应用 */
        .yeap-body-text, .yeap-body-text p, .yeap-body-text li, .yeap-body-text span {{
            font-family: 'Noto Sans', 'Noto Sans SC', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-size: 15px;
            line-height: 1.6;
            color: #333333;
        }}

        /* 默认 Markdown 正文字体同步（与 yeap-body-text 保持一致） */
        .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span, .markdown-text-container {{
            font-family: 'Noto Sans', 'Noto Sans SC', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-size: 15px;
            line-height: 1.6;
            color: #333333;
        }}

        /* 取消正文加粗样式 */
        .yeap-body-text b, .yeap-body-text strong {{ font-weight: 400 !important; }}
        .stMarkdown b, .stMarkdown strong, .markdown-text-container b, .markdown-text-container strong {{ font-weight: 400 !important; }}

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
            padding-top: 0rem; /* 去掉顶部内边距，确保切页后完全贴顶 */
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

    def create_plotly_theme(self) -> dict:
        """提供与可视化层兼容的主题结构"""
        return {'layout': self.global_chart_config['layout']}

    def _wrap_title(self, title: str, max_chars: int = 120) -> str:
        """换行长标题以避免溢出"""
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
        """将标签文本首字母大写（保留短大写缩写，如 ILO、UN）。"""
        if s is None:
            return ''
        s = str(s)
        def _cap_word(w: str) -> str:
            # 保留全大写且较短的缩写
            if w.isupper() and len(w) <= 5:
                return w
            # 处理连字符词
            return '-'.join(sub.capitalize() if sub else '' for sub in w.split('-'))
        return ' '.join(_cap_word(part) for part in s.split())

    # 自定义：固定宽度纵向图例（使用注释模拟）
    def _wrap_legend_text(self, text: str, max_chars: int = 18) -> str:
        """按字符数进行简单换行，返回带<br>的文本"""
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
        在图右侧添加自定义纵向图例：
        - 固定文本宽度（按字符数近似），超过部分自动换行
        - 每个图例项独占一行，高度自适应
        - 使用注释表示文本，使用 shape 绘制彩色方块，避免重叠
        """
        # 预先计算行数以便估算盒子高度
        wrapped_labels = [self._wrap_legend_text(lbl, max_chars=max_chars) for lbl in labels]
        total_lines = sum(wl.count('<br>') + 1 for wl in wrapped_labels)

        # 起始位置（paper坐标, 保持在画布内）
        y_cursor = y
        x_text = x
        symbol_x = x_text - 0.03  # 彩色方块靠左
        symbol_w = 0.015
        symbol_h = 0.02
        for idx, wrapped in enumerate(wrapped_labels):
            # 文本注释
            fig.add_annotation(
                xref='paper', yref='paper',
                x=x_text, y=y_cursor,
                text=wrapped,
                showarrow=False,
                align='left',
                xanchor='left',
                yanchor='middle',
                font=dict(size=font_size, color='#333'),
            )
            # 彩色方块（改为shape矩形，更好对齐）
            fig.add_shape(
                type='rect',
                xref='paper', yref='paper',
                x0=symbol_x, x1=symbol_x + symbol_w,
                y0=y_cursor - symbol_h/2, y1=y_cursor + symbol_h/2,
                line=dict(width=0),
                fillcolor=colors[idx % len(colors)],
                layer='above'
            )
            # 根据行数下移游标
            lines = wrapped.count('<br>') + 1
            y_cursor -= row_gap + (lines - 1) * (row_gap * 0.6)

        if draw_box:
            # 绘制一个包含所有图例的矩形框（保持在画布范围内）
            height_est = total_lines * row_gap + 0.04
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
        """标准化图表创建，统一样式，支持 pie/bar/horizontal_bar，对区域图表使用渐变色"""
        # 支持 Series 或 dict
        if isinstance(data, pd.Series):
            series = data.dropna()
            data_dict = series.to_dict()
        elif isinstance(data, dict):
            data_dict = {str(k): int(v) if pd.notna(v) else 0 for k, v in data.items()}
        else:
            data_dict = {}
        
        # 排序（除非要求保留原始顺序）
        if not preserve_order and chart_type in ['bar', 'horizontal_bar']:
            data_dict = dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))
        
        labels = [self._to_title_case(lbl) for lbl in list(data_dict.keys())]
        values = list(data_dict.values())
        
        # 检查是否为区域相关图表、Partnership类型图表或频次分析图表，使用渐变色
        is_region_chart = any(keyword in title.lower() for keyword in ['region', 'regions', 'across regions'])
        is_partnership_chart = any(keyword in title.lower() for keyword in ['partnership', 'advocacy'])
        is_frequency_chart = any(keyword in title.lower() for keyword in ['types of', 'outputs delivered', 'frequency', 'distribution'])
        
        if (is_region_chart or is_partnership_chart or is_frequency_chart) and chart_type == 'bar':
            # 使用渐变色配色方案
            gradient_colors_hex = [
                '#BEDCfa',  # rgb(190, 220, 250) - 最浅
                '#82AFDC',  # rgb(130, 175, 220)
                '#5A87CD',  # rgb(90, 135, 205)
                '#3264C8',  # rgb(50, 100, 200)
                '#1E2DBE',  # rgb(30, 45, 190) - ILO BLUE (主色)
                '#151F85',  # rgb(21, 31, 133)
                '#230050'   # rgb(35, 0, 80) - 最深
            ]
            
            # 根据数值大小分配颜色（数值越大颜色越深）
            if values:
                max_val = max(values)
                min_val = min(values)
                val_range = max_val - min_val if max_val != min_val else 1
                
                colors = []
                for val in values:
                    # 计算颜色索引（数值越大索引越大，颜色越深）
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
                width=0.6,  # 调整柱子宽度，使其更细
                showlegend=False  # 确保柱状图不显示图例
            )])
            
            # 添加渐变色图例条（优化显示效果）
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(
                    colorscale=[[i/(len(gradient_colors_hex)-1), color] for i, color in enumerate(gradient_colors_hex)],
                    showscale=True,
                    cmin=min_val if values else 0,
                    cmax=max_val if values else 1,
                    colorbar=dict(
                        title={'text': ''},  # 彻底移除标题，避免 trace 0
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
                name=' ',  # 防止 Plotly 回退到 trace 0
                hoverinfo='skip'
            ))
        else:
            # 使用标准颜色
            colors = self.get_chart_colors()
            
            if chart_type == 'pie':
                fig = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    marker_colors=colors[:len(labels)]
                )])
                # 禁用内置图例，改用自定义纵向固定宽度图例
                fig.update_layout(
                    margin=dict(l=20, r=180, t=60, b=20),
                    autosize=True,
                    showlegend=False
                )
                # 添加自定义图例（固定宽度，文本可换行，逐行显示）
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
        
        # 应用统一布局和标题换行
        layout_config = self.get_global_chart_config('layout').copy()
        title_config = layout_config.get('title', {}).copy()
        title_config['text'] = self._wrap_title(title)
        layout_config['title'] = title_config
        fig.update_layout(**layout_config)
        # 统一悬停标签样式，确保与全局字体保持一致
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

# 全局样式管理器实例（供其他模块导入）
style_manager = StreamlitStyleManager()

# 兼容页面样式应用函数（供其他模块导入）
def apply_page_style():
    try:
        style_manager.apply_custom_css()
    except Exception:
        pass

# 兼容的标准化图表函数（供其他模块导入）
def create_standardized_chart(data, chart_type: str, title: str, preserve_order: bool = False) -> go.Figure:
    return style_manager.create_standardized_chart(data, chart_type, title, preserve_order=preserve_order)

# 兼容的表格创建函数（供其他模块导入）
def create_table(df: pd.DataFrame, title: Optional[str] = None) -> str:
    return style_manager.create_data_table(df, title)

# 兼容的指标卡片函数（供其他模块导入）
def create_metrics(metrics: List[Dict[str, Any]]) -> List[str]:
    cards = []
    for m in metrics or []:
        cards.append(style_manager.create_metric_card(
            m.get('title', ''), m.get('value', ''), m.get('delta'), m.get('delta_color', 'normal')
        ))
    return cards

# 兼容的统一图表创建入口（供其他模块导入）
def create_chart(data, chart_type: str = 'bar', title: str = '', **kwargs) -> go.Figure:
    preserve_order = kwargs.get('preserve_order', False)
    return style_manager.create_standardized_chart(data, chart_type, title, preserve_order=preserve_order)


    # 自定义：固定宽度纵向图例（使用注释模拟）
    def _wrap_legend_text(self, text: str, max_chars: int) -> str:
        """按字符数进行简单换行，返回带<br>的文本"""
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
        在图右侧添加自定义纵向图例：
        - 固定文本宽度（按字符数近似），超过部分自动换行
        - 每个图例项单独一行，高度自适应
        - 使用注释表示彩色方块和文本
        """
        # 起始位置（paper坐标）
        y_cursor = y
        symbol_x = x - 0.02  # 彩色方块靠左
        for idx, label in enumerate(labels):
            wrapped = self._wrap_legend_text(label, max_chars=max_chars)
            # 文本注释
            fig.add_annotation(
                xref='paper', yref='paper',
                x=x, y=y_cursor,
                text=wrapped,
                showarrow=False,
                align='left',
                font=dict(size=font_size, color='#333'),
            )
            # 彩色方块（用文本块模拟 ■）
            fig.add_annotation(
                xref='paper', yref='paper',
                x=symbol_x, y=y_cursor,
                text='■',
                showarrow=False,
                font=dict(size=font_size+4, color=colors[idx % len(colors)])
            )
            # 根据行数下移游标
            lines = wrapped.count('<br>') + 1
            y_cursor -= row_gap + (lines - 1) * (row_gap * 0.6)