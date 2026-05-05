"""
Technical Assistance page - Implementation that works with st_q6q7q10q11_dashboard.py
This file only handles the Technical Assistance section of the dashboard.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import base64
from typing import Dict, Any, List

# Import from main dashboard file
from st_q6q7q10q11_dashboard import (
    Q6Q7Q10Q11DataProcessor, 
    create_theme_count_chart,
    STANDARD_COLORS,
    create_unified_header,
    get_base64_image
)

# Import chart creation function for proper color handling
try:
    from st_styles import create_chart
    CHART_FUNCTION_AVAILABLE = True
except ImportError:
    CHART_FUNCTION_AVAILABLE = False

def create_layout():
    """Main entry point for the Technical Assistance page"""
    # 添加顶部锚点
    st.markdown('<div id="yeap-top-anchor"></div>', unsafe_allow_html=True)
    
    # 强制页面置顶 - 使用多种方法确保成功
    st.markdown("""
    <script>
    function forceScrollToTop() {
        // 方法1: 标准滚动
        window.scrollTo({top: 0, behavior: 'instant'});
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
        
        // 方法2: 查找并滚动所有可能的容器
        const selectors = [
            'main', '.main', '.stApp', 
            '[data-testid="stAppViewContainer"]',
            '[data-testid="block-container"]',
            '.css-1d391kg', '.css-18e3th9', '.css-1lcbmhc',
            '[style*="overflow"]', '[style*="scroll"]'
        ];
        
        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (element && element.scrollTop !== undefined) {
                    element.scrollTop = 0;
                }
            });
        });
        
        // 方法3: 滚动到锚点
        const anchor = document.getElementById('yeap-top-anchor');
        if (anchor) {
            anchor.scrollIntoView({behavior: 'instant', block: 'start'});
        }
        
        // 方法4: 强制重置所有滚动位置
        const allElements = document.querySelectorAll('*');
        allElements.forEach(element => {
            if (element.scrollTop > 0) {
                element.scrollTop = 0;
            }
            if (element.scrollLeft > 0) {
                element.scrollLeft = 0;
            }
        });
    }
    
    // 立即执行
    forceScrollToTop();
    
    // 延迟执行多次，确保页面完全加载后也能置顶
    setTimeout(forceScrollToTop, 50);
    setTimeout(forceScrollToTop, 100);
    setTimeout(forceScrollToTop, 200);
    setTimeout(forceScrollToTop, 500);
    
    // 监听页面变化
    if (window.MutationObserver) {
        const observer = new MutationObserver(function(mutations) {
            let shouldScroll = false;
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    shouldScroll = true;
                }
            });
            if (shouldScroll) {
                setTimeout(forceScrollToTop, 10);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // 5秒后停止观察
        setTimeout(() => observer.disconnect(), 5000);
    }
    </script>
    """, unsafe_allow_html=True)
    
    # 使用 Streamlit 的 empty 组件强制重新渲染
    if '_scroll_to_top' not in st.session_state:
        st.session_state['_scroll_to_top'] = True
    
    create_technical_assistance_layout()


def create_technical_assistance_layout(data_processor=None, filtered_user_ids=None):
    """Create Technical Assistance layout - this function is called from the main dashboard"""
    # Create unified header with logo and title for all pages
    create_unified_header()
    
    # Get global filter values from session state
    selected_year = st.session_state.get('selected_year', 'All')
    selected_region = st.session_state.get('selected_region', 'All')
    
    # Initialize data processor with base path
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if data_processor is None:
        data_processor = Q6Q7Q10Q11DataProcessor(base_path)
    
    # Apply region filtering if needed (similar to original implementation)
    if selected_region != 'All':
        try:
            # Load the original data to get filtered user IDs
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            data_files = [
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ6.csv'),
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ7.csv'),
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ10.csv'),
                os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ11.csv'),
            ]
            
            filtered_user_ids = None
            for fp in data_files:
                if os.path.exists(fp):
                    try:
                        df = pd.read_csv(fp)
                        if 'Department/Region' in df.columns:
                            filtered_data = df[df['Department/Region'] == selected_region]
                            if not filtered_data.empty and 'UserId' in filtered_data.columns:
                                if filtered_user_ids is None:
                                    filtered_user_ids = set(filtered_data['UserId'].unique())
                                else:
                                    filtered_user_ids.update(filtered_data['UserId'].unique())
                    except Exception:
                        pass
            
            # Apply region filter to data processor if we have filtered user IDs
            if filtered_user_ids is not None:
                from st_q6q7q10q11_dashboard import apply_region_filter_to_processor
                data_processor = apply_region_filter_to_processor(data_processor, list(filtered_user_ids))
                st.info(f"Showing data for: {selected_region}")
        except Exception as e:
            st.warning(f"Region filtering encountered an issue: {str(e)}. Showing all data.")
    
    # Apply year filtering if needed
    if selected_year != 'All':
        try:
            # Filter combined_data by year if it exists
            if data_processor.combined_data is not None and not data_processor.combined_data.empty:
                if 'YEAR' in data_processor.combined_data.columns:
                    data_processor.combined_data = data_processor.combined_data[
                        data_processor.combined_data['YEAR'].astype(str) == str(selected_year)
                    ]
                elif 'year' in data_processor.combined_data.columns:
                    data_processor.combined_data = data_processor.combined_data[
                        data_processor.combined_data['year'].astype(str) == str(selected_year)
                    ]
                # Recalculate statistics after year filtering
                data_processor._recalculate_works_count_stats()
        except Exception as e:
            st.warning(f"Year filtering encountered an issue: {str(e)}. Showing all data.")
    
    # First section: Description text and links
    st.subheader("🔧 Technical Assistance")
    st.markdown("""This tab highlights the ILO's technical support to countries in developing and implementing **gender-responsive youth employment policies and strategies**. Activities include support for **national employment policies**, **entrepreneurship programmes**, **job creation measures**, and **social protection for youth**. It also covers policy responses to **future-of-work trends**, such as **technology, climate change**, and the **care economy**, as well as efforts to promote **equal opportunities**, **rights at work**, and a **just transition**.

**Additional resources:**
- [ILO Employment Policy Gateway](https://webapps.ilo.org/empolgateway/)""")
    
    st.markdown("---")
    
    # Second section: Clusters Of The Implementation Framework
    st.subheader("📊 Clusters Of The Implementation Framework")
    works_count_data = data_processor.get_works_count_data()
    if works_count_data:
        count_fig = create_theme_count_chart(data_processor, current_theme='Q7')
        if count_fig:
            st.plotly_chart(count_fig, width='stretch')
    else:
        st.info("No data available for Clusters Of The Implementation Framework")
    
    st.markdown("---")
    
    # Third section: Frequency Analysis
    st.subheader("📊 Frequency Analysis")
    
    # Get Q7 theme info for charts
    theme_charts = [
        ('Funding source (Options: regular budget or extrabudgetary)', 'pie', 'Funding Source Of Technical Assistance Outputs'),
        ('Focus \n(Options: Youth only or Youth is one of the target groups)', 'pie', 'Target Group Of Technical Assistance Outputs'),
        ('Country or Region', 'bar', 'Technical Assistance Outputs Across Regions')
    ]
    
    # Check if any frequency data exists
    has_frequency_data = False
    for field_name, chart_type, chart_title in theme_charts:
        field_data = data_processor.get_field_distribution('Q7', field_name)
        if field_data:
            has_frequency_data = True
            break
    
    if has_frequency_data:
        # 获取当前选中的年份
        selected_year = st.session_state.get('selected_year', 'All')
        
        # 定义哪些特定的图表在选 All 时需要变成折线图
        line_chart_targets = [
            'Technical Assistance Outputs Across Regions'
        ]
        
        for field_name, chart_type, chart_title in theme_charts:
            
            # ---------------- 智能拦截逻辑 ----------------
            if selected_year == 'All' and chart_type == 'pie':
                # 1. 饼图 -> 100% 堆叠柱状图
                field_data = data_processor.get_time_series_distribution('Q7', field_name)
                preserve_order = False
                
            elif selected_year == 'All' and chart_title in line_chart_targets:
                # 2. 特定的柱状图 -> 多折线图
                field_data = data_processor.get_time_series_distribution('Q7', field_name)
                chart_type = 'line'  # 通知底层画折线[cite: 16]
                
                # 折线图中的 Top 10 计算（跨年份总和）[cite: 16]
                if 'Region' in chart_title or 'Regions' in chart_title:
                    region_totals = {}
                    for y, cats in field_data.items():
                        for reg, val in cats.items():
                            region_totals[reg] = region_totals.get(reg, 0) + val
                    top_10 = sorted(region_totals.keys(), key=lambda k: region_totals[k], reverse=True)[:10]
                    field_data = {y: {reg: cats[reg] for reg in top_10 if reg in cats} for y, cats in field_data.items()}
                preserve_order = False
                
            else:
                # 3. 否则走原本的 1D 数据提取逻辑
                field_data = data_processor.get_field_distribution('Q7', field_name)
                if field_data:
                    # 处理 Top 10 Region[cite: 13]
                    if 'Region' in chart_title or 'Regions' in chart_title:
                        field_data = dict(sorted(field_data.items(), key=lambda x: x[1], reverse=True)[:10])
                preserve_order = False
            # ----------------------------------------------

            if field_data:
                # Use the same chart creation function as the original file[cite: 13]
                if CHART_FUNCTION_AVAILABLE:
                    fig = create_chart(field_data, chart_type, chart_title, preserve_order=preserve_order)
                else:
                    # Fallback to basic chart creation[cite: 13]
                    if chart_type == 'pie':
                        df = pd.DataFrame(list(field_data.items()), columns=['Category', 'Count'])
                        fig = px.pie(
                            df, 
                            values='Count', 
                            names='Category',
                            title=chart_title,
                            color_discrete_sequence=STANDARD_COLORS
                        )
                    elif chart_type == 'bar':
                        df = pd.DataFrame(list(field_data.items()), columns=['Category', 'Count'])
                        df = df.sort_values('Count', ascending=False)
                        
                        fig = px.bar(
                            df, 
                            x='Category', 
                            y='Count',
                            title=chart_title,
                            color='Count',  
                            color_continuous_scale='Blues'  
                        )
                    else:
                        fig = None # 避免未定义错误
                
                if fig:
                    fig.update_layout(height=500)
                    # 使用新的 width='stretch' 规范[cite: 13]
                    st.plotly_chart(fig, width='stretch')
    else:
        st.info("No frequency analysis data available for Technical Assistance")
    
    st.markdown("---")
    
    # Fourth section: Outputs Detail List
    st.subheader("📋 Outputs Detail List")
    
    # Import the detail list creation function
    try:
        from st_q6q7q10q11_dashboard import create_theme_detail_list
        detail_df = create_theme_detail_list(data_processor, 'Q7')
        
        if detail_df is not None and not detail_df.empty:
            total_records = len(detail_df)
            
            # Initialize session state for current page if not exists
            page_key = 'outputs_current_page_Q7'
            if page_key not in st.session_state:
                st.session_state[page_key] = 1
            
            # Get current page data
            items_per_page = st.session_state.get('items_per_page', 50)
            total_pages = (total_records - 1) // items_per_page + 1
            
            # Calculate display range
            start_idx = (st.session_state[page_key] - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_records)
            
            # Get current page data
            display_df = detail_df.iloc[start_idx:end_idx].copy()
            
            st.dataframe(display_df, width='stretch')
            
            # Compact pagination controls
            st.markdown("<br>", unsafe_allow_html=True)
            
            # First row: Page info centered at the top
            st.markdown(
                f"<div style='text-align: center; margin: 10px 0;'>"
                f"<strong>Page {st.session_state[page_key]} of {total_pages}</strong> | "
                f"Showing {start_idx + 1}-{end_idx} of {total_records} records"
                f"</div>", 
                unsafe_allow_html=True
            )
            
            # Second row: Items per page and Jump to page side by side
            control_col1, control_col2 = st.columns([1, 1])
            
            with control_col1:
                # Items per page
                new_items_per_page = st.selectbox(
                    "Items per page:",
                    options=[10, 25, 50, 100, 200],
                    index=[10, 25, 50, 100, 200].index(items_per_page) if items_per_page in [10, 25, 50, 100, 200] else 2,
                    key=f"items_per_page_Q7"
                )
                
                if new_items_per_page != items_per_page:
                    st.session_state.items_per_page = new_items_per_page
                    st.session_state[page_key] = 1
                    st.rerun()
            
            with control_col2:
                # Jump to page
                new_page = st.number_input(
                    "Jump to page:",
                    min_value=1,
                    max_value=total_pages,
                    value=st.session_state[page_key],
                    key=f"page_input_Q7"
                )
                if new_page != st.session_state[page_key]:
                    st.session_state[page_key] = new_page
                    st.rerun()
            
        else:
            st.info("No detailed output data available for Technical Assistance")
    except Exception as e:
        st.error(f"Error loading output details: {e}")
    
def create_layout():
    """Create Technical Assistance layout - this function is called from the main app"""
    # Create data processor
    data_processor = Q6Q7Q10Q11DataProcessor()
    
    # Create layout
    create_technical_assistance_layout(data_processor)