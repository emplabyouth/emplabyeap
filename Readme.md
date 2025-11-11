# YEAP Data Analysis Dashboard Guide

## 📋 Project Overview

The **YEAP (Youth Employment Action Programme) Data Analysis Dashboard** is an interactive data visualization platform built with **Streamlit** to analyze survey data related to the Youth Employment Action Plan.

The dashboard contains five main pages, providing comprehensive insights from overall survey results to specialized thematic analysis.

### Page Structure

1. **🏠 Overview** – Survey overview page
2. **📚 Knowledge Development & Dissemination** – Analysis of knowledge products and dissemination outputs
3. **🔧 Technical Assistance** – Analysis of technical assistance-related outputs
4. **🎓 Capacity Development** – Analysis of capacity development activities
5. **🤝 Advocacy & Partnerships** – Analysis of advocacy initiatives and partnership-related outputs

---

## 🏠 Overview Page (Survey Overview)

### Page Functions

* **Comprehensive Overview**
  Provides a high-level overview of survey responses and key findings.

* **Q2 Data Visualization**
  Displays a pie chart for core survey questions based on Q2 data.

* **Q3–Q5 Summary Tables**
  Shows aggregated data on:

  * Implementation framework clusters
  * Policy pillars
  * Target youth groups

### Data File Locations

* **Q2 Data**

  * `orignaldata/PART1_base_dataQ2-5.csv`
* **Q3–Q5 Data**

  * `orignaldata/PART2_base_dataQ3.csv`
  * `orignaldata/PART2_base_dataQ4.csv`
  * `orignaldata/PART2_base_dataQ5.csv`

### Display Content

1. **Unified Header**

   * Blue background container
   * Displays ILO logo
   * Shows year-based title related to the reporting period

2. **Q2 Pie Chart**

   * Visualizes responses to core Q2 questions using PART1 data.

3. **Q3–Q5 Summary Tables**

   * Provides summary tables for:

     * Clusters of the implementation framework
     * Policy and programmatic areas
     * Target youth groups

---

## 🔗 Project Links

* **GitHub Repository:** `https://github.com/emplabyouth/emplabyeap`
* **Git Clone URL:** `https://github.com/emplabyouth/emplabyeap.git`
* **Streamlit Cloud Console:** `https://streamlit.io/cloud` (login with GitHub)
* **Deployed Streamlit App:** `https://emplabyeap.streamlit.app`

---

## 📊 General Survey Analysis Page

### Page Functions

* Supports visualization of **all** survey questions.
* Automatically selects the most appropriate chart type:

  * Pie chart
  * Vertical bar chart
  * Horizontal bar chart
* Provides interactive controls for:

  * Selecting survey questions
  * Switching chart types

### Data File Location

* **Main data file:** `orignaldata/PART1_base_dataQ2-5.csv`
* **Data format:**

  * `question` – Question text
  * `option` – Response option
  * `count` – Count of responses

### Chart Creation Logic

#### Auto Chart Selection Logic

* **Pie Chart**

  * Used when the number of options is **≤ 5**.

* **Vertical Bar Chart**

  * Used when:

    * Number of options > 5, or
    * Label text is relatively long.

* **Horizontal Bar Chart**

  * Used when:

    * Number of options > 10, or
    * Label length > 20 characters.

#### Data Processing Rules

* **Column Mapping**

  * `question` → Chart title
  * `option` → Category label
  * `count` → Numerical value in charts

* **Filtering Rules**

  * For **Q4** and **Q5** questions:

    * Exclude options labeled **“Other”**.
  * For **Q2**:

    * Display **all** options (no filtering).

#### Data Table Display

* Displayed contents:

  * Option name
  * Count
  * Percentage
* Sorting:

  * Sorted by count in **descending** order.
* Percentage:

  * Automatically calculated for each option.

---

## 📈 Specialized Analysis Pages

### Page Functions

The specialized analysis pages provide:

* **Independent page titles and subtitles** for each thematic area.
* **Outputs count comparison** across different question categories.
* **Thematic frequency analysis** organized by major themes.
* **Filtering options**:

  * By department/region
  * By year
* **Multi-dimensional analysis**, including:

  * Funding sources
  * Target youth groups
  * Delivery modalities
  * Geographic focus

### Page Title System

Each specialized page has its own configured titles:

#### 📊 Outputs Count Statistics

* **Main title:** `📊 Outputs Count Statistics`
* **Subtitle:** `Overview of output counts across all analysis areas`

#### 📚 Knowledge Development & Dissemination

* **Main title:** `📚 Knowledge Development & Dissemination`
* **Subtitle:** `Analysis of knowledge development and dissemination outputs`

#### 🔧 Technical Assistance

* **Main title:** `🔧 Technical Assistance`
* **Subtitle:** `Analysis of technical assistance outputs and delivery`

#### 🎓 Capacity Development

* **Main title:** `🎓 Capacity Development`
* **Subtitle:** `Analysis of capacity development programs and outcomes`

#### 🤝 Advocacy & Partnerships

* **Main title:** `🤝 Advocacy & Partnerships`
* **Subtitle:** `Analysis of advocacy initiatives and partnership activities`

### Data File Locations

* **Q6 – Knowledge Development & Dissemination:**
  `orignaldata/PART3_base_dataQ6.csv`
* **Q7 – Technical Assistance:**
  `orignaldata/PART3_base_dataQ7.csv`
* **Q10 – Capacity Development:**
  `orignaldata/PART3_base_dataQ10.csv`
* **Q11 – Advocacy & Partnerships:**
  `orignaldata/PART3_base_dataQ11.csv`

### Filtering Features

* **Region Filter**

  * Based on `Department/Region` field.

* **Year Filter**

  * Global year selector.

* **Real-time Application**

  * Selected filters are applied instantly to all relevant charts and tables.

### Page Layout Structure

#### 1. Outputs Count Comparison

* **Chart Title:** `Outputs Count by Question`
* **Data Source:** Combined data from Q6, Q7, Q10, and Q11.
* **Indicators:**

  * Number of staff reporting
  * Number of outputs delivered
* **Chart Type:** Grouped bar chart.

#### 2. Themed Frequency Analysis

Powered by the `Q6Q7Q10Q11DataProcessor` class, which:

* Merges multiple data sources
* Performs dynamic statistics
* Applies filters in real time

##### Theme 1: Q6 – Knowledge Development & Dissemination

* **Background:** Light blue
* **Processing:**

  * Recalculates `works_count`
  * Identifies valid outputs and unique contributors
* **Dimensions:**

  * Funding sources
  * Target groups
  * Types of knowledge and dissemination outputs delivered

##### Theme 2: Q7 – Technical Assistance

* **Background:** Light green
* **Dimensions:**

  * Funding sources
  * Target groups
  * Regional distribution (`Technical Assistance Outputs Across Regions`, top 10 regions)

##### Theme 3: Q10 – Capacity Development

* **Background:** Light yellow
* **Dimensions:**

  * Delivery modes
  * Funding sources
  * Certification status
  * Target groups

##### Theme 4: Q11 – Advocacy & Partnerships

* **Background:** Light pink
* **Dimensions:**

  * Funding sources
  * Target groups
  * Types of advocacy or partnership outputs
  * Regional distribution (`Advocacy & Partnership Outputs Across Regions`, top 10 regions)
  * Geographical focus of outputs

### Chart Style Guidelines

* **Pie Charts**

  * Show share of each category
  * Display exact counts and percentages for each slice

* **Bar Charts**

  * Show comparisons across multiple categories
  * Applied when categories are more numerous or labels are longer

* **Automatic Selection**

  * Chart type is automatically selected based on:

    * Number of options
    * Length of labels
    * Layout clarity

---

## 🔧 Technical Implementation Details

### System Architecture

* **Frontend Framework:** Streamlit
* **Data Processing:** Pandas
* **Charting Library:** Plotly
* **Styling:**

  * `StreamlitStyleManager` class
  * CSS variable system
  * Unified color scheme
* **Modular Design:**

  * Separated page components
  * Style management
  * Color configuration

### Core Modules

* `streamlit_app.py`

  * Main entry point
  * Page configuration
  * Navigation
  * Global filters (year, department/region)

* `st_landing_dashboard.py`

  * Overview page
  * Q2 pie chart
  * Q3–Q5 summary tables

* `st_q6q7q10q11_dashboard.py`

  * Specialized analysis page for Q6, Q7, Q10, Q11

* `st_styles.py`

  * `StreamlitStyleManager`
  * Global style configuration
  * Standardized chart layout

* `color_config.py`

  * Centralized color palette and theme configuration

### Unified Header Design

* Blue background container: `RGB(33, 45, 183)`
* Displays the ILO logo on the left
* Shows a dynamic year-based reporting title
* Responsive layout for different screen sizes

### Data Processing Workflow

1. **Secure Data Loading**

   * Uses `safe_read_csv` to:

     * Auto-detect encoding
     * Handle file read errors

2. **Global Filters**

   * Manages year and department/region filters with `st.session_state`.

3. **Preprocessing**

   * `Q6Q7Q10Q11DataProcessor`:

     * Merges relevant data
     * Cleans and standardizes fields

4. **Dynamic Aggregation**

   * Recalculates statistics on the fly instead of relying on pre-aggregated results.

5. **Standardized Visualization**

   * Uses `StreamlitStyleManager` to:

     * Apply consistent visual styles
     * Handle label wrapping
     * Configure layout parameters

6. **Responsive Layout**

   * Adjusts chart and table display based on content and screen size.

### Performance Optimization

* **Session Caching**

  * Data loaded only once per session.

* **Real-time Filtering**

  * Filters applied without reloading data files.

* **Smart Chart Selection**

  * Adapts visualization types to data structure for clarity and performance.

### Error Handling

* **File Existence Checks**

  * Verifies required CSV files.

* **Data Validation**

  * Ensures expected columns and formats are present.

* **User-Friendly Messages**

  * Provides clear instructions and hints when issues occur.

---

## 📊 Data Quality Standards

### Data Integrity Requirements

* Project name fields must not be empty.
* Numeric fields cannot be:

  * `'None'`
  * `'nan'`
  * Empty strings
* Only valid records are included in statistics.

### Data Filtering Rules

* **“Other” Options**

  * May be excluded for clarity in certain charts.
* **Year Filtering**

  * Supports restricting data to selected reporting years.

---

## 🚀 Usage Guide

### Starting the Application Locally

```bash
cd streamlit
streamlit run streamlit_app.py
```

### Navigation

1. Use the **sidebar navigation menu** to switch between:

   * Overview
   * Outputs Count Statistics
   * Knowledge Development & Dissemination
   * Technical Assistance
   * Capacity Development
   * Advocacy & Partnerships

2. Use **global filters** in the sidebar:

   * Select specific year or “All”
   * Select department/region where applicable

3. **Interactive features:**

   * Click or hover on chart elements to see more details.

### Data Filtering

1. **Year Filter**

   * Choose a specific year.
   * Or select “All” to view all years combined.

2. **Region / Department Filter**

   * On specialized pages, select specific organizational units.

3. **Real-time Updates**

   * All charts and tables update immediately when filters change.

### Chart Interaction

* **Hover Tooltips:**

  * View detailed numerical values.
* **Zooming & Panning:**

  * Explore chart details interactively.
* **Download Option:**

  * Export charts as images when enabled.

---

## 📁 Project File Structure

```bash
emplabyeap-main/
├── orignaldata/                      # Raw data directory
│   ├── PART1_base_dataQ2-5.csv       # Q2 pie chart & general survey analysis
│   ├── PART2_base_dataQ3.csv         # Q3 summary (implementation framework)
│   ├── PART2_base_dataQ4.csv         # Q4 summary (policy pillars)
│   ├── PART2_base_dataQ5.csv         # Q5 summary (target groups)
│   ├── PART3_base_dataQ6.csv         # Q6 - Knowledge Dev. & Dissemination
│   ├── PART3_base_dataQ7.csv         # Q7 - Technical Assistance
│   ├── PART3_base_dataQ10.csv        # Q10 - Capacity Development
│   ├── PART3_base_dataQ11.csv        # Q11 - Advocacy & Partnerships
│   ├── logo.png                      # ILO logo
│   └── question_list.csv             # Full question list
├── streamlit/                        # Streamlit application directory
│   ├── streamlit_app.py              # Main entry, navigation, global filters
│   ├── st_landing_dashboard.py       # Overview: Q2 + Q3–Q5 summary
│   ├── st_q6q7q10q11_dashboard.py    # Specialized analysis: Q6/Q7/Q10/Q11
│   ├── st_styles.py                  # Global styles and theming
│   ├── color_config.py               # Common color configuration
│   ├── visualizer.py                 # Visualization helpers
│   ├── assets/fonts/                 # Font resources
│   ├── pages/                        # Optional: additional pages (if enabled)
│   └── requirements.txt              # Python dependencies for Streamlit app
├── start_dashboard.py                # Local start script
├── upload_to_github_example.ps1      # Example Git upload script
├── requirements.txt                  # Project-level dependencies
└── readme.md                         # Project documentation (this file)
```

---

# YEAP Dashboard – Beginner Guide

This section explains, step by step, how to:

1. Set up the YEAP Dashboard locally
2. Upload it to GitHub
3. Deploy it on Streamlit Cloud

All operational steps from the original guide are included below without omission.

## 1. Prerequisites

Before you begin, ensure you have the following installed and configured:

* **Git**

  * Used for version control and syncing with GitHub.
  * Download: `https://git-scm.com/downloads`

* **Python**

  * Programming language used by the dashboard.
  * Download: `https://www.python.org/downloads/`

* **Streamlit**

  * Framework for building the dashboard.
  * Install via pip:

    ```bash
    pip install streamlit
    ```

* **GitHub Account**

  * For hosting your repository.
  * Sign up: `https://github.com/join`

* **Streamlit Cloud Account**

  * For deploying your dashboard online.
  * Sign up: `https://streamlit.io/cloud`

## 2. Local Setup

1. **Download the Project**

   * Obtain the project files:

     * Either by downloading a ZIP file, or
     * By cloning an existing repository (if available).
   * Extract or place the project folder in a simple path, e.g.:
     `C:\Users\<YourUsername>\Desktop\yeap`

2. **Open Terminal in the Project Directory**

   * On Windows:

     * Open File Explorer
     * Navigate into the `yeap` project folder
     * Right-click inside the folder
     * Select **“Open in Terminal”** or **“Open PowerShell window here”**
   * On macOS/Linux:

     * Open Terminal and run:

       ```bash
       cd /path/to/yeap
       ```

3. **Create and Activate a Virtual Environment (Optional but Recommended)**

   * Example using `venv`:

     ```bash
     python -m venv .venv
     ```
   * Activate (Windows PowerShell):

     ```bash
     .\.venv\Scripts\Activate.ps1
     ```
   * Activate (macOS/Linux):

     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies**

   * The Streamlit app dependencies are listed in:

     * `streamlit/requirements.txt`
   * In your activated environment, run:

     ```bash
     pip install -r streamlit/requirements.txt
     ```

5. **Run the Dashboard Locally**

   * Ensure your environment is activated.
   * From the project root (same directory as `start_dashboard.py`), run:

     ```bash
     python start_dashboard.py
     ```
   * The script will:

     * Launch Streamlit
     * Open your default browser at:

       * `http://localhost:8501` (or similar)
   * You should now see the YEAP Dashboard running locally.

## 3. Page Structure (Within the Running App)

The YEAP Dashboard typically includes:

1. **🏠 Home**

   * Project introduction and overview.

2. **📊 Overview**

   * High-level data overview and basic statistics.

3. **📊 Outputs Count Statistics**

   * Comparative analysis of outputs across clusters/questions.

4. **🌱 Knowledge Development & Dissemination**

   * Detailed analysis of knowledge products and dissemination outputs.

5. **🔧 Technical Assistance**

   * Analysis of technical support and advisory activities.

6. **💪 Capacity Development**

   * Analysis of trainings, workshops, and capacity-building initiatives.

7. **🤝 Advocacy & Partnerships**

   * Analysis of advocacy initiatives and partnership-based outputs.

Each specialized page:

* Has a clearly defined **main title** and **subtitle**.
* Focuses on one dimension of the Youth Employment Action Plan.

## 4. Uploading from Local to GitHub

A sample PowerShell script `upload_to_github_example.ps1` is included to simplify the upload process.

### Step-by-Step

1. **Create a New GitHub Repository**

   * Go to: `https://github.com/new`
   * Enter a repository name, e.g. `YEAP-Dashboard`
   * **Important:**

     * Do **NOT** initialize with:

       * README
       * `.gitignore`
       * License
     * These are already in your local project.
   * Click **“Create repository”**.

2. **Initialize Git Locally (If Not Already Done)**

   In the project root (`yeap`):

   ```bash
   git init
   ```

3. **Configure Remote Origin**

   * On your GitHub repository page, copy the HTTPS URL, e.g.:

     * `https://github.com/<your_username>/YEAP-Dashboard.git`

   * In your terminal:

     ```bash
     git remote add origin https://github.com/<your_username>/YEAP-Dashboard.git
     ```

   * If `origin` already exists and points elsewhere:

     ```bash
     git remote remove origin
     git remote add origin https://github.com/<your_username>/YEAP-Dashboard.git
     ```

4. **Prepare the Upload Script**

   * Rename:

     * `upload_to_github_example.ps1` → `upload_to_github.ps1`
   * Open `upload_to_github.ps1` in a text editor.
   * At the bottom of the script:

     * Replace the placeholder:

       * `https://github.com/your_username/your_repository.git`
       * with your actual GitHub repository URL.

5. **Run the Upload Script**

   From the project root in PowerShell:

   ```bash
   .\upload_to_github.ps1
   ```

   The script will:

   * Check Git status.
   * Add all modified and new files.
   * Prompt you for a commit message:

     * You may press **Enter** to accept the default.
   * Attempt to push to GitHub:

     * If a normal push fails (e.g. due to remote changes), it may:

       * Attempt a forced push depending on script configuration.
   * Print:

     * Your GitHub repository URL.
     * A suggested link for checking Streamlit Cloud deployment.

## 5. Deploying to Streamlit Cloud

Streamlit Cloud allows you to deploy directly from your GitHub repository.

1. **Open Streamlit Cloud**

   * Visit: `https://share.streamlit.io/` or `https://streamlit.io/cloud`

2. **Log In**

   * Use your GitHub account to sign in.

3. **Create a New App**

   * Click **“New app”**.
   * Select **“From existing repo”**.

4. **Configure Deployment**

   * **Repository:**
     `your_username/YEAP-Dashboard`
   * **Branch:**
     Usually `main` (or `master` if applicable).
   * **Main file path:**
     `streamlit/streamlit_app.py`
   * **Python version:**
     Choose a supported version, e.g. `3.9` or `3.10`.
   * **Advanced Settings (Optional):**

     * **Secrets:**
       Add only if your app connects to external APIs or sensitive data.
     * **Custom command:**
       Not required for a standard Streamlit app.

5. **Deploy**

   * Click **“Deploy!”**.
   * Streamlit Cloud will:

     * Install dependencies from `requirements.txt` / `streamlit/requirements.txt`
     * Run `streamlit_app.py`
   * After build completion:

     * You receive a public URL for your dashboard.

---

## 6. Troubleshooting

### Common Issues & Solutions

1. **Python Dependency Issues**

   * Ensure Python version is **3.7 or above**.
   * If installation fails:

     ```bash
     python -m pip install --upgrade pip
     pip install -r streamlit/requirements.txt
     ```

2. **Streamlit Startup Problems**

   * Check if port `8501` is already in use.
   * Run on another port:

     ```bash
     streamlit run streamlit/streamlit_app.py --server.port 8502
     ```

3. **GitHub Upload Issues**

   * Confirm Git username and email are configured:

     ```bash
     git config --global user.name "Your Name"
     git config --global user.email "you@example.com"
     ```
   * Check network connectivity.
   * Ensure remote repository URL is correct.
   * If push is rejected:

     * Pull first or adjust script/force push as appropriate.

4. **Missing or Incorrect Data Files**

   * Ensure all required CSVs are inside `orignaldata/`.
   * Verify:

     * File names exactly match the ones referenced in code.
     * No typo in paths.

### How to Get Help

If issues persist:

1. Read the full error message shown in the terminal.
2. Confirm file paths and filenames.
3. Verify the structure of your CSV files.
4. Review this README and the **Title Modification Guide** below.

---

# YEAP Dashboard Title Modification Guide

This document explains how to modify titles using text search, without relying on fixed line numbers—making it robust to future code changes.

## Project Structure (Relevant Files)

* `streamlit_app.py` – Main entry; navigation menu.
* `st_landing_dashboard.py` – Overview page.
* `st_q6q7q10q11_dashboard.py` – Detailed thematic dashboards.
* `st_styles.py` – Styling configuration.

## Types of Titles & How to Modify Them

### 1. Page Main Titles

**Search Keyword:** `st.title(`
**Files:** `st_landing_dashboard.py`, `st_q6q7q10q11_dashboard.py`

**Example:**

```python
# Original:
st.title("📊 General Overview")
# Change to:
st.title("📊 Your New Title")
```

### 2. Unified Page Header

**Search Keyword:** `create_unified_header`
**File:** `st_q6q7q10q11_dashboard.py`

**What to Edit:**

* Main header text:

  * Search for: `"ILO Youth Employment Action Plan (YEAP):"`
* Year-related text:

  * Search for: `f"{selected_year} Reporting"`

Modify the strings as needed while keeping function calls intact.

### 3. Navigation Menu Titles

**Search Keyword:** `PAGES = {`
**File:** `streamlit_app.py`

**Example:**

```python
PAGES = {
    "🏠 Overview": st_landing_dashboard,
    "📊 Clusters Of The Implementation Framework": st_q6q7q10q11_dashboard,
}
```

You may rename the keys (left-hand strings) to adjust sidebar labels.

### 4. Page-Specific Titles

**Search Keyword:** `page_titles = {`
**File:** `st_q6q7q10q11_dashboard.py`

This dictionary may include:

* `"📊 Clusters Of The Implementation Framework"`
* `"📚 Knowledge Development & Dissemination"`
* `"🔧 Technical Assistance"`
* `"🎓 Capacity Development"`
* `"🤝 Advocacy & Partnerships"`

Edit the mapped strings to update visible titles accordingly.

### 5. Chart Titles

**Examples of Search Terms:**

* `"Number of Outputs Delivered by Cluster"`
* `"Distribution of Responses on Whether Entities Conducted Youth Employment Work"`
* `"📋 Outputs Detail List"`

**Files:**

* Located mainly in:

  * `st_landing_dashboard.py`
  * `st_q6q7q10q11_dashboard.py`

Search by the exact title string and replace with your desired wording.

### 6. Subtitles & Descriptive Text

**Search Keywords:**

* `st.subheader(`
* `st.markdown("###`
* Long-form explanatory text strings.

**Files:** All dashboard-related `.py` files.

You can adjust these for explanatory clarity, language localization, or branding.

---

## Recommended Editing Steps

1. **Identify the Type of Text to Modify**

   * Page title? → search `st.title(`
   * Sidebar navigation? → search `PAGES = {`
   * Thematic page title? → search `page_titles = {`
   * Chart title? → search the current text.
   * Subheader/text? → search `st.subheader(` or markdown calls.

2. **Use Global Search**

   * Use your editor's:

     * `Ctrl+F` for file search
     * `Ctrl+Shift+F` (or equivalent) for project-wide search

3. **Edit Safely**

   * Keep emojis if used for structure and recognizability.
   * Only replace text within the quotes.
   * Do not alter Python syntax.

4. **Test After Changes**

   * Save files.
   * Restart the Streamlit app:

     ```bash
     streamlit run streamlit/streamlit_app.py
     ```
   * Verify that all modified titles display correctly.

---

## Notes & Good Practices

1. **Consistency**

   * Ensure related titles are updated consistently across files and pages.

2. **Formatting**

   * Keep emojis, capitalization, and spacing consistent with project style.

3. **Backup**

   * Consider backing up files or using Git commits before large-scale edits.

4. **Encoding**

   * Ensure UTF-8 encoding for multilingual content.

5. **Bulk Changes**

   * Use “Find and Replace” with caution.
   * Always re-run and visually inspect the app after batch edits.

---



##Chinese 中文



# YEAP 数据分析仪表板说明书 
# YEAP Data Analysis Dashboard Guide

## 📋 项目概览 Project Overview

YEAP (Youth Employment Action Programme) 数据分析仪表板是一个基于 Streamlit 的交互式数据可视化平台，用于分析青年就业行动计划的调查数据。该仪表板包含五个主要页面，提供从概览到专项分析的全方位数据洞察。

### 页面结构 Page Structure
1. **🏠 Overview** - 调查概览页面
2. **📚 Knowledge Development & Dissemination** - 知识发展与传播分析
3. **🔧 Technical Assistance** - 技术援助分析
4. **🎓 Capacity Development** - 能力发展分析
5. **🤝 Advocacy & Partnerships** - 倡导与合作伙伴关系分析

## 🏠 Overview 页面 (调查概览)

### 页面功能 Page Functions
- **综合概览**: 提供调查响应和关键洞察的全面概述
- **Q2 数据展示**: 显示核心调查问题的饼图分析
- **Q3-Q5 汇总表**: 展示实施框架、政策领域和目标群体的汇总数据

### 数据文件位置 Data File Locations
- **Q2 数据**: `orignaldata/PART1_base_dataQ2-5.csv`
- **Q3-Q5 数据**: 
  - `orignaldata/PART2_base_dataQ3.csv`
  - `orignaldata/PART2_base_dataQ4.csv`
  - `orignaldata/PART2_base_dataQ5.csv`

### 显示内容 Display Content
1. **统一头部**: 蓝色背景容器，包含 ILO Logo 和年份感知标题
2. **Q2 饼图**: 基于 PART1 数据的核心问题可视化
3. **Q3-Q5 汇总表**: 三个专项分析的数据汇总表格

---

## 🔗 项目地址 Links

- GitHub 仓库: https://github.com/emplabyouth/emplabyeap
- Git 克隆地址: https://github.com/emplabyouth/emplabyeap.git
- Streamlit Cloud 控制台: https://streamlit.io/cloud （使用 GitHub 账号登录）
- Streamlit 应用地址:  https://emplabyeap.streamlit.app

---

## 📊 General Survey Analysis 页面 (通用调查分析)

### 页面功能 Page Functions
- **多问题分析**: 支持所有问题的可视化分析
- **多图表类型**: 自动选择最适合的图表类型（饼图、条形图、横向条形图）
- **交互式功能**: 提供问题选择和图表类型切换功能

### 数据文件位置 Data File Location
- **主数据文件**: `orignaldata/PART1_base_dataQ2-5.csv`
- **文件格式**: CSV 文件，包含三列：`question`(问题), `option`(选项), `count`(数量)

### 图表制作方式 Chart Creation Methods

#### 自动图表选择逻辑 Auto Chart Selection Logic
- **饼图**: 当选项 ≤ 5个时使用
- **竖条图**: 当选项 > 5个或标签文字较长时使用
- **横条图**: 当选项 > 10个或标签文字 > 20个字符时使用

#### 数据处理规则 Data Processing Rules
- **数据映射**: 
  - `question`列 → 图表标题
  - `option`列 → 图表分类标签
  - `count`列 → 图表数值
- **数据过滤**: 
  - Q4和Q5问题：过滤掉"其他"选项
  - Q2问题：显示所有选项（不过滤）

#### 数据表格显示 Data Table Display
- **显示内容**: 选项名称、数量、百分比
- **排序方式**: 按数量从高到低排序
- **百分比计算**: 自动计算各选项占比

---

## 📈 Specialized Analysis Pages (专项分析页面)

### 页面功能 Page Functions
- **独立页面标题**: 每个专项分析页面都有独立的主标题和副标题
- **产出统计对比**: 各问题类别的产出数量统计
- **主题化分析**: 按四大主题组织的详细频率分析
- **地区筛选**: 支持按组织单位筛选数据
- **多维度分析**: 资金来源、目标群体、交付方式等多角度分析

### 页面标题系统 Page Title System
每个专项分析页面都有独立的标题配置：

#### 📊 Outputs Count Statistics
- **主标题**: "📊 Outputs Count Statistics"
- **副标题**: "Overview of output counts across all analysis areas"

#### 📚 Knowledge Development & Dissemination
- **主标题**: "📚 Knowledge Development & Dissemination"
- **副标题**: "Analysis of knowledge development and dissemination outputs"

#### 🔧 Technical Assistance
- **主标题**: "🔧 Technical Assistance"
- **副标题**: "Analysis of technical assistance outputs and delivery"

#### 🎓 Capacity Development
- **主标题**: "🎓 Capacity Development"
- **副标题**: "Analysis of capacity development programs and outcomes"

#### 🤝 Advocacy & Partnerships
- **主标题**: "🤝 Advocacy & Partnerships"
- **副标题**: "Analysis of advocacy initiatives and partnership activities"

### 数据文件位置 Data File Locations
- **Q6_knowledge development&dissemination**: `orignaldata/PART3_base_dataQ6.csv`(知识发展与传播)
- **Q7_technical assistance**: `orignaldata/PART3_base_dataQ7.csv`(技术援助)
- **Q10_capacity development**: `orignaldata/PART3_base_dataQ10.csv`(能力发展)
- **Q11_advocacy&partnerships**: `orignaldata/PART3_base_dataQ11.csv`(倡导与合作伙伴关系)

### 筛选功能 Filtering Features
- **地区筛选**: `Department/Region` 字段筛选
- **年份筛选**: 全局年份筛选功能
- **实时应用**: 筛选条件实时应用到所有图表

### 页面布局结构 Page Layout Structure

#### 1. 产出统计对比 Outputs Count Comparison
- **图表标题**: "Outputs Count by Question"
- **数据来源**: 综合 Q6、Q7、Q10、Q11 四个数据文件
- **显示指标**: 
  - Number of staff reporting (报告员工数量)
  - Number of outputs delivered (交付产出数量)
- **图表类型**: 分组条形图

#### 2. 主题化频率分析 Themed Frequency Analysis
**技术实现**: 使用 Q6Q7Q10Q11DataProcessor 类进行数据处理，支持多数据源合并、动态统计计算和实时筛选

##### 主题1: Q6 - 知识发展与传播 Knowledge Development & Dissemination
- **主题颜色**: 浅蓝色背景
- **数据处理**: 自动重新计算 works_count 统计，识别有效作品和唯一用户
- **分析维度**:
  - 资金来源分析: "Funding Source Of Knowledge Development And Dissemination Outputs"
  - 目标群体分析: "Target Group Of Knowledge Development And Dissemination Outputs"
  - 产出类型分析: "Types Of Knowledge Development And Dissemination Outputs Delivered"

##### 主题2: Q7 - 技术援助 Technical Assistance
- **主题颜色**: 浅绿色背景
- **分析维度**:
  - 资金来源分析: "Funding Source Of Technical Assistance Outputs"
  - 目标群体分析: "Target Group Of Technical Assistance Outputs"
  - 地区分布分析: "Technical Assistance Outputs Across Regions" (显示前10个地区)

##### 主题3: Q10 - 能力发展 Capacity Development
- **主题颜色**: 浅黄色背景
- **分析维度**:
  - 交付方式分析: "Delivery Mode Of Capacity Development Outputs"
  - 资金来源分析: "Funding Source For Capacity Development Outputs"
  - 认证情况分析: "Capacity Development Outputs & Certification"
  - 目标群体分析: "Target Group Of Capacity Development Outputs"

##### 主题4: Q11 - 倡导与合作伙伴关系 Advocacy & Partnerships
- **主题颜色**: 浅粉色背景
- **分析维度**:
  - 资金来源分析: "Funding Source For Advocacy & Partnerships Related Outputs"
  - 目标群体分析: "Target Group For Advocacy & Partnerships Outputs"
  - 产出类型分析: "Types Of Advocacy Or Partnership Outputs"
  - 地区分布分析: "Advocacy & Partnership Outputs Across Regions" (显示前10个地区)
  - 地理重点分析: "Geographical Focus Of Advocacy And Partnerships Outputs"

### 图表样式说明 Chart Style Guidelines
- **饼图**: 显示各类别分布比例，每个扇形显示具体数量和百分比
- **条形图**: 显示各类别数量对比，适用于多类别比较
- **自动选择**: 根据数据特征自动选择最适合的图表类型

---

## 🔧 技术实现详情 Technical Implementation

### 系统架构 System Architecture
- **前端框架**: Streamlit
- **数据处理**: Pandas
- **图表库**: Plotly
- **样式管理**: StreamlitStyleManager 类 + CSS 变量系统 + 统一配色方案
- **模块化设计**: 分离的页面组件、样式管理和颜色配置

#### 核心模块 Core Modules
- **streamlit_app.py**: 主应用入口，负责页面配置、导航和全局筛选器
- **st_landing_dashboard.py**: Overview 页面，包含 Q2 饼图和 Q3-Q5 汇总表
- **st_q6q7q10q11_dashboard.py**: 专项分析页面，处理 Q6、Q7、Q10、Q11 数据
- **st_styles.py**: StreamlitStyleManager 类，提供全局样式管理、标准化图表生成和主题配置
- **color_config.py**: 统一的颜色配置和主题管理

### 统一头部设计 Unified Header Design
- **蓝色背景容器**: RGB(33, 45, 183)
- **ILO Logo**: 左侧显示国际劳工组织标志
- **年份感知标题**: 根据选择年份动态更新标题
- **响应式设计**: 适配不同屏幕尺寸

### 数据处理流程 Data Processing Workflow
1. **安全数据加载**: 使用 safe_read_csv 函数自动检测编码并处理读取错误
2. **全局筛选**: 通过 session_state 管理年份和组织单位筛选器
3. **数据预处理**: Q6Q7Q10Q11DataProcessor 类负责数据合并和预处理
4. **动态聚合**: 实时重新计算统计数据而非使用预计算结果
5. **标准化可视化**: StreamlitStyleManager 提供统一的图表配置、频率筛选和标签包装功能
6. **响应式布局**: 根据数据内容动态调整表格和图表显示

### 性能优化 Performance Optimization
- **会话缓存**: 数据在会话中只加载一次
- **实时筛选**: 筛选条件实时应用，无需重新加载
- **智能图表**: 根据数据量自动选择最优图表类型

### 错误处理 Error Handling
- **文件检查**: 自动检测数据文件是否存在
- **数据验证**: 验证数据格式和完整性
- **友好提示**: 提供清晰的错误信息和解决建议

---

## 📊 数据质量标准 Data Quality Standards

### 数据完整性要求 Data Integrity Requirements
- 项目名称字段不能为空
- 数值字段不能是 'None'、'nan' 或空字符串
- 只统计符合标准的有效记录

### 数据筛选规则 Data Filtering Rules
- **百分比阈值**: other选项可能被过滤
- **年份筛选**: 支持按具体年份筛选数据

---

## 🚀 使用指南 Usage Guide

### 本地启动应用 Starting the Application
```bash
cd streamlit
streamlit run streamlit_app.py
```

### 导航使用 Navigation Usage
1. **侧边栏导航**: 使用左侧导航菜单切换页面
2. **全局筛选**: 使用侧边栏的年份和地区筛选器
3. **交互功能**: 点击图表元素查看详细信息

### 数据筛选 Data Filtering
1. **年份筛选**: 在侧边栏选择特定年份或"All"查看所有年份
2. **地区筛选**: 在专项分析页面选择特定组织单位
3. **实时更新**: 筛选条件会立即应用到所有相关图表

### 图表交互 Chart Interaction
- **悬停信息**: 鼠标悬停查看详细数值
- **缩放功能**: 支持图表缩放和平移
- **下载功能**: 可下载图表为图片格式

---

## 📁 项目文件结构 Project File Structure

```
emplabyeap-main/
├── orignaldata/                    # 原始数据文件夹
│   ├── PART1_base_dataQ2-5.csv   # Q2 饼图与通用分析数据
│   ├── PART2_base_dataQ3.csv     # Q3 概览汇总（实施框架）
│   ├── PART2_base_dataQ4.csv     # Q4 概览汇总（政策支柱）
│   ├── PART2_base_dataQ5.csv     # Q5 概览汇总（目标群体）
│   ├── PART3_base_dataQ6.csv     # Q6_knowledge development & dissemination
│   ├── PART3_base_dataQ7.csv     # Q7_technical assistance
│   ├── PART3_base_dataQ10.csv    # Q10_capacity development
│   ├── PART3_base_dataQ11.csv    # Q11_advocacy & partnerships
│   ├── logo.png                   # ILO 标志文件
│   └── question_list.csv          # 问题列表文件
├── streamlit/                      # Streamlit 应用文件夹
│   ├── streamlit_app.py           # 主应用入口，页面配置与导航（年份/组织单位筛选）
│   ├── st_landing_dashboard.py    # Overview：Q2 饼图、Q3–Q5 概览汇总表
│   ├── st_q6q7q10q11_dashboard.py # 专项分析：Q6/Q7/Q10/Q11
│   ├── st_styles.py               # 全局样式与主题配置
│   ├── color_config.py            # 统一配色方案
│   ├── visualizer.py              # 可视化辅助
│   ├── assets/fonts/              # 字体资源
│   ├── pages/                     # 多页面支持（如启用）
│   └── requirements.txt           # Python 依赖文件（Streamlit 子项目）
├── start_dashboard.py             # 启动脚本
├── upload_to_github_example.ps1   # Git 上传脚本示例
├── requirements.txt               # 项目依赖
└── readme.md                      # 项目说明文件
```

---


# YEAP Dashboard - 新手指南

本教程将指导您如何在本地设置 YEAP Dashboard 项目，将其上传到 GitHub，并部署到 Streamlit Cloud。

## 1. 前提条件

在开始之前，请确保您已安装并设置好以下各项：

- **Git**: 用于版本控制和与 GitHub 交互。
  - 下载地址: [https://git-scm.com/downloads](https://git-scm.com/downloads)
- **Python**: 仪表板的编程语言。
  - 下载地址: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Streamlit**: 用于构建仪表板的框架。
  - 通过 pip 安装: `pip install streamlit`
- **GitHub 账户**: 用于托管您的代码仓库。
  - 注册地址: [https://github.com/join](https://github.com/join)
- **Streamlit Cloud 账户**: 用于在线部署您的仪表板。
  - 注册地址: [https://streamlit.io/cloud](https://streamlit.io/cloud)

## 2. 本地设置

1.  **下载项目**: 获取项目文件（例如，通过下载 ZIP 文件或如果您已有仓库则克隆）。
    -   将项目解压到 `C:\Users\您的用户名\Desktop\yeap` 等位置。

2.  **打开终端**: 在您的终端（Windows 上为 PowerShell）中导航到项目根目录 (`yeap`)。
    -   在文件资源管理器中，右键单击 `yeap` 文件夹内部，然后选择"在此处打开终端"或"在此处打开 PowerShell 窗口"。

3.  **安装依赖**: Streamlit 应用程序需要特定的 Python 库。这些库列在 `streamlit/requirements.txt` 中。
    -   激活环境（如果需要）：
        ```bash
        # 如果您使用的是特定的 Python 环境，请在此处激活它。
        # 例如：conda activate myenv 或 .\.venv\Scripts\Activate.ps1
        ```
    -   安装所需的包：
        ```bash
        pip install -r streamlit/requirements.txt
        ```

4.  **在本地运行仪表板**: 您可以使用 `start_dashboard.py` 脚本快速启动。
    -   确保您的虚拟环境已激活。
    -   运行脚本：
        ```bash
        python start_dashboard.py
        ```
    -   此脚本将自动在您的默认网页浏览器中打开 `http://localhost:8501`（或类似地址），您的仪表板将在此处运行。

## 3. 页面结构

YEAP Dashboard 包含以下页面：

1. **🏠 Home** - 项目主页和概览
2. **📊 Overview** - 数据总览和基础统计
3. **📊 Outputs Count Statistics** - 产出数量统计分析
4. **🌱 Knowledge Development & Dissemination** - 知识发展与传播分析
5. **🔧 Technical Assistance** - 技术援助分析
6. **💪 Capacity Development** - 能力发展分析
7. **🤝 Advocacy & Partnerships** - 倡导与合作分析

### 独立页面标题系统

每个专项分析页面都有独立的主标题和副标题：
- **Outputs Count Statistics**: "📊 产出数量统计" / "统计各类产出的数量分布"
- **Knowledge Development & Dissemination**: "🌱 知识发展与传播" / "分析知识创造和传播活动"
- **Technical Assistance**: "🔧 技术援助" / "技术支持和援助项目分析"
- **Capacity Development**: "💪 能力发展" / "能力建设和培训项目分析"
- **Advocacy & Partnerships**: "🤝 倡导与合作" / "倡导活动和合作伙伴关系分析"

## 4. 从本地上传到 GitHub

本项目包含一个 PowerShell 脚本示例 (`upload_to_github_example.ps1`)，用于简化将代码上传到 GitHub 仓库的过程。

1.  **创建新的 GitHub 仓库**: 
    -   访问 [https://github.com/new](https://github.com/new)。
    -   选择一个仓库名称（例如，`YEAP-Dashboard`）。
    -   **重要**: 不要使用 README、.gitignore 或许可证初始化仓库。请将它们留空，因为您的项目已经包含这些文件。
    -   点击“创建仓库”。

2.  **在本地初始化 Git**: 如果您的项目文件夹尚未是 Git 仓库，您需要对其进行初始化。
    -   在 `yeap` 项目根目录中打开终端。
    -   初始化 Git：
        ```bash
        git init
        ```

3.  **将本地仓库链接到 GitHub**: 将您的本地仓库连接到新创建的 GitHub 仓库。
    -   在您的 GitHub 仓库页面上，复制 HTTPS URL（例如，`https://github.com/您的用户名/YEAP-Dashboard.git`）。
    -   在您的终端中，添加远程源：
        ```bash
        git remote add origin https://github.com/您的用户名/YEAP-Dashboard.git
        # 将 您的用户名 和 YEAP-Dashboard 替换为您的实际 GitHub 用户名和仓库名称
        ```
    -   如果您之前已初始化 Git 并链接到其他远程仓库，您可能需要先删除旧的远程仓库：
        ```bash
        git remote remove origin
        git remote add origin https://github.com/您的用户名/YEAP-Dashboard.git
        ```

4.  **运行上传脚本**: 
    -   **重要**: 在运行脚本之前，请将 `upload_to_github_example.ps1` 重命名为 `upload_to_github.ps1`，并打开该文件，将文件末尾的 GitHub 仓库 URL `https://github.com/your_username/your_repository.git` 替换为您自己仓库的实际 URL。
    -   确保您的终端位于 `yeap` 项目根目录中。
    -   执行 PowerShell 脚本：
        ```bash
        .\upload_to_github.ps1
        ```
    -   脚本将执行以下操作：
        -   检查 Git 状态。
        -   将所有更改添加到 Git。
        -   提示您输入提交消息（您可以按 Enter 键使用默认消息）。
        -   尝试正常推送。如果失败（例如，由于远程更改），它将自动尝试强制推送。
        -   成功推送后，它将显示您的 GitHub 仓库 URL 和一个用于检查 Streamlit Cloud 部署状态的链接。

## 5. 部署到 Streamlit Cloud

Streamlit Cloud 可以轻松地直接从 GitHub 部署您的 Streamlit 应用程序。

1.  **访问 Streamlit Cloud**: 打开您的网页浏览器并访问 [https://share.streamlit.io/](https://share.streamlit.io/)。

2.  **登录**: 使用您的 GitHub 账户登录。

3.  **部署应用程序**: 
    -   点击“New app”（新应用）按钮（通常在右上角）。
    -   选择“From existing repo”（从现有仓库）。

4.  **配置部署**: 
    -   **Repository (仓库)**: 选择您刚刚上传的 GitHub 仓库（例如，`您的用户名/YEAP-Dashboard`）。
    -   **Branch (分支)**: 选择 `main`（或 `master`，取决于您仓库的默认分支）。
    -   **Main file path (主文件路径)**: 输入 `streamlit/streamlit_app.py`（这是您的 Streamlit 应用程序的主文件）。
    -   **Python version (Python 版本)**: 选择一个兼容的 Python 版本（例如，`3.9` 或 `3.10`）。
    -   **Advanced settings (高级设置) (可选)**:
        -   **Secrets (密钥)**: 如果您的应用程序使用任何 API 密钥或敏感信息，您可以在此处添加。对于本项目，除非您添加外部数据源，否则可能不需要。
        -   **Custom command (自定义命令)**: 对于标准的 Streamlit 应用程序，通常不需要此项。

5.  **部署！**: 点击“Deploy!”（部署！）按钮。

    -   Streamlit Cloud 将开始构建和部署您的应用程序。此过程可能需要几分钟。
    -   部署完成后，您将获得一个可共享的仪表板公共 URL。



## 6. 故障排除

### 常见问题

1. **Python 依赖问题**
   - 确保您使用的是 Python 3.7 或更高版本
   - 如果遇到包安装问题，尝试升级 pip：`python -m pip install --upgrade pip`

2. **Streamlit 启动问题**
   - 检查端口 8501 是否被占用
   - 尝试使用不同端口：`streamlit run streamlit/streamlit_app.py --server.port 8502`

3. **GitHub 上传问题**
   - 确保您已正确配置 Git 用户名和邮箱
   - 检查网络连接和 GitHub 访问权限
   - 如果推送失败，可能需要先创建远程仓库

4. **数据文件问题**
   - 确保所有 CSV 文件都在 `orignaldata/` 文件夹中
   - 检查文件名是否与代码中的引用一致

### 获取帮助

如果您遇到其他问题，请：
1. 检查终端输出的错误信息
2. 确认所有文件路径正确
3. 了解数据结构
4. 查看 `YEAP 仪表板标题修改指南` 了解页面定制

---

就是这样！您现在已经成功在本地运行并部署了您的 YEAP Dashboard。

# YEAP 仪表板标题修改指南

## 概述
本文档提供基于搜索关键词的标题修改方法，不依赖具体行数，适应代码变化。

## 项目结构

### 主要文件
- `streamlit_app.py` - 主应用入口，包含导航菜单
- `st_landing_dashboard.py` - 首页概览仪表板
- `st_q6q7q10q11_dashboard.py` - 详细分析仪表板
- `st_styles.py` - 样式配置文件

## 标题类型与搜索方法

### 1. 页面主标题

#### 搜索关键词：`st.title(`
**位置：** `st_landing_dashboard.py` 和 `st_q6q7q10q11_dashboard.py`

**示例修改：**
```python
# 搜索：st.title("📊 General Overview")
# 修改为：st.title("📊 您的新标题")
```

### 2. 统一页面头部

#### 搜索关键词：`create_unified_header`
**位置：** `st_q6q7q10q11_dashboard.py`

**修改内容：**
- 主标题：搜索 `"ILO Youth Employment Action Plan (YEAP):"`
- 年份标题：搜索 `f"{selected_year} Reporting"`

### 3. 导航菜单标题

#### 搜索关键词：`PAGES = {`
**位置：** `streamlit_app.py`

**修改方法：**
```python
# 搜索 PAGES 字典
PAGES = {
    "🏠 Overview": st_landing_dashboard,  # 修改显示名称
    "📊 Clusters Of The Implementation Framework": st_q6q7q10q11_dashboard
}
```

### 4. 页面特定标题

#### 搜索关键词：`page_titles = {`
**位置：** `st_q6q7q10q11_dashboard.py`

**包含的标题：**
- "📊 Clusters Of The Implementation Framework"
- "📚 Knowledge Development & Dissemination"
- "🔧 Technical Assistance"
- "🎓 Capacity Development"
- "🤝 Advocacy & Partnerships"

### 5. 图表标题

#### 5.1 主要统计图表
**搜索关键词：** `"Number of Outputs Delivered by Cluster"`
**位置：** `st_q6q7q10q11_dashboard.py`

#### 5.2 Q2 饼图标题
**搜索关键词：** `"Distribution of Responses on Whether Entities Conducted Youth Employment Work"`
**位置：** `st_landing_dashboard.py`

#### 5.3 详细列表标题
**搜索关键词：** `"📋 Outputs Detail List"`
**位置：** `st_q6q7q10q11_dashboard.py`

### 6. 子标题和说明文本

#### 搜索关键词：`st.subheader(`
**位置：** 各个仪表板文件

#### 搜索关键词：`st.markdown("###`
**位置：** 各个仪表板文件

## 修改步骤

### 步骤1：确定要修改的标题类型
1. 页面主标题 → 搜索 `st.title(`
2. 导航菜单 → 搜索 `PAGES = {`
3. 图表标题 → 搜索具体标题文本
4. 子标题 → 搜索 `st.subheader(`

### 步骤2：使用搜索功能定位
1. 在IDE中使用 Ctrl+F 搜索关键词
2. 或使用全局搜索 Ctrl+Shift+F
3. 根据文件名和上下文确认正确位置

### 步骤3：修改标题内容
1. 保持原有的emoji图标（如📊、📚等）
2. 修改文字部分
3. 确保引号和语法正确

### 步骤4：验证修改
1. 保存文件
2. 重启Streamlit应用
3. 检查页面显示效果

## 常用搜索关键词速查

| 标题类型 | 搜索关键词 | 文件位置 |
|---------|-----------|----------|
| 页面主标题 | `st.title(` | `st_landing_dashboard.py`, `st_q6q7q10q11_dashboard.py` |
| 导航菜单 | `PAGES = {` | `streamlit_app.py` |
| 统一头部 | `create_unified_header` | `st_q6q7q10q11_dashboard.py` |
| 页面特定标题 | `page_titles = {` | `st_q6q7q10q11_dashboard.py` |
| 图表标题 | 具体标题文本 | 各仪表板文件 |
| 子标题 | `st.subheader(` | 各仪表板文件 |

## 注意事项

1. **保持一致性**：相关的标题要同步修改
2. **保留格式**：保持emoji图标和特殊格式
3. **测试验证**：修改后要重启应用测试
4. **备份文件**：重要修改前建议备份
5. **字符编码**：注意中文字符的正确显示

## 常见问题

### Q: 修改后标题不显示？
A: 检查语法错误，确保引号匹配，重启Streamlit应用

### Q: 导航菜单修改无效？
A: 确保修改了 `streamlit_app.py` 中的 `PAGES` 字典

### Q: 图表标题在多处出现？
A: 使用全局搜索找到所有位置，逐一修改

### Q: 如何批量修改相似标题？
A: 使用IDE的查找替换功能，但要谨慎操作

