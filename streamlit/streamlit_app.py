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
    st.session_state['_scroll_to_top'] = True

selection = st.sidebar.radio("Go to", list(PAGES.keys()), key="page_selection", on_change=_on_page_change)
page = PAGES[selection]

# In-page top anchor for robust scrollIntoView behavior
TOP_ANCHOR_ID = 'yeap-top-anchor'
st.markdown(f'<div id="{TOP_ANCHOR_ID}" style="position:relative;height:0;"></div>', unsafe_allow_html=True)

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

# Ensure scrolling to top once the page finishes rendering
if st.session_state.get('_scroll_to_top', False):
    import streamlit.components.v1 as components
    components.html(
        """
        <script>
        (function(){
          var attempts = 0;
          function scrollTop(){
            attempts++;
            try {
              var parentDoc = window.parent && window.parent.document ? window.parent.document : document;
              var anchor = parentDoc.getElementById('yeap-top-anchor');
              if (anchor && anchor.scrollIntoView) {
                anchor.scrollIntoView({behavior:'auto', block:'start'});
              } else {
                var main = parentDoc.querySelector('section.main') || parentDoc.querySelector('.main') || parentDoc.querySelector('[data-testid="stAppViewContainer"]') || parentDoc.querySelector('[data-testid="stAppViewBlockContainer"]') || parentDoc.querySelector('.block-container');
                if (main && main.scrollTop !== undefined) { main.scrollTop = 0; }
                if (main && main.scrollTo) { main.scrollTo({top:0, behavior:'auto'}); }
                window.scrollTo(0,0);
              }
            } catch(e) { window.scrollTo(0,0); }
            if (attempts < 5) setTimeout(scrollTop, 100);
          }
          setTimeout(scrollTop, 0);
        })();
        </script>
        """,
        height=0,
    )
    st.session_state['_scroll_to_top'] = False