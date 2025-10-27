import streamlit as st
import sys
import os
import pandas as pd

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import st_q6q7q10q11_dashboard
import st_landing_dashboard

st.set_page_config(
    page_title="ILO Youth Employment Action Plan (YEAP)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def safe_read_csv(file_path):
    """
    Safely read CSV file with automatic encoding detection
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, try without specifying  encoding
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Failed to read {file_path}: {str(e)}")
        return pd.DataFrame()


# add custom css style, set title color to light gray
# Remove old global main title to declutter header area

# Apply global styles as early as possible so sidebar filters also get CSS
try:
    from st_styles import apply_page_style as _apply_global_style
    _apply_global_style()
except Exception:
    pass

PAGES = {
    "🏠 Overview": st_landing_dashboard,
    "📚 Knowledge Development & Dissemination": st_q6q7q10q11_dashboard,
    "🔧 Technical Assistance": st_q6q7q10q11_dashboard,
    "🎓 Capacity Development": st_q6q7q10q11_dashboard,
    "🤝 Advocacy & Partnerships": st_q6q7q10q11_dashboard,
}

st.sidebar.title("Navigation")

def _on_page_change():
    # 设置页面重置标记
    st.session_state['_page_reset_requested'] = True
    
    # 对于使用相同模块的页面间切换，强制清除更多状态
    current_selection = st.session_state.get('page_selection', '')
    previous_selection = st.session_state.get('_previous_page_selection', '')
    
    # 检查是否是在使用相同模块的页面间切换
    same_module_pages = [
        "📚 Knowledge Development & Dissemination",
        "🔧 Technical Assistance", 
        "🎓 Capacity Development",
        "🤝 Advocacy & Partnerships"
    ]
    
    if current_selection in same_module_pages and previous_selection in same_module_pages:
        # 强制清除所有相关状态，确保完全重新初始化
        st.session_state['_force_full_reset'] = True
    
    # 记录当前页面选择
    st.session_state['_previous_page_selection'] = current_selection

selection = st.sidebar.radio("Go to", list(PAGES.keys()), key="page_selection", on_change=_on_page_change)

# 处理页面重置请求
if st.session_state.get('_page_reset_requested', False):
    # 清除所有页面相关的session state，强制重新初始化
    keys_to_clear = []
    for key in st.session_state.keys():
        # 保留全局设置，清除页面特定的状态
        if not key.startswith('selected_year') and not key.startswith('selected_region') and not key.startswith('year_options') and not key.startswith('regions_options'):
            # 对于强制完全重置的情况，清除更多状态
            if st.session_state.get('_force_full_reset', False):
                if key not in ['page_selection', '_page_reset_requested', '_force_full_reset', '_previous_page_selection']:
                    keys_to_clear.append(key)
            else:
                # 始终清除分页相关的状态，确保滚动重置正常工作
                if key not in ['page_selection', '_page_reset_requested', '_previous_page_selection'] or key.startswith('outputs_current_page_'):
                    keys_to_clear.append(key)
    
    for key in keys_to_clear:
        del st.session_state[key]
    
    # 设置滚动到顶部标记
    st.session_state['_scroll_to_top'] = True
    
    # 清除重置标记
    st.session_state['_page_reset_requested'] = False
    if '_force_full_reset' in st.session_state:
        del st.session_state['_force_full_reset']
    
    # 强制重新运行
    st.rerun()

page = PAGES[selection]

# In-page top anchor for robust scrollIntoView behavior
TOP_ANCHOR_ID = 'yeap-top-anchor'
st.markdown(f'<div id="{TOP_ANCHOR_ID}" style="position:relative;top:-50px;height:0;"></div>', unsafe_allow_html=True)

# ---------------- Global Year Filter ----------------
# Always provide a global year filter
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, 'orignaldata')

    year_values = set()
    if os.path.isdir(data_dir):
        for fname in os.listdir(data_dir):
            if fname.lower().endswith('.csv'):
                fpath = os.path.join(data_dir, fname)
                try:
                    df = safe_read_csv(fpath)
                    # Check for both 'YEAR' and 'year' columns
                    if 'YEAR' in df.columns:
                        # Normalize to string and clean up, remove empty values
                        years = df['YEAR'].dropna().astype(str).str.strip()
                        years = years[years != ''].unique().tolist()
                        # Convert float-like strings to int strings (e.g., '2026.0' -> '2026')
                        years = [str(int(float(y))) if '.' in y and y.replace('.', '').isdigit() else y for y in years]
                        year_values.update(years)
                    elif 'year' in df.columns:
                        # Also check lowercase 'year' column
                        years = df['year'].dropna().astype(str).str.strip()
                        years = years[years != ''].unique().tolist()
                        # Convert float-like strings to int strings (e.g., '2026.0' -> '2026')
                        years = [str(int(float(y))) if '.' in y and y.replace('.', '').isdigit() else y for y in years]
                        year_values.update(years)
                except Exception:
                    # Skip files that cannot be read
                    pass

    # Build options: All + sorted years desc (as strings)
    year_options = ['All'] + sorted(year_values, reverse=True)
    if len(year_options) == 1:  # Only 'All'
        year_options = ['All', '2025']  # Fallback default to 2025

    st.sidebar.header("Filters")
    
    # Set default to 2025 if available, otherwise most recent year, otherwise 'All'
    default_index = 0  # Default to 'All'
    # Set default to 2024 if available, otherwise most recent year
    if '2024' in year_options:
        default_index = year_options.index('2024')
    elif '2025' in year_options:
        default_index = year_options.index('2025')
    elif len(year_options) > 1:
        default_index = 1  # Most recent year if neither 2024 nor 2025 available
    
    selected_year = st.sidebar.selectbox(
        "Select Period",
        year_options,
        index=default_index,
        key="selected_year",
    )
    # Expose to pages
    st.session_state['year_options'] = year_options
except Exception as e:
    st.sidebar.info(f"Year filtering not available - error: {e}")
# ---------------------------------------------------

# ---------------- Global shared filters (Organizational Unit) ----------------
# Check if any of the specialized analysis pages are selected
specialized_pages = [
    "📚 Knowledge Development & Dissemination", 
    "🔧 Technical Assistance",
    "🎓 Capacity Development",
    "🤝 Advocacy & Partnerships"
]

if selection in specialized_pages:  # Any specialized analysis page needs region filtering
    st.sidebar.header("Filters")
    try:
        # Build unified regions list from both PART2 and PART3 datasets
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        data_files = [
            # PART2 (Q3, Q4, Q5)
            os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ3.csv'),
            os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ4.csv'),
            os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ5.csv'),
            # PART3 (Q6, Q7, Q10, Q11)
            os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ6.csv'),
            os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ7.csv'),
            os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ10.csv'),
            os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ11.csv'),
        ]
        regions_set = set()
        for fp in data_files:
            if os.path.exists(fp):
                try:
                    df = safe_read_csv(fp)
                    if 'Department/Region' in df.columns:
                        regions_set.update(df['Department/Region'].dropna().unique())
                except Exception:
                    pass
        if regions_set:
            regions_options = ['All'] + sorted(list(regions_set))
            # Soft-wrapping for long labels in display only
            def _wrap_label(s: object) -> str:
                s = str(s)
                for ch in ['/', '\\', '-', '—', '–', '_', ' ', '（', '）', '(', ')', ':', '：', ',', '·']:
                    s = s.replace(ch, ch + '\u200B')
                return s
            selected_region = st.sidebar.selectbox(
                "Select Organizational Unit",
                regions_options,
                key="selected_region",
                format_func=_wrap_label,
            )
            # Expose to pages
            st.session_state['regions_options'] = regions_options
        else:
            st.sidebar.info("Regional filtering not available - no region data found.")
    except Exception as e:
        st.sidebar.info(f"Regional filtering not available - error: {e}")

# Set the selected analysis section based on the current page selection
if selection in specialized_pages:
    # Map page selection to analysis section
    page_to_section = {
        "📚 Knowledge Development & Dissemination": "Knowledge Development & Dissemination",
        "🔧 Technical Assistance": "Technical Assistance", 
        "🎓 Capacity Development": "Capacity Development",
        "🤝 Advocacy & Partnerships": "Advocacy & Partnerships"
    }
    
    # Set the selected section in session state
    st.session_state['selected_analysis_section'] = page_to_section[selection]
# ---------------------------------------------------------------------------

# Check if the selected page has a create_layout function
if hasattr(page, 'create_layout'):
    page.create_layout()
else:
    st.error("The selected page does not have a create_layout function.")

# Re-apply global styles at end so our <style> appears last
try:
    _apply_global_style()
except Exception:
    pass

# 确保在页面渲染完成后滚动到顶部
if st.session_state.get('_scroll_to_top', False):
    import streamlit.components.v1 as components
    components.html(
        f"""
        <script>
        (function() {{
            function scrollToTop() {{
                try {{
                    // 尝试滚动到锚点
                    const anchor = window.parent.document.getElementById('{TOP_ANCHOR_ID}');
                    if (anchor) {{
                        anchor.scrollIntoView({{behavior: 'auto', block: 'start'}});
                        return;
                    }}
                    
                    // 如果没有锚点，尝试滚动主容器
                    const containers = [
                        window.parent.document.documentElement,
                        window.parent.document.body,
                        window.parent.document.querySelector('section.main'),
                        window.parent.document.querySelector('.main'),
                        window.parent.document.querySelector('[data-testid="stAppViewContainer"]'),
                        window.parent.document.querySelector('[data-testid="stAppViewBlockContainer"]'),
                        window.parent.document.querySelector('.block-container')
                    ];
                    
                    containers.forEach(container => {{
                        if (container) {{
                            try {{
                                container.scrollTop = 0;
                            }} catch(e) {{}}
                        }}
                    }});
                    
                    // 最后尝试窗口滚动
                    window.parent.scrollTo(0, 0);
                }} catch(e) {{
                    console.log('Scroll error:', e);
                }}
            }}
            
            // 立即执行一次
            scrollToTop();
            
            // 延迟执行几次确保生效
            setTimeout(scrollToTop, 100);
            setTimeout(scrollToTop, 300);
            setTimeout(scrollToTop, 500);
        }})();
        </script>
        """,
        height=0,
    )
    st.session_state['_scroll_to_top'] = False
