import streamlit as st
import os
import base64
import pandas as pd
import plotly.graph_objects as go

# Try to apply unified  page  style if available
try:
    from st_styles import apply_page_style, create_chart
    STYLES_AVAILABLE = True
except Exception:
    STYLES_AVAILABLE = False


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


def get_q2_data():
    """Load Q2 data from PART1_base_dataQ2-5.csv"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        csv_path = os.path.join(project_root, 'orignaldata', 'PART1_base_dataQ2-5.csv')
        
        if os.path.exists(csv_path):
            df = safe_read_csv(csv_path)
            
            # Apply global YEAR filter if available
            try:
                selected_year = st.session_state.get('selected_year', 'All')
                if selected_year != 'All':
                    # Check for both 'YEAR' and 'year' columns
                    if 'YEAR' in df.columns:
                        df = df[df['YEAR'].astype(str).str.strip() == str(selected_year)]
                    elif 'year' in df.columns:
                        df = df[df['year'].astype(str).str.strip() == str(selected_year)]
            except Exception:
                pass
            
            # Filter Q2 data
            q2_data = df[df['question'].str.contains('Q2:', na=False)]
            
            # Create data dictionary for chart
            data_dict = {}
            for _, row in q2_data.iterrows():
                option = str(row['option']).strip()
                count = int(row['count']) if pd.notna(row['count']) else 0
                data_dict[option] = count
            
            return data_dict
        else:
            return {}
    except Exception as e:
        st.error(f"Error loading Q2 data: {e}")
        return {}


def create_q2_chart(data):
    """Create Q2 pie chart with specified title"""
    if not data:
        return None
    
    title = "Distribution of Responses on Whether Entities Conducted Youth Employment Work in the Reference Period"
    
    if STYLES_AVAILABLE:
        try:
            return create_chart(data, 'pie', title)
        except Exception:
            pass
    
    # Fallback chart creation
    fig = go.Figure()
    
    categories = list(data.keys())
    values = list(data.values())
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    
    fig.add_trace(go.Pie(
        labels=categories,
        values=values,
        marker_colors=colors[:len(categories)],
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 14},
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'pad': {'b': 10}
        },
        height=400,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font_family="Noto Sans",
        margin=dict(t=60, b=20, l=20, r=20),
        autosize=True
    )
    
    return fig


def get_q345_data():
    """Load and process Q3, Q4, Q5 data to create summary table, separated by Department and Region"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # Load data files
        q3_path = os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ3.csv')
        q4_path = os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ4.csv')
        q5_path = os.path.join(project_root, 'orignaldata', 'PART2_base_dataQ5.csv')
        
        # Initialize result dictionaries for departments and regions
        department_data = {}
        region_data = {}
        
        # Process Q3 data
        if os.path.exists(q3_path):
            df_q3 = safe_read_csv(q3_path)
            
            # Apply global YEAR filter if available
            try:
                selected_year = st.session_state.get('selected_year', 'All')
                if selected_year != 'All':
                    # Check for both 'YEAR' and 'year' columns
                    if 'YEAR' in df_q3.columns:
                        df_q3 = df_q3[df_q3['YEAR'].astype(str).str.strip() == str(selected_year)]
                    elif 'year' in df_q3.columns:
                        df_q3 = df_q3[df_q3['year'].astype(str).str.strip() == str(selected_year)]
            except Exception:
                pass
            
            # Get unique departments and regions
            all_entities = df_q3['Department/Region'].dropna().unique()
            departments = [entity for entity in all_entities if not entity.startswith('Region:')]
            regions = [entity for entity in all_entities if entity.startswith('Region:')]
            
            # Initialize departments and regions in result_data
            for dept in departments:
                if dept not in department_data:
                    department_data[dept] = {}
            for region in regions:
                if region not in region_data:
                    region_data[region] = {}
            
            q3_columns = [col for col in df_q3.columns if col not in ['UserId', 'Department/Region', 'year']]
            
            # Group by department and check for YES values
            for dept in departments:
                dept_data = df_q3[df_q3['Department/Region'] == dept]
                for col in q3_columns:
                    col_key = f"Q3_{col.strip()}"
                    # Check if any row for this department has YES for this column
                    has_yes = (dept_data[col].fillna('').str.upper() == 'YES').any()
                    department_data[dept][col_key] = "Yes" if has_yes else ""
            
            # Group by region and check for YES values
            for region in regions:
                region_data_df = df_q3[df_q3['Department/Region'] == region]
                for col in q3_columns:
                    col_key = f"Q3_{col.strip()}"
                    # Check if any row for this region has YES for this column
                    has_yes = (region_data_df[col].fillna('').str.upper() == 'YES').any()
                    region_data[region][col_key] = "Yes" if has_yes else ""
        
        # Process Q4 data
        if os.path.exists(q4_path):
            df_q4 = safe_read_csv(q4_path)
            
            # Apply global YEAR filter if available
            try:
                selected_year = st.session_state.get('selected_year', 'All')
                if selected_year != 'All':
                    # Check for both 'YEAR' and 'year' columns
                    if 'YEAR' in df_q4.columns:
                        df_q4 = df_q4[df_q4['YEAR'].astype(str).str.strip() == str(selected_year)]
                    elif 'year' in df_q4.columns:
                        df_q4 = df_q4[df_q4['year'].astype(str).str.strip() == str(selected_year)]
            except Exception:
                pass
            
            all_entities = df_q4['Department/Region'].dropna().unique()
            departments = [entity for entity in all_entities if not entity.startswith('Region:')]
            regions = [entity for entity in all_entities if entity.startswith('Region:')]
            
            # Initialize departments and regions in result_data
            for dept in departments:
                if dept not in department_data:
                    department_data[dept] = {}
            for region in regions:
                if region not in region_data:
                    region_data[region] = {}
            
            q4_columns = [col for col in df_q4.columns if col not in ['UserId', 'Department/Region', 'year', 'Other', 'Other (elaborated answ)']]
            
            # Group by department and check for YES values
            for dept in departments:
                dept_data = df_q4[df_q4['Department/Region'] == dept]
                for col in q4_columns:
                    col_key = f"Q4_{col.strip()}"
                    # Check if any row for this department has YES for this column
                    has_yes = (dept_data[col].fillna('').str.upper() == 'YES').any()
                    department_data[dept][col_key] = "Yes" if has_yes else ""
            
            # Group by region and check for YES values
            for region in regions:
                region_data_df = df_q4[df_q4['Department/Region'] == region]
                for col in q4_columns:
                    col_key = f"Q4_{col.strip()}"
                    # Check if any row for this region has YES for this column
                    has_yes = (region_data_df[col].fillna('').str.upper() == 'YES').any()
                    region_data[region][col_key] = "Yes" if has_yes else ""
        
        # Process Q5 data
        if os.path.exists(q5_path):
            df_q5 = safe_read_csv(q5_path)
            
            # Apply global YEAR filter if available
            try:
                selected_year = st.session_state.get('selected_year', 'All')
                if selected_year != 'All':
                    # Check for both 'YEAR' and 'year' columns
                    if 'YEAR' in df_q5.columns:
                        df_q5 = df_q5[df_q5['YEAR'].astype(str).str.strip() == str(selected_year)]
                    elif 'year' in df_q5.columns:
                        df_q5 = df_q5[df_q5['year'].astype(str).str.strip() == str(selected_year)]
            except Exception:
                pass
            
            all_entities = df_q5['Department/Region'].dropna().unique()
            departments = [entity for entity in all_entities if not entity.startswith('Region:')]
            regions = [entity for entity in all_entities if entity.startswith('Region:')]
            
            # Initialize departments and regions in result_data
            for dept in departments:
                if dept not in department_data:
                    department_data[dept] = {}
            for region in regions:
                if region not in region_data:
                    region_data[region] = {}
            
            q5_columns = [col for col in df_q5.columns if col not in ['UserId', 'Department/Region', 'year', 'Other', 'Other (elaborated answ)']]
            
            # Group by department and check for YES values
            for dept in departments:
                dept_data = df_q5[df_q5['Department/Region'] == dept]
                for col in q5_columns:
                    col_key = f"Q5_{col.strip()}"
                    # Check if any row for this department has YES for this column
                    has_yes = (dept_data[col].fillna('').str.upper() == 'YES').any()
                    department_data[dept][col_key] = "Yes" if has_yes else ""
            
            # Group by region and check for YES values
            for region in regions:
                region_data_df = df_q5[df_q5['Department/Region'] == region]
                for col in q5_columns:
                    col_key = f"Q5_{col.strip()}"
                    # Check if any row for this region has YES for this column
                    has_yes = (region_data_df[col].fillna('').str.upper() == 'YES').any()
                    region_data[region][col_key] = "Yes" if has_yes else ""
        
        return {'departments': department_data, 'regions': region_data}
        
    except Exception as e:
        st.error(f"Error loading Q3-Q4-Q5 data: {e}")
        return {'departments': {}, 'regions': {}}


def create_q345_table(data):
    """Create a formatted table for Q3-Q4-Q5 data"""
    if not data:
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.fillna("")
    
    # Reset index to make Department/Region a column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Department/Region'}, inplace=True)
    
    # Reorder columns to match the sample format
    q3_cols = [col for col in df.columns if col.startswith('Q3_')]
    q4_cols = [col for col in df.columns if col.startswith('Q4_')]
    q5_cols = [col for col in df.columns if col.startswith('Q5_')]
    
    # Create column order
    column_order = ['Department/Region'] + q3_cols + q4_cols + q5_cols
    df = df.reindex(columns=column_order)
    
    # Create proper column headers with question titles
    display_columns = ['Department/Region']
    
    # Add Q3 title row
    if q3_cols:
        display_columns.append('Entities\' Work Across The Clusters Of The Implementation Framework')
        # Add empty columns for Q3 options (except the first one which has the title)
        for i in range(len(q3_cols) - 1):
            display_columns.append('')
    
    # Add Q4 title row  
    if q4_cols:
        display_columns.append('Entities\' Work Across The Pillars Of The Call For Action On Youth Employment')
        # Add empty columns for Q4 options (except the first one which has the title)
        for i in range(len(q4_cols) - 1):
            display_columns.append('')
    
    # Add Q5 title row
    if q5_cols:
        display_columns.append('Entities\' Work Across Target Youth Groups, When Applicable')
        # Add empty columns for Q5 options (except the first one which has the title)
        for i in range(len(q5_cols) - 1):
            display_columns.append('')
    
    # Create a multi-level header structure
    # First create the title row
    title_row = [''] + ['Entities\' Work Across The Clusters Of The Implementation Framework'] * len(q3_cols) + \
                ['Entities\' Work Across The Pillars Of The Call For Action On Youth Employment'] * len(q4_cols) + \
                ['Entities\' Work Across Target Youth Groups, When Applicable'] * len(q5_cols)
    
    # Create option row (clean column names for display)
    option_row = ['Department/Region']
    for col in df.columns[1:]:
        if col.startswith('Q3_'):
            option_row.append(col.replace('Q3_', '').strip())
        elif col.startswith('Q4_'):
            option_row.append(col.replace('Q4_', '').strip())
        elif col.startswith('Q5_'):
            option_row.append(col.replace('Q5_', '').strip())
        else:
            option_row.append(col)
    
    # Create a new DataFrame with proper structure
    result_df = df.copy()
    result_df.columns = option_row
    
    # Add title information as metadata (we'll display it separately)
    result_df.attrs['q3_title'] = 'Entities\' Work Across The Clusters Of The Implementation Framework'
    result_df.attrs['q4_title'] = 'Entities\' Work Across The Pillars Of The Call For Action On Youth Employment'
    result_df.attrs['q5_title'] = 'Entities\' Work Across Target Youth Groups, When Applicable'
    result_df.attrs['q3_cols'] = len(q3_cols)
    result_df.attrs['q4_cols'] = len(q4_cols)
    result_df.attrs['q5_cols'] = len(q5_cols)
    
    return result_df


def create_department_table_transposed(data):
    """Create a transposed formatted table for Q3-Q4-Q5 Department data"""
    if not data:
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.fillna("")
    
    # Reset index to make Department a column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Department'}, inplace=True)
    
    # Reorder columns to match the sample format
    q3_cols = [col for col in df.columns if col.startswith('Q3_')]
    q4_cols = [col for col in df.columns if col.startswith('Q4_')]
    q5_cols = [col for col in df.columns if col.startswith('Q5_')]
    
    # Create column order
    column_order = ['Department'] + q3_cols + q4_cols + q5_cols
    df = df.reindex(columns=column_order)
    
    # Set Department as index for transposition
    df.set_index('Department', inplace=True)
    
    # Transpose the DataFrame
    transposed_df = df.T
    
    # Create option column (clean row names for display)
    option_names = []
    for idx in transposed_df.index:
        if idx.startswith('Q3_'):
            option_names.append(idx.replace('Q3_', '').strip())
        elif idx.startswith('Q4_'):
            option_names.append(idx.replace('Q4_', '').strip())
        elif idx.startswith('Q5_'):
            option_names.append(idx.replace('Q5_', '').strip())
        else:
            option_names.append(idx)
    
    # Reset index and add option column
    transposed_df.reset_index(inplace=True)
    transposed_df.insert(0, 'Option', option_names)
    transposed_df.drop(columns=['index'], inplace=True)
    
    # Add title information as metadata
    transposed_df.attrs['q3_title'] = 'Entities\' Work Across The Clusters Of The Implementation Framework'
    transposed_df.attrs['q4_title'] = 'Entities\' Work Across The Pillars Of The Call For Action On Youth Employment'
    transposed_df.attrs['q5_title'] = 'Entities\' Work Across Target Youth Groups, When Applicable'
    transposed_df.attrs['q3_cols'] = len(q3_cols)
    transposed_df.attrs['q4_cols'] = len(q4_cols)
    transposed_df.attrs['q5_cols'] = len(q5_cols)
    
    return transposed_df


def create_department_table(data):
    """Create a formatted table for Q3-Q4-Q5 Department data"""
    if not data:
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.fillna("")
    
    # Reset index to make Department a column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Department'}, inplace=True)
    
    # Reorder columns to match the sample format
    q3_cols = [col for col in df.columns if col.startswith('Q3_')]
    q4_cols = [col for col in df.columns if col.startswith('Q4_')]
    q5_cols = [col for col in df.columns if col.startswith('Q5_')]
    
    # Create column order
    column_order = ['Department'] + q3_cols + q4_cols + q5_cols
    df = df.reindex(columns=column_order)
    
    # Create option row (clean column names for display)
    option_row = ['Department']
    for col in df.columns[1:]:
        if col.startswith('Q3_'):
            option_row.append(col.replace('Q3_', '').strip())
        elif col.startswith('Q4_'):
            option_row.append(col.replace('Q4_', '').strip())
        elif col.startswith('Q5_'):
            option_row.append(col.replace('Q5_', '').strip())
        else:
            option_row.append(col)
    
    # Create a new DataFrame with proper structure
    result_df = df.copy()
    result_df.columns = option_row
    
    # Add title information as metadata
    result_df.attrs['q3_title'] = 'Entities\' Work Across The Clusters Of The Implementation Framework'
    result_df.attrs['q4_title'] = 'Entities\' Work Across The Pillars Of The Call For Action On Youth Employment'
    result_df.attrs['q5_title'] = 'Entities\' Work Across Target Youth Groups, When Applicable'
    result_df.attrs['q3_cols'] = len(q3_cols)
    result_df.attrs['q4_cols'] = len(q4_cols)
    result_df.attrs['q5_cols'] = len(q5_cols)
    
    return result_df


def create_region_table_transposed(data):
    """Create a transposed formatted table for Q3-Q4-Q5 Region data"""
    if not data:
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.fillna("")
    
    # Reset index to make Region a column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Region'}, inplace=True)
    
    # Reorder columns to match the sample format
    q3_cols = [col for col in df.columns if col.startswith('Q3_')]
    q4_cols = [col for col in df.columns if col.startswith('Q4_')]
    q5_cols = [col for col in df.columns if col.startswith('Q5_')]
    
    # Create column order
    column_order = ['Region'] + q3_cols + q4_cols + q5_cols
    df = df.reindex(columns=column_order)
    
    # Set Region as index for transposition
    df.set_index('Region', inplace=True)
    
    # Transpose the DataFrame
    transposed_df = df.T
    
    # Create option column (clean row names for display)
    option_names = []
    for idx in transposed_df.index:
        if idx.startswith('Q3_'):
            option_names.append(idx.replace('Q3_', '').strip())
        elif idx.startswith('Q4_'):
            option_names.append(idx.replace('Q4_', '').strip())
        elif idx.startswith('Q5_'):
            option_names.append(idx.replace('Q5_', '').strip())
        else:
            option_names.append(idx)
    
    # Reset index and add option column
    transposed_df.reset_index(inplace=True)
    transposed_df.insert(0, 'Option', option_names)
    transposed_df.drop(columns=['index'], inplace=True)
    
    # Add title information as metadata
    transposed_df.attrs['q3_title'] = 'Entities\' Work Across The Clusters Of The Implementation Framework'
    transposed_df.attrs['q4_title'] = 'Entities\' Work Across The Pillars Of The Call For Action On Youth Employment'
    transposed_df.attrs['q5_title'] = 'Entities\' Work Across Target Youth Groups, When Applicable'
    transposed_df.attrs['q3_cols'] = len(q3_cols)
    transposed_df.attrs['q4_cols'] = len(q4_cols)
    transposed_df.attrs['q5_cols'] = len(q5_cols)
    
    return transposed_df


def create_region_table(data):
    """Create a formatted table for Q3-Q4-Q5 Region data"""
    if not data:
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.fillna("")
    
    # Reset index to make Region a column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Region'}, inplace=True)
    
    # Reorder columns to match the sample format
    q3_cols = [col for col in df.columns if col.startswith('Q3_')]
    q4_cols = [col for col in df.columns if col.startswith('Q4_')]
    q5_cols = [col for col in df.columns if col.startswith('Q5_')]
    
    # Create column order
    column_order = ['Region'] + q3_cols + q4_cols + q5_cols
    df = df.reindex(columns=column_order)
    
    # Create option row (clean column names for display)
    option_row = ['Region']
    for col in df.columns[1:]:
        if col.startswith('Q3_'):
            option_row.append(col.replace('Q3_', '').strip())
        elif col.startswith('Q4_'):
            option_row.append(col.replace('Q4_', '').strip())
        elif col.startswith('Q5_'):
            option_row.append(col.replace('Q5_', '').strip())
        else:
            option_row.append(col)
    
    # Create a new DataFrame with proper structure
    result_df = df.copy()
    result_df.columns = option_row
    
    # Add title information as metadata
    result_df.attrs['q3_title'] = 'Entities\' Work Across The Clusters Of The Implementation Framework'
    result_df.attrs['q4_title'] = 'Entities\' Work Across The Pillars Of The Call For Action On Youth Employment'
    result_df.attrs['q5_title'] = 'Entities\' Work Across Target Youth Groups, When Applicable'
    result_df.attrs['q3_cols'] = len(q3_cols)
    result_df.attrs['q4_cols'] = len(q4_cols)
    result_df.attrs['q5_cols'] = len(q5_cols)
    
    return result_df


def create_html_table_with_headers(df, original_data, table_type="Department"):
    """Create HTML table with merged header cells for Q3, Q4, Q5 sections"""
    
    # Identify Q3, Q4, Q5 columns based on original data structure
    all_columns = df.columns.tolist()
    dept_col = table_type  # Use table_type as the first column name
    data_columns = [col for col in all_columns if col != dept_col]
    
    # Get sample original data to identify column types
    sample_orig_keys = list(original_data[list(original_data.keys())[0]].keys())
    
    q3_cols = []
    q4_cols = []
    q5_cols = []
    
    for col in data_columns:
        # Check if this column corresponds to Q3, Q4, or Q5 in original data
        for orig_key in sample_orig_keys:
            if orig_key.startswith('Q3_') and orig_key.replace('Q3_', '').strip() == col:
                q3_cols.append(col)
                break
            elif orig_key.startswith('Q4_') and orig_key.replace('Q4_', '').strip() == col:
                q4_cols.append(col)
                break
            elif orig_key.startswith('Q5_') and orig_key.replace('Q5_', '').strip() == col:
                q5_cols.append(col)
                break
    
    # Count columns for each section
    q3_count = len(q3_cols)
    q4_count = len(q4_cols)
    q5_count = len(q5_cols)
    
    # Start building HTML table
    html = f"""
    <style>
    .q345-table-{table_type.lower()} {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        font-family: 'Noto Sans', 'Noto Sans SC', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-size: 13px;
        table-layout: fixed;
    }}
    .q345-table-{table_type.lower()} th, .q345-table-{table_type.lower()} td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
        vertical-align: middle;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }}
    .q345-table-{table_type.lower()} th {{
        background-color: #f2f2f2;
        font-weight: bold;
    }}
    .q345-table-{table_type.lower()} .title-header {{
        background-color: #e6f3ff;
        font-weight: bold;
        text-align: center;
        font-size: 12px;
        padding: 6px;
    }}
    .q345-table-{table_type.lower()} .dept-col {{
        background-color: #f9f9f9;
        font-weight: normal;
        width: 120px;
        min-width: 120px;
        max-width: 120px;
        font-size: 10px !important;
        line-height: 1.2;
    }}
    .q345-table-{table_type.lower()} td.dept-col {{
        font-size: 12px !important;
        font-weight: normal;
    }}
    .q345-table-{table_type.lower()} .dept-header {{
        background-color: #f9f9f9;
        font-weight: bold;
        width: 120px;
        min-width: 120px;
        max-width: 120px;
        font-size: 13px;
        text-align: center;
        vertical-align: middle !important;
        white-space: normal;
        word-break: keep-all;
        line-height: 1.3;
        padding: 6px;
    }}
    .q345-table-{table_type.lower()} .dept-header-inner {{
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        width: 100%;
    }}
    .q345-table-{table_type.lower()} .option-header {{
        background-color: #f8f8f8;
        font-size: 11px;
        text-align: center;
        padding: 6px;
        width: 100px;
        min-width: 100px;
        max-width: 100px;
    }}
    .q345-table-{table_type.lower()} .data-cell {{
        text-align: center;
        font-size: 12px;
        width: 100px;
        min-width: 100px;
        max-width: 100px;
    }}
    .q345-table-{table_type.lower()} .percentage-row {{
        background-color: #f0f8ff;
        font-weight: bold;
        font-style: italic;
    }}
    .q345-table-{table_type.lower()} .percentage-cell {{
        text-align: center;
        font-size: 12px;
        font-weight: bold;
        background-color: #f0f8ff;
        color: #0066cc;
    }}
    </style>
    <table class="q345-table-{table_type.lower()} summary-table">
    """
    
    # Create title header row
    html += "<tr>"
    # Wrap header content in an inner flex container to ensure vertical centering across rowspan
    html += f'<th class="dept-header" rowspan="2"><div class="dept-header-inner">{table_type}</div></th>'
    
    if q3_count > 0:
        html += f'<th class="title-header" colspan="{q3_count}">Entities\' Work Across The Clusters Of The Implementation Framework</th>'
    
    if q4_count > 0:
        html += f'<th class="title-header" colspan="{q4_count}">Entities\' Work Across The Pillars Of The Call For Action On Youth Employment</th>'
    
    if q5_count > 0:
        html += f'<th class="title-header" colspan="{q5_count}">Entities\' Work Across Target Youth Groups, When Applicable</th>'
    
    html += "</tr>"
    
    # Create column header row
    html += "<tr>"
    
    # Add Q3 column headers
    for col in q3_cols:
        html += f'<th class="option-header">{col}</th>'
    
    # Add Q4 column headers
    for col in q4_cols:
        html += f'<th class="option-header">{col}</th>'
    
    # Add Q5 column headers
    for col in q5_cols:
        html += f'<th class="option-header">{col}</th>'
    
    html += "</tr>"
    
    # Add data rows
    for _, row in df.iterrows():
        html += "<tr>"
        html += f'<td class="dept-col">{row[dept_col]}</td>'
        
        # Add Q3 data
        for col in q3_cols:
            value = row[col] if col in row else ""
            # Only show ○ for Yes values, empty for others
            if value == "Yes":
                display_value = "○"
            else:
                display_value = ""  # No and empty values show as empty
            html += f'<td class="data-cell symbol-cell">{display_value}</td>'
        
        # Add Q4 data
        for col in q4_cols:
            value = row[col] if col in row else ""
            # Only show ○ for Yes values, empty for others
            if value == "Yes":
                display_value = "○"
            else:
                display_value = ""  # No and empty values show as empty
            html += f'<td class="data-cell symbol-cell">{display_value}</td>'
        
        # Add Q5 data
        for col in q5_cols:
            value = row[col] if col in row else ""
            # Only show ○ for Yes values, empty for others
            if value == "Yes":
                display_value = "○"
            else:
                display_value = ""  # No and empty values show as empty
            html += f'<td class="data-cell symbol-cell">{display_value}</td>'
        
        html += "</tr>"
    
    # Add percentage statistics row
    html += '<tr class="percentage-row">'
    html += '<td class="dept-col">Coverage Rate</td>'
    
    # Calculate and add Q3 percentages (only count Q3 rows)
    q3_total_count = len(q3_cols)
    for col in q3_cols:
        yes_count = len(df[df[col] == "Yes"])
        percentage = round((yes_count / q3_total_count * 100), 1) if q3_total_count > 0 else 0
        html += f'<td class="percentage-cell">{percentage}%</td>'
    
    # Calculate and add Q4 percentages (only count Q4 rows)
    q4_total_count = len(q4_cols)
    for col in q4_cols:
        yes_count = len(df[df[col] == "Yes"])
        percentage = round((yes_count / q4_total_count * 100), 1) if q4_total_count > 0 else 0
        html += f'<td class="percentage-cell">{percentage}%</td>'
    
    # Calculate and add Q5 percentages (only count Q5 rows)
    q5_total_count = len(q5_cols)
    for col in q5_cols:
        yes_count = len(df[df[col] == "Yes"])
        percentage = round((yes_count / q5_total_count * 100), 1) if q5_total_count > 0 else 0
        html += f'<td class="percentage-cell">{percentage}%</td>'
    
    html += "</tr>"
    
    html += "</table>"
    
    return html


def create_html_table_with_headers_transposed(df, original_data, table_type="Department"):
    """Create transposed HTML table with section titles on left and Coverage Rate column on right"""
    
    # For transposed table, the first column is "Option" and other columns are departments/regions
    all_columns = df.columns.tolist()
    option_col = "Option"
    entity_columns = [col for col in all_columns if col != option_col]
    
    # Get sample original data to identify row types
    sample_orig_keys = list(original_data[list(original_data.keys())[0]].keys())
    
    # Identify Q3, Q4, Q5 rows based on the Option column values
    q3_rows = []
    q4_rows = []
    q5_rows = []
    
    for idx, row in df.iterrows():
        option_value = row[option_col]
        # Check if this option corresponds to Q3, Q4, or Q5 in original data
        for orig_key in sample_orig_keys:
            if orig_key.startswith('Q3_') and orig_key.replace('Q3_', '').strip() == option_value:
                q3_rows.append(idx)
                break
            elif orig_key.startswith('Q4_') and orig_key.replace('Q4_', '').strip() == option_value:
                q4_rows.append(idx)
                break
            elif orig_key.startswith('Q5_') and orig_key.replace('Q5_', '').strip() == option_value:
                q5_rows.append(idx)
                break
    
    # Count rows for each section
    q3_count = len(q3_rows)
    q4_count = len(q4_rows)
    q5_count = len(q5_rows)
    
    # Define section titles with line breaks for better readability
    q3_title = "Entities' Work Across<br>The Clusters Of The<br>Implementation Framework"
    q4_title = "Entities' Work Across<br>The Pillars Of The Call<br>For Action On Youth<br>Employment"
    q5_title = "Entities' Work Across<br>Target Youth Groups,<br>When Applicable"
    
    # Start building HTML table
    html = f"""
    <style>
    .q345-table-transposed {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        font-family: 'Noto Sans', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
        table-layout: fixed;
    }}
    .q345-table-transposed th, .q345-table-transposed td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
        vertical-align: middle;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }}
    .q345-table-transposed th {{
        background-color: #f2f2f2;
        font-weight: bold;
    }}
    .q345-table-transposed .section-title {{
        background-color: #e6f3ff;
        font-weight: bold;
        text-align: center;
        font-size: 11px;
        padding: 8px;
        writing-mode: horizontal-tb;
        text-orientation: upright;
        width: 120px;
        min-width: 110px;
        max-width: 130px;
        line-height: 1.3;
        word-break: break-word;
        overflow: hidden;
        vertical-align: middle;
    }}
    .q345-table-transposed .option-col {{
        background-color: #f9f9f9;
        font-weight: normal;
        width: 200px;
        min-width: 180px;
        max-width: 220px;
        font-size: 11px !important;
        line-height: 1.2;
    }}
    .q345-table-transposed .option-header {{
        background-color: #f9f9f9;
        font-weight: bold;
        width: 200px;
        min-width: 180px;
        max-width: 220px;
        font-size: 13px;
        text-align: center;
        vertical-align: middle !important;
        white-space: normal;
        word-break: keep-all;
        line-height: 1.3;
        padding: 6px;
    }}
    .q345-table-transposed .entity-header {{
        background-color: #f8f8f8;
        font-size: 11px;
        text-align: center;
        padding: 6px;
        width: 120px;
        min-width: 110px;
        max-width: 130px;
    }}
    .q345-table-transposed .coverage-header {{
        background-color: #f0f8ff;
        font-size: 11px;
        text-align: center;
        padding: 6px;
        width: 120px;
        min-width: 110px;
        max-width: 130px;
        font-weight: bold;
        color: #0066cc;
    }}
    .q345-table-transposed .data-cell {{
        text-align: center;
        font-size: 12px;
        width: 120px;
        min-width: 110px;
        max-width: 130px;
    }}
    .q345-table-transposed .coverage-cell {{
        text-align: center;
        font-size: 12px;
        font-weight: bold;
        background-color: #f0f8ff;
        color: #0066cc;
        width: 120px;
        min-width: 110px;
        max-width: 130px;
    }}
    .q345-table-transposed .percentage-row {{
        background-color: #f0f8ff;
        font-weight: bold;
        font-style: italic;
    }}
    .q345-table-transposed .percentage-cell {{
        text-align: center;
        font-size: 12px;
        font-weight: bold;
        background-color: #f0f8ff;
        color: #0066cc;
    }}
    </style>
    <table class="q345-table-transposed summary-table">
    """
    
    # Create header row
    html += "<tr>"
    
    # Add section title column header (empty for header row)
    html += '<th class="section-title"></th>'
    
    # Add Option column header
    html += f'<th class="option-header">Option</th>'
    
    # Add entity column headers
    for entity in entity_columns:
        html += f'<th class="entity-header">{entity}</th>'
    
    # Add Coverage Rate column header
    html += '<th class="coverage-header">Coverage Rate</th>'
    
    html += "</tr>"
    
    # Add Q3 section
    if q3_count > 0:
        for i, idx in enumerate(q3_rows):
            row = df.iloc[idx]
            html += "<tr>"
            
            # Add section title for first row of Q3
            if i == 0:
                html += f'<td class="section-title" rowspan="{q3_count}">{q3_title}</td>'
            
            # Add option
            html += f'<td class="option-col">{row[option_col]}</td>'
            
            # Add entity data
            yes_count = 0
            for entity in entity_columns:
                value = row[entity] if entity in row else ""
                # Only show ○ for Yes values, empty for others
                if value == "Yes":
                    display_value = "○"
                    yes_count += 1
                else:
                    display_value = ""  # No and empty values show as empty
                html += f'<td class="data-cell symbol-cell">{display_value}</td>'
            
            # Add Coverage Rate for this row
            total_entities = len(entity_columns)
            coverage_percentage = round((yes_count / total_entities * 100), 1) if total_entities > 0 else 0
            html += f'<td class="coverage-cell">{coverage_percentage}%</td>'
            
            html += "</tr>"
    
    # Add Q4 section
    if q4_count > 0:
        for i, idx in enumerate(q4_rows):
            row = df.iloc[idx]
            html += "<tr>"
            
            # Add section title for first row of Q4
            if i == 0:
                html += f'<td class="section-title" rowspan="{q4_count}">{q4_title}</td>'
            
            # Add option
            html += f'<td class="option-col">{row[option_col]}</td>'
            
            # Add entity data
            yes_count = 0
            for entity in entity_columns:
                value = row[entity] if entity in row else ""
                # Only show ○ for Yes values, empty for others
                if value == "Yes":
                    display_value = "○"
                    yes_count += 1
                else:
                    display_value = ""  # No and empty values show as empty
                html += f'<td class="data-cell symbol-cell">{display_value}</td>'
            
            # Add Coverage Rate for this row
            total_entities = len(entity_columns)
            coverage_percentage = round((yes_count / total_entities * 100), 1) if total_entities > 0 else 0
            html += f'<td class="coverage-cell">{coverage_percentage}%</td>'
            
            html += "</tr>"
    
    # Add Q5 section
    if q5_count > 0:
        for i, idx in enumerate(q5_rows):
            row = df.iloc[idx]
            html += "<tr>"
            
            # Add section title for first row of Q5
            if i == 0:
                html += f'<td class="section-title" rowspan="{q5_count}">{q5_title}</td>'
            
            # Add option
            html += f'<td class="option-col">{row[option_col]}</td>'
            
            # Add entity data
            yes_count = 0
            for entity in entity_columns:
                value = row[entity] if entity in row else ""
                # Only show ○ for Yes values, empty for others
                if value == "Yes":
                    display_value = "○"
                    yes_count += 1
                else:
                    display_value = ""  # No and empty values show as empty
                html += f'<td class="data-cell symbol-cell">{display_value}</td>'
            
            # Add Coverage Rate for this row
            total_entities = len(entity_columns)
            coverage_percentage = round((yes_count / total_entities * 100), 1) if total_entities > 0 else 0
            html += f'<td class="coverage-cell">{coverage_percentage}%</td>'
            
            html += "</tr>"
    
    html += "</table>"
    
    return html


def get_base64_image(image_path):
    """Convert image to base64 string for embedding in HTML"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


def create_layout():
    """Landing page with logo and dynamic year-based title"""
    if STYLES_AVAILABLE:
        try:
            apply_page_style()
        except Exception:
            pass

    # Resolve logo path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    logo_path = os.path.join(project_root, 'orignaldata', 'logo.png')

    # Determine year-aware title with line break
    selected_year = st.session_state.get('selected_year', None)
    year_text = None
    if selected_year and str(selected_year).lower() != 'all':
        year_text = str(selected_year)
    
    # Split title into two lines
    main_title = "ILO Youth Employment Action Plan (YEAP):"
    year_title = f"{year_text} Reporting" if year_text else "2025 Reporting"

    # Create a unified blue background container for both logo and title
    st.markdown(f"""
    <div style="
        background-color: rgb(33, 45, 183);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        margin-top: -5px;
        display: flex;
        align-items: center;
        gap: 15px;
        height: 120px;
    ">
        <div style="flex: 1; max-width: 180px; display: flex; align-items: center; justify-content: center;">
              <img src="data:image/png;base64,{get_base64_image(logo_path)}" 
                   style="width: 100%; height: auto; display: block;">
          </div>
        <div style="
            flex: 3;
            color: white;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            line-height: 1.2;
        ">
            <div style="font-family: 'Overpass', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 2.8rem; font-weight: 700; margin-bottom: 5px;">
                {main_title}
            </div>
            <div style="font-family: 'Overpass', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 1.8rem; font-weight: 300;">
                {year_title}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add Q2 pie chart as the first chart
    st.subheader("📊 General Overview")
    st.markdown("""
This dashboard presents key findings from the **ILO Youth Employment Action Plan (YEAP) 2020–2030 Monitoring Progress Survey**, based on inputs from ILO staff across the globe.

It is organized in six tabs:

1\\. **General Overview** – background, definitions, and references  
2\\. **Clusters of the Implementation Framework** – summary of reported outputs by clusters  
3–6\\. **Dedicated cluster information** – insights on progress across four areas

**Filters** (accessible through the navigation panel on the left)

• The **Period Filter** allows users to filter results by year of reporting.  
• The **Organizational Unit Filter** displays results by specific department or region.

**Definitions**

• **Outputs**: tangible deliverables or results contributing to YEAP implementation.  
• **Respondents**: ILO staff from HQ and field offices.

**References**

• [YEAP 2020–2030](https://www.ilo.org/resource/policy/ilos-youth-employment-action-plan-yeap-2020-30)  
• [Youth Employment Crisis: A Call for Action (ILC, 2012)](https://www.ilo.org/sites/default/files/wcmsp5/groups/public/%40ed_norm/%40relconf/documents/meetingdocument/wcms_185950.pdf)
""", unsafe_allow_html=True)
    st.markdown("---")
    
    # Load and display Q2 data
    q2_data = get_q2_data()
    if q2_data:
        q2_chart = create_q2_chart(q2_data)
        if q2_chart:
            st.plotly_chart(q2_chart, use_container_width=True, config={'displayModeBar': False})
        else:
            st.error("Failed to create Q2 chart")
    else:
        st.warning("No Q2 data available")
    
    st.markdown("---")
    
    # Add Q3-Q4-Q5 summary tables as the second chart

    
    # Load and display Q3-Q4-Q5 data
    q345_data = get_q345_data()
    
    if q345_data and ('departments' in q345_data or 'regions' in q345_data):
        # Display Department table
        if 'departments' in q345_data and q345_data['departments']:
            dept_df = create_department_table(q345_data['departments'])
            
        # Display Region table
        if 'regions' in q345_data and q345_data['regions']:
            region_df = create_region_table(q345_data['regions'])
        
        # Add spacing before transposed tables
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Display Transposed Department table
        if 'departments' in q345_data and q345_data['departments']:
            st.markdown("### 📋Mapping of the ILO's Work on Youth Employment across Departments")
            dept_df_transposed = create_department_table_transposed(q345_data['departments'])
            
            if dept_df_transposed is not None and not dept_df_transposed.empty:
                html_table_transposed = create_html_table_with_headers_transposed(dept_df_transposed, q345_data['departments'], "Department")
                st.markdown(html_table_transposed, unsafe_allow_html=True)
            else:
                st.warning("No Department data available for transposed view")
        
        # Add some spacing between transposed tables
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display Transposed Region table
        if 'regions' in q345_data and q345_data['regions']:
            st.markdown("### 📋Mapping of the ILO's Work on Youth Employment across Regions")
            region_df_transposed = create_region_table_transposed(q345_data['regions'])
            
            if region_df_transposed is not None and not region_df_transposed.empty:
                html_table_transposed = create_html_table_with_headers_transposed(region_df_transposed, q345_data['regions'], "Region")
                st.markdown(html_table_transposed, unsafe_allow_html=True)
            else:
                st.warning("No Region data available for transposed view")
    else:
        st.warning("No Q3-Q4-Q5 data available")
    
    st.markdown("---")
    
    # Add Clusters Of The Implementation Framework section
    st.subheader("📊 Clusters Of The Implementation Framework")
    st.markdown("Overview of output counts across all analysis areas")
    
    # Import and use the chart creation function from st_q6q7q10q11_dashboard
    try:
        from st_q6q7q10q11_dashboard import Q6Q7Q10Q11DataProcessor, create_theme_count_chart
        
        # Initialize data processor
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_processor = Q6Q7Q10Q11DataProcessor(base_path)
        
        # Get works count data
        works_count_data = data_processor.get_works_count_data()
        
        if works_count_data:
            # Create and display the chart
            count_fig = create_theme_count_chart(works_count_data, current_theme=None)
            if count_fig:
                st.plotly_chart(count_fig, use_container_width=True)
            else:
                st.info("Chart could not be generated")
        else:
            st.info("No data available for Clusters Of The Implementation Framework")
            
    except Exception as e:
        st.error(f"Error loading Clusters data: {e}")
    
    st.markdown("---")
    st.write("Use the sidebar to select period and navigate other dashboards.")