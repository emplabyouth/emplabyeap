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
import st_technical_assistance_new

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
    
    # If all encodings fail, try without specifying encoding
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Failed to read {file_path}: {str(e)}")
        return pd.DataFrame()


# Add custom css style, set title color to light gray
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
    "🔧 Technical Assistance": st_technical_assistance_new,
    "🎓 Capacity Development": st_q6q7q10q11_dashboard,
    "🤝 Advocacy & Partnerships": st_q6q7q10q11_dashboard,
}

st.sidebar.title("Navigation")

def _on_page_change():
    # Set page reset flag
    st.session_state['_page_reset_requested'] = True
    
    # Set scroll to top flag - all page switches need to scroll to top
    st.session_state['_scroll_to_top'] = True
    
    # For switching between pages using the same module, force clear more states
    current_selection = st.session_state.get('page_selection', '')
    previous_selection = st.session_state.get('_previous_page_selection', '')
    
    # Check if switching between pages that use the same module
    same_module_pages = [
        "📚 Knowledge Development & Dissemination",
        "🔧 Technical Assistance", 
        "🎓 Capacity Development",
        "🤝 Advocacy & Partnerships"
    ]
    
    if current_selection in same_module_pages and previous_selection in same_module_pages:
        # Force clear all relevant states to ensure complete re-initialization
        st.session_state['_force_full_reset'] = True
    
    # Record current page selection
    st.session_state['_previous_page_selection'] = current_selection

selection = st.sidebar.radio("Go to", list(PAGES.keys()), key="page_selection", on_change=_on_page_change)

# Process page reset requests
if st.session_state.get('_page_reset_requested', False):
    # Clear all page-related session states, force re-initialization
    keys_to_clear = []
    for key in st.session_state.keys():
        # Keep global settings, clear page-specific states
        if not key.startswith('selected_year') and not key.startswith('selected_region') and not key.startswith('year_options') and not key.startswith('regions_options'):
            # For cases requiring a forced full reset, clear more states
            if st.session_state.get('_force_full_reset', False):
                if key not in ['page_selection', '_page_reset_requested', '_force_full_reset', '_previous_page_selection']:
                    keys_to_clear.append(key)
            else:
                # Always clear pagination-related states to ensure scroll reset works properly
                if key not in ['page_selection', '_page_reset_requested', '_previous_page_selection'] or key.startswith('outputs_current_page_'):
                    keys_to_clear.append(key)
    
    for key in keys_to_clear:
        del st.session_state[key]
    
    # Set scroll to top flag
    st.session_state['_scroll_to_top'] = True
    
    # Clear reset flag
    st.session_state['_page_reset_requested'] = False
    if '_force_full_reset' in st.session_state:
        del st.session_state['_force_full_reset']
    
    # Force rerun
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
    
    # ================= Ultimate Bulletproof Version: Separate Component State from Global State =================

    # 1. Initialize a truly safe "behind-the-scenes" global variable
    # (Note: The variable name must start with selected_year to evade the cleanup logic in your _on_page_change)
    if 'selected_year_safe' not in st.session_state:
        if '2025' in year_options:
            st.session_state['selected_year_safe'] = '2025'
        elif '2024' in year_options:
            st.session_state['selected_year_safe'] = '2024'
        elif len(year_options) > 1:
            st.session_state['selected_year_safe'] = year_options[1]
        else:
            st.session_state['selected_year_safe'] = 'All'

    # 2. Fallback protection: Prevent the option from not existing due to switching data files
    if st.session_state['selected_year_safe'] not in year_options:
        st.session_state['selected_year_safe'] = 'All'

    # 3. Dynamically calculate the safe index
    safe_index = year_options.index(st.session_state['selected_year_safe'])

    # 4. Define callback function: Only update the behind-the-scenes variable when the user [manually clicks] the dropdown
    def sync_year():
        st.session_state['selected_year_safe'] = st.session_state['selected_year_widget']

    # 5. Render dropdown: Anchor it using the safe index, use callback to capture changes
    selected_year = st.sidebar.selectbox(
        "Select Period",
        year_options,
        index=safe_index,
        key="selected_year_widget",
        on_change=sync_year
    )

    # 6. Expose the finally selected year to all subpages (maintaining the original variable name)
    st.session_state['selected_year'] = st.session_state['selected_year_safe']
    # =================================================================
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

# Check if page has changed and reset region filter if needed
if 'previous_page' not in st.session_state:
    st.session_state['previous_page'] = selection
    # Force scroll to top on first load
    st.session_state['_scroll_to_top'] = True
elif st.session_state['previous_page'] != selection:
    # Page has changed, reset region filter to "All"
    if 'selected_region' in st.session_state:
        st.session_state['selected_region'] = 'All'
    # Trigger scroll to top when page changes
    st.session_state['_scroll_to_top'] = True
    st.session_state['previous_page'] = selection
    # Force immediate scroll to top with stronger JavaScript
    st.markdown(
        """
        <script>
        (function() {
          function forceScrollToTop() {
            try {
              const doc = window.parent && window.parent.document ? window.parent.document : document;
              // Collect all possible scroll containers including Streamlit view container
              const containers = [
                doc.documentElement,
                doc.body,
                doc.querySelector('[data-testid="stAppViewContainer"]'),
                doc.querySelector('[data-testid="block-container"]'),
                doc.querySelector('section.main'),
                doc.querySelector('.main'),
                doc.querySelector('.block-container')
              ].filter(Boolean);

              // Force scroll behavior to auto and scroll to top
              containers.forEach(el => {
                try { el.style.scrollBehavior = 'auto'; el.scrollTop = 0; } catch (e) {}
              });

              // Also attempt to reset any nested containers that match these selectors
              try {
                doc.querySelectorAll('[data-testid="stAppViewContainer"], [data-testid="block-container"], section.main, .main, .block-container').forEach(el => {
                  try { el.style.scrollBehavior = 'auto'; el.scrollTop = 0; } catch (e) {}
                });
              } catch (e) {}
              
              // Also try window scroll
              try { 
                if (window.parent && window.parent.scrollTo) {
                  window.parent.scrollTo(0, 0);
                } else {
                  window.scrollTo(0, 0);
                }
              } catch (e) {}
            } catch (err) {}
          }
          
          // Execute immediately and also after a short delay
          forceScrollToTop();
          setTimeout(forceScrollToTop, 100);
          setTimeout(forceScrollToTop, 300);
        })();
        </script>
        """,
        unsafe_allow_html=True
    )

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
            
            # Set default value to "All" if not set or if page changed
            if 'selected_region' not in st.session_state:
                st.session_state['selected_region'] = 'All'
                
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
    "🏠 Overview": "Overview",
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
    # Special handling for key pages to ensure scroll to top prior to render
    if selection in ["🔧 Technical Assistance", "🏠 Overview", "📚 Knowledge Development & Dissemination"]:
        # Force scroll to top before calling the page
        st.markdown("""
        <script>
        (function() {
            function forceScrollToTop() {
                try {
                    // Multiple scroll methods
                    try { window.scrollTo({top: 0, behavior: 'instant'}); } catch (e) { try { window.scrollTo(0,0); } catch (e2) {} }
                    try { document.documentElement.scrollTop = 0; } catch (e) {}
                    try { document.body.scrollTop = 0; } catch (e) {}

                    // Find and scroll all possible containers
                    const selectors = [
                        'main', '.main', '.stApp', 
                        '[data-testid="stAppViewContainer"]',
                        '[data-testid="block-container"]',
                        'section.main', '.css-1d391kg'
                    ];

                    selectors.forEach(selector => {
                        try {
                            const elements = document.querySelectorAll(selector);
                            elements.forEach(element => {
                                try { if (element && element.scrollTop !== undefined) { element.style.scrollBehavior = 'auto'; element.scrollTop = 0; } } catch (e) {}
                            });
                        } catch (e) {}
                    });
                } catch (e) {}
            }

            // Execute immediately and with delays
            forceScrollToTop();
            setTimeout(forceScrollToTop, 10);
            setTimeout(forceScrollToTop, 50);
            setTimeout(forceScrollToTop, 100);
        })();
        </script>
        """, unsafe_allow_html=True)

    page.create_layout()
else:
    st.error("The selected page does not have a create_layout function.")

# Re-apply global styles at end so our <style> appears last
try:
    _apply_global_style()
except Exception:
    pass

# Scroll to top after page rendering completes (handle uniformly for all pages)
if st.session_state.get('_scroll_to_top', False):
    import streamlit.components.v1 as components
    components.html(
        """
        <script>
        (function() {
          const MAX_FRAMES = 80;
          let frames = 0;
          try { if ('scrollRestoration' in window.history) window.history.scrollRestoration = 'manual'; } catch (e) {}
          function doScroll() {
            try {
              const doc = window.parent && window.parent.document ? window.parent.document : document;
              const anchor = doc.getElementById('%s');
              if (anchor && typeof anchor.scrollIntoView === 'function') {
                try { anchor.scrollIntoView({ behavior: 'auto', block: 'start', inline: 'nearest' }); } catch (e) {}
              }
              // Collect and reset all common containers, including Streamlit's app view container
              const containers = [
                doc.documentElement,
                doc.body,
                doc.querySelector('[data-testid="stAppViewContainer"]'),
                doc.querySelector('[data-testid="block-container"]'),
                doc.querySelector('section.main'),
                doc.querySelector('.main'),
                doc.querySelector('.block-container')
              ].filter(Boolean);
              containers.forEach(el => { try { el.style.scrollBehavior = 'auto'; el.scrollTop = 0; } catch (e) {} });
              // Also try resetting any additional matches
              try {
                doc.querySelectorAll('[data-testid="stAppViewContainer"], [data-testid="block-container"], section.main, .main, .block-container').forEach(el => {
                  try { el.style.scrollBehavior = 'auto'; el.scrollTop = 0; } catch (e) {}
                });
              } catch (e) {}
              try { (window.parent && window.parent.scrollTo ? window.parent.scrollTo(0, 0) : window.scrollTo(0, 0)); } catch (e) {}
            } catch (err) {}
            if (++frames < MAX_FRAMES) requestAnimationFrame(doScroll);
          }
          requestAnimationFrame(doScroll);
        })();
        </script>
        """ % TOP_ANCHOR_ID,
        height=1,
    )
    st.session_state['_scroll_to_top'] = False


# Fallback: Always ensure page container returns to top after each run (non-intrusive)
st.markdown(
    """
    <script>
      (function(){
        try {
          var doc = window.parent && window.parent.document ? window.parent.document : document;
          try { if ('scrollRestoration' in window.history) window.history.scrollRestoration = 'manual'; } catch (e) {}
          var main = doc.querySelector('section.main') || doc.querySelector('.main') || doc.querySelector('.block-container');
          if (main) { try { main.style.scrollBehavior='auto'; main.scrollTop=0; } catch (e) {} }
          try { doc.documentElement.scrollTop = 0; } catch(e) {}
          try { doc.body.scrollTop = 0; } catch(e) {}
          try { (window.parent && window.parent.scrollTo ? window.parent.scrollTo(0,0) : window.scrollTo(0,0)); } catch(e) {}
        } catch(e) {}
      })();
    </script>
    """,
    unsafe_allow_html=True
)