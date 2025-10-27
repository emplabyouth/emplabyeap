import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import base64
from typing import Dict, Any, List

# Try to import custom styles
try:
    from st_styles import style_manager, create_chart, apply_page_style, create_metrics, create_table, create_standardized_chart
    STYLES_AVAILABLE = True
except ImportError:
    STYLES_AVAILABLE = False

# Standard color palette
STANDARD_COLORS = ['#1E2DBE', '#FA3C4B', '#05D2D2', '#FFCD2D', '#960A55', '#8CE164', '#34495E', '#F1C40F', '#E67E22', '#95A5A6']

def safe_read_csv(file_path: str, **kwargs) -> pd.DataFrame:
    """Safely read CSV file with error handling"""
    try:
        if os.path.exists(file_path):
            return pd.read_csv(file_path, **kwargs)
        else:
            st.warning(f"File not found: {file_path}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading file {file_path}: {str(e)}")
        return pd.DataFrame()

def get_base64_image(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image {image_path}: {str(e)}")
        return None

def create_unified_header():
    """Create unified header for all pages"""
    # Get base64 image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    image_path = os.path.join(project_root, 'orignaldata', 'logo.png')
    
    img_base64 = get_base64_image(image_path)
    
    if img_base64:
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{img_base64}" style="height: 60px; margin-right: 20px;">
            <div>
                <h1 style="margin: 0; color: #1E2DBE;">ILO Youth Employment Action Plan (YEAP)</h1>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title("🎓 ILO Youth Employment Action Plan (YEAP)")
        st.subheader("Capacity Development Dashboard")

    # Add page-specific title and subtitle with blue background
    st.subheader("🎓 Capacity Development")
    st.markdown("""This tab focuses on the ILO's efforts to enhance the **capacity of policymakers, social partners, and other stakeholders** to address youth employment challenges effectively.

Activities reported under this cluster include **training courses, workshops, and seminars** on various aspects of youth employment, such as **policy design, monitoring, and evaluation**.

Outputs also cover the development and dissemination of **training materials, toolkits, and e-learning modules** through platforms like the [ILO's International Training Centre (ITC-ILO)](https://www.itcilo.org/).

**Additional resources:**
- [International Training Centre of the ILO](https://www.itcilo.org/)
- [E-learning platform | ITCILO](https://www.itcilo.org/e-learning)
- [Youth employment courses | ITCILO](https://www.itcilo.org/courses?field_course_topic_target_id_selective=496)""")
    st.markdown("---")

class Q10DataProcessor:
    """Data processor specifically for Q10 (Capacity Development)"""
    
    def __init__(self):
        self.data = None
        self.original_data = None
        self.load__data()
    
    def load_data(self):
        """Load Q10 data"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # Load Q10 data
        q10_file = os.path.join(project_root, 'orignaldata', 'PART3_base_dataQ10.csv')
        
        if os.path.exists(q10_file):
            self.original_data = safe_read_csv(q10_file)
            self.data = self.original_data.copy()
        else:
            st.error(f"Q10 data file not found: {q10_file}")
            self.data = pd.DataFrame()
            self.original_data = pd.DataFrame()
    
    def apply_filters(self, selected_region='All', selected_year='All', filtered_user_ids=None):
        """Apply filters to the data"""
        if self.original_data.empty:
            return
        
        self.data = self.original_data.copy()
        
        # Apply year filter
        if selected_year != 'All':
            if 'YEAR' in self.data.columns:
                self.data = self.data[self.data['YEAR'].astype(str).str.strip() == str(selected_year)]
            elif 'year' in self.data.columns:
                self.data = self.data[self.data['year'].astype(str).str.strip() == str(selected_year)]
        
        # Apply region filter
        if selected_region != 'All':
            if 'Region' in self.data.columns:
                self.data = self.data[self.data['Region'].str.strip() == selected_region]
        
        # Apply user ID filter if provided
        if filtered_user_ids is not None:
            if 'User_ID' in self.data.columns:
                self.data = self.data[self.data['User_ID'].isin(filtered_user_ids)]
    
    def get_field_distribution(self, field_name):
        """Get distribution of values for a specific field"""
        if self.data.empty or field_name not in self.data.columns:
            return {}
        
        # Handle multiple values separated by semicolons
        all_values = []
        for value in self.data[field_name].dropna():
            if pd.isna(value) or str(value).strip() == '':
                continue
            # Split by semicolon and clean up
            values = [v.strip() for v in str(value).split(';') if v.strip()]
            all_values.extend(values)
        
        # Count occurrences
        from collections import Counter
        return dict(Counter(all_values))
    
    def get_works_count_data(self):
        """Get works count data for Q10 - returns dict format compatible with original"""
        if self.data.empty:
            return {}
        
        # Calculate statistics for Q10
        total_works = len(self.data)
        unique_users = self.data['UserId'].nunique() if 'UserId' in self.data.columns else 0
        
        return {
            'Q10': {
                'total_works': total_works,
                'valid_works': total_works,
                'unique_users': unique_users,
                'users_with_works': unique_users,
                'avg_works_per_user': (total_works / unique_users) if unique_users > 0 else 0
            }
        }

def create_theme_count_chart(works_count_data, current_theme=None):
    """Create count chart with transparency effect for non-current themes"""
    if not works_count_data:
        return None
    
    question_labels = {
        'Q6': 'Knowledge development & dissemination',
        'Q7': 'Technical assistance', 
        'Q10': 'Capacity building',
        'Q11': 'Advocacy & partnerships'
    }
    
    # Filter Q6, Q7, Q10, Q11 data (consistent with Dash version)
    all_questions = ['Q6', 'Q7', 'Q10', 'Q11']
    
    # Prepare data - ensure all questions have data, fill with 0 if missing
    questions = all_questions
    question_display_labels = [question_labels.get(q, q) for q in questions]
    unique_users = []
    total_works = []
    
    for q in questions:
        if q in works_count_data:
            unique_users.append(works_count_data[q]['unique_users'])
            total_works.append(works_count_data[q]['valid_works'])
        else:
            unique_users.append(0)
            total_works.append(0)
    
    # Create chart with transparency effect
    colors = STANDARD_COLORS[:2] if not STYLES_AVAILABLE else style_manager.get_chart_colors()[:2]
    
    # Apply transparency to non-current themes
    user_colors = []
    work_colors = []
    
    for i, q in enumerate(questions):
        if current_theme and q != current_theme:
            # Make non-current themes semi-transparent
            user_colors.append(f"rgba({int(colors[0][1:3], 16)}, {int(colors[0][3:5], 16)}, {int(colors[0][5:7], 16)}, 0.3)")
            work_colors.append(f"rgba({int(colors[1][1:3], 16)}, {int(colors[1][3:5], 16)}, {int(colors[1][5:7], 16)}, 0.3)")
        else:
            # Keep current theme fully opaque
            user_colors.append(colors[0])
            work_colors.append(colors[1])
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Number of staff reporting',
        x=question_display_labels,
        y=unique_users,
        marker_color=user_colors,
        hovertemplate='<b>%{x}</b><br>Number of staff reporting: %{y}<extra></extra>',
        hoverlabel=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='rgba(0,0,0,0.2)', font_color='black')
    ))
    fig.add_trace(go.Bar(
        name='Number of outputs delivered',
        x=question_display_labels,
        y=total_works,
        marker_color=work_colors,
        hovertemplate='<b>%{x}</b><br>Number of outputs delivered: %{y}<extra></extra>',
        hoverlabel=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='rgba(0,0,0,0.2)', font_color='black')
    ))
    
    # Create line-wrapped labels
    wrapped_labels = []
    for label in question_display_labels:
        # Split long labels into two lines
        if len(label) > 15:
            words = label.split(' ')
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            wrapped_labels.append(f"{line1}<br>{line2}")
        else:
            wrapped_labels.append(label)
    
    # Apply style configuration
    if STYLES_AVAILABLE:
        layout_config = style_manager.get_global_chart_config('layout').copy()
        # Override margin to ensure enough space for wrapped labels
        layout_config['margin'] = dict(l=40, r=40, t=60, b=120)
        fig.update_layout(
            xaxis_title='',  # Hide x-axis title
            yaxis_title='',  # Hide y-axis title
            barmode='group',
            height=500,
            xaxis=dict(
                tickangle=0,
                tickmode='array',
                tickvals=list(range(len(question_display_labels))),
                ticktext=wrapped_labels,
                tickfont=dict(size=10),
                side='bottom'
            ),
            **layout_config
        )
        # Set chart title under unified style
        fig.update_layout(
            title='Number of Outputs Delivered by Cluster',
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center'
        )
    else:
        fig.update_layout(
            title='Number of Outputs Delivered by Cluster',
            title_font_size=20,
            title_x=0.5,
            title_xanchor='center',
            xaxis_title='',  # Hide x-axis title
            yaxis_title='',  # Hide y-axis title
            barmode='group',
            height=500,
            margin=dict(b=120),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_family="Noto Sans",
            xaxis=dict(
                tickangle=0,
                tickmode='array',
                tickvals=list(range(len(question_display_labels))),
                ticktext=wrapped_labels,
                tickfont=dict(size=10),
                side='bottom'
            )
        )
    
    return fig

def create_theme_detail_list(data_processor):
    """Create detailed list for Q10"""
    if data_processor.data.empty:
        return None
    
    df = data_processor.data.copy()
    
    # Select relevant columns for display
    display_columns = []
    available_columns = df.columns.tolist()
    
    # Common columns to display
    preferred_columns = [
        'User_ID', 'YEAR', 'Region', 'Country', 
        'Q10_1_Capacity_building_type', 'Q10_2_Capacity_building_title',
        'Q10_3_Capacity_building_description', 'Q10_4_Capacity_building_beneficiaries',
        'Q10_5_Capacity_building_partners'
    ]
    
    for col in preferred_columns:
        if col in available_columns:
            display_columns.append(col)
    
    # Add any remaining columns
    for col in available_columns:
        if col not in display_columns:
            display_columns.append(col)
    
    return df[display_columns]

def create_layout():
    """Create the main Streamlit layout for Q10"""
    # Add unified header first
    create_unified_header()
    
    # Apply page styles
    if STYLES_AVAILABLE:
        apply_page_style()
    else:
        st.set_page_config(
            page_title="ILO YEAP - Capacity Development",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    # Initialize data processor
    data_processor = Q10DataProcessor()
    
    # Apply filters if they exist in session state
    selected_region = st.session_state.get('selected_region', 'All')
    selected_year = st.session_state.get('selected_year', 'All')
    filtered_user_ids = st.session_state.get('filtered_user_ids', None)
    
    data_processor.apply_filters(selected_region, selected_year, filtered_user_ids)
    
    # Check if data is available
    if data_processor.data.empty:
        st.warning("No data available for Capacity Development with current filters.")
        return
    
    # Section 1: Count Statistics
    st.subheader("📊 Clusters Of The Implementation Framework")
    works_count_data = data_processor.get_works_count_data()
    
    if works_count_data:
        count_fig = create_theme_count_chart(works_count_data, current_theme="Q10")
        if count_fig:
            st.plotly_chart(count_fig, width='stretch')
    else:
        st.info("No output count data available with current filters.")
    
    st.markdown("---")
    
    # Section 2: Frequency Analysis
    st.subheader("📊 Frequency Analysis")
    
    # Define Q10-specific charts based on original themes configuration
    q10_charts = [
        ('Funding source (Options: regular budget or extrabudgetary)', 'pie', 'Funding Source Of Capacity Building Outputs'),
        ('Focus (Options: Youth only or Youth is one of the target groups)', 'pie', 'Target Group Of Capacity Building Outputs'),
        ('Type of capacity building (Options: Training, or Workshop, or Seminar)', 'bar', 'Types Of Capacity Building Delivered')
    ]
    
    has_frequency_data = False
    for field_name, chart_type, chart_title in q10_charts:
        field_data = data_processor.get_field_distribution(field_name)
        if field_data:
            has_frequency_data = True
            
            fig = create_chart(pd.Series(field_data), chart_type, chart_title)
            st.plotly_chart(fig, use_container_width=True)
    
    if not has_frequency_data:
        st.info("No frequency analysis data available with current filters.")
    
    # Section 3: Outputs Detail List
    st.subheader("📋 Outputs Detail List")
    
    detail_df = create_theme_detail_list(data_processor)
    if detail_df is not None and not detail_df.empty:
        total_records = len(detail_df)
        
        # Initialize session state for current page if not exists
        page_key = 'q10_current_page'
        if page_key not in st.session_state:
            st.session_state[page_key] = 1
        
        # Get current page data
        items_per_page = st.session_state.get('q10_items_per_page', 50)
        total_pages = (total_records - 1) // items_per_page + 1
        
        # Calculate display range
        start_idx = (st.session_state[page_key] - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_records)
        
        # Get current page data
        display_df = detail_df.iloc[start_idx:end_idx].copy()
        
        st.dataframe(display_df, width='stretch')
        
        # Compact pagination controls
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Page info
        st.markdown(
            f"<div style='text-align: center; margin: 10px 0;'>"
            f"<strong>Page {st.session_state[page_key]} of {total_pages}</strong> | "
            f"Showing {start_idx + 1}-{end_idx} of {total_records} records"
            f"</div>", 
            unsafe_allow_html=True
        )
        
        # Controls
        control_col1, control_col2 = st.columns([1, 1])
        
        with control_col1:
            # Items per page
            new_items_per_page = st.selectbox(
                "Items per page:",
                options=[10, 25, 50, 100, 200],
                index=[10, 25, 50, 100, 200].index(items_per_page) if items_per_page in [10, 25, 50, 100, 200] else 2,
                key="q10_items_per_page_select"
            )
            
            if new_items_per_page != items_per_page:
                st.session_state.q10_items_per_page = new_items_per_page
                st.session_state[page_key] = 1
                st.rerun()
        
        with control_col2:
            # Jump to page
            new_page = st.number_input(
                "Jump to page:",
                min_value=1,
                max_value=total_pages,
                value=st.session_state[page_key],
                key="q10_page_input"
            )
            if new_page != st.session_state[page_key]:
                st.session_state[page_key] = new_page
                st.rerun()
    else:
        st.info("No detail data available with current filters.")

if __name__ == "__main__":
    create_layout()