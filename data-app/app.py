import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))
from core.cleaner import DataCleaner
from core.analyzer import DataAnalyzer

# Page config
st.set_page_config(
    page_title="Data Cleaner",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with responsive design
st.markdown("""
<style>
    /* Base styles */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Tablet styles (768px - 1024px) */
    @media (max-width: 1024px) and (min-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .block-container {
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] {
            width: 250px;
        }
        
        .stMetric {
            font-size: 0.9rem;
        }
    }
    
    /* Mobile styles (max 767px) */
    @media (max-width: 767px) {
        .main-header {
            font-size: 1.8rem;
            text-align: center;
        }
        
        .block-container {
            padding: 1rem 0.5rem;
        }
        
        [data-testid="stSidebar"] {
            width: 100%;
        }
        
        .stMetric {
            font-size: 0.85rem;
        }
        
        .stMetric label {
            font-size: 0.75rem;
        }
        
        .stButton>button {
            padding: 0.75rem 1rem;
            font-size: 0.9rem;
        }
        
        /* Stack columns on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        
        /* Better spacing for mobile */
        .element-container {
            margin-bottom: 0.5rem;
        }
        
        /* Adjust dataframe for mobile */
        .stDataFrame {
            font-size: 0.75rem;
        }
        
        /* Radio buttons horizontal on mobile */
        .stRadio > div {
            flex-direction: column;
        }
    }
    
    /* Desktop large screens (1440px+) */
    @media (min-width: 1440px) {
        .block-container {
            max-width: 1400px;
            padding: 3rem 2rem;
        }
        
        .main-header {
            font-size: 3.5rem;
        }
    }
    
    /* Touch-friendly improvements */
    @media (hover: none) and (pointer: coarse) {
        .stButton>button {
            padding: 0.75rem 1.5rem;
            min-height: 44px;
        }
        
        .stCheckbox {
            min-height: 44px;
        }
        
        .stRadio label {
            padding: 0.5rem;
        }
    }
    
    /* Smooth transitions */
    * {
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None
if 'issues' not in st.session_state:
    st.session_state.issues = []
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = {}

# Header with responsive subtitle
st.markdown('<h1 class="main-header"><span style="-webkit-text-fill-color: initial;">🧹</span> Data Cleaner</h1>', unsafe_allow_html=True)
st.markdown("### Transform messy data into clean, analysis-ready datasets")

# Sidebar with responsive navigation
with st.sidebar:
    st.title("Navigation")
    
    # Use tabs for better mobile experience
    page = st.radio(
        "Choose a step:",
        ["📤 Upload Data", "🔍 Analyze", "🧹 Clean", "📊 Results", "💾 Export"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Progress indicator
    steps = ["📤 Upload Data", "🔍 Analyze", "🧹 Clean", "📊 Results", "💾 Export"]
    current_step = steps.index(page) + 1
    st.progress(current_step / len(steps))
    st.caption(f"Step {current_step} of {len(steps)}")
    
    st.divider()
    st.caption("Made with ❤️ using Streamlit")
    st.caption("📱 Optimized for all devices")

# Page: Upload Data
if page == "📤 Upload Data":
    st.header("📤 Upload Your Data")
    
    # Responsive layout - stack on mobile
    if st.session_state.get('compact_mode', False):
        cols = st.columns(1)
    else:
        cols = st.columns([2, 1])
    
    with cols[0]:
        uploaded_file = st.file_uploader(
            "Drop your CSV or Excel file here",
            type=['csv', 'xlsx', 'xls'],
            help="Supported formats: CSV, Excel"
        )
        
        if uploaded_file:
            try:
                with st.spinner("Loading and analyzing file..."):
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                
                st.session_state.df = df
                
                # Auto-detect issues
                analyzer = DataAnalyzer(df)
                issues, recommendations = analyzer.auto_detect_issues()
                quality_score = analyzer.get_data_quality_score()
                
                st.session_state.issues = issues
                st.session_state.recommendations = recommendations
                
                st.success(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns")
                
                # Show quality score
                col_score1, col_score2, col_score3 = st.columns([1, 2, 1])
                with col_score2:
                    if quality_score >= 80:
                        score_color = "🟢"
                        score_text = "Excellent"
                    elif quality_score >= 60:
                        score_color = "🟡"
                        score_text = "Good"
                    elif quality_score >= 40:
                        score_color = "�"
                        score_text = "Fair"
                    else:
                        score_color = "�"
                        score_text = "Needs Cleaning"
                    
                    st.metric(
                        "Data Quality Score",
                        f"{score_color} {quality_score:.0f}/100",
                        score_text
                    )
                
                # Show detected issues
                if issues:
                    st.warning(f"⚠️ Detected {len(issues)} data quality issues")
                    
                    with st.expander("🔍 View Detected Issues", expanded=True):
                        for issue in issues:
                            severity_icon = "🔴" if issue['severity'] == 'high' else "🟡" if issue['severity'] == 'medium' else "🟢"
                            st.markdown(f"{severity_icon} **{issue['message']}**")
                            st.caption(f"💡 Recommendation: {issue['recommendation']}")
                            st.divider()
                        
                        st.info("👉 Go to the 'Clean' tab to apply recommended fixes automatically!")
                else:
                    st.success("✨ No major issues detected! Your data looks clean.")
                
                with st.expander("👀 Preview Data", expanded=False):
                    st.dataframe(df.head(10), use_container_width=True, height=300)
                    
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
    
    if len(cols) > 1:
        with cols[1]:
            st.info("""
            **Tips:**
            - Max file size: 200MB
            - CSV files load faster
            - First row should be headers
            """)
    else:
        with st.expander("💡 Tips"):
            st.info("""
            - Max file size: 200MB
            - CSV files load faster
            - First row should be headers
            """)

# Page: Analyze
elif page == "🔍 Analyze":
    st.header("🔍 Data Analysis")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first!")
    else:
        df = st.session_state.df
        analyzer = DataAnalyzer(df)
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Rows", f"{len(df):,}")
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
            st.metric("Missing Data", f"{missing_pct:.1f}%")
        with col4:
            duplicates = df.duplicated().sum()
            st.metric("Duplicates", duplicates)
        
        st.divider()
        
        # Missing data visualization - responsive
        if st.session_state.get('compact_mode', False):
            # Stack vertically on mobile/compact mode
            st.subheader("Missing Values by Column")
            missing_data = analyzer.get_missing_summary()
            if not missing_data.empty:
                fig = px.bar(
                    missing_data,
                    x='column',
                    y='missing_percentage',
                    color='missing_percentage',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(showlegend=False, height=300, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✨ No missing values found!")
            
            st.subheader("Data Types")
            dtype_counts = df.dtypes.value_counts()
            fig = px.pie(
                values=dtype_counts.values,
                names=dtype_counts.index.astype(str),
                hole=0.4
            )
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Side by side on desktop/tablet
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Missing Values by Column")
                missing_data = analyzer.get_missing_summary()
                if not missing_data.empty:
                    fig = px.bar(
                        missing_data,
                        x='column',
                        y='missing_percentage',
                        color='missing_percentage',
                        color_continuous_scale='Reds'
                    )
                    fig.update_layout(showlegend=False, height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.success("✨ No missing values found!")
            
            with col2:
                st.subheader("Data Types")
                dtype_counts = df.dtypes.value_counts()
                fig = px.pie(
                    values=dtype_counts.values,
                    names=dtype_counts.index.astype(str),
                    hole=0.4
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Detailed column info
        with st.expander("📋 Detailed Column Information"):
            col_info = analyzer.get_column_info()
            st.dataframe(col_info, use_container_width=True)

# Page: Clean
elif page == "🧹 Clean":
    st.header("🧹 Clean Your Data")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first!")
    else:
        df = st.session_state.df.copy()
        cleaner = DataCleaner(df)
        
        # Show AI recommendations
        recommendations = st.session_state.recommendations
        issues = st.session_state.issues
        
        if issues:
            st.info(f"🤖 **Smart Recommendations:** Found {len(issues)} issues that need attention")
            st.divider()
        
        st.subheader("Select Cleaning Operations")
        
        # Get recommended values
        rec = recommendations
        default_missing_strategy = rec.get('missing_strategy', 'Drop rows')
        
        # Responsive layout for cleaning options
        if st.session_state.get('compact_mode', False):
            # Single column on mobile
            remove_duplicates = st.checkbox(
                "🔄 Remove Duplicate Rows", 
                value=rec.get('remove_duplicates', False),
                help="✅ Recommended" if rec.get('remove_duplicates') else None
            )
            handle_missing = st.checkbox(
                "🔧 Handle Missing Values", 
                value=rec.get('handle_missing', False),
                help="✅ Recommended" if rec.get('handle_missing') else None
            )
            
            if handle_missing:
                strategies = ["Drop rows", "Fill with mean", "Fill with median", "Fill with mode", "Forward fill"]
                default_idx = strategies.index(default_missing_strategy) if default_missing_strategy in strategies else 0
                missing_strategy = st.selectbox(
                    "Strategy for missing values:",
                    strategies,
                    index=default_idx
                )
            
            remove_outliers = st.checkbox(
                "� Remove Outliers (numeric columns)",
                value=rec.get('remove_outliers', False),
                help="✅ Recommended" if rec.get('remove_outliers') else None
            )
            standardize_text = st.checkbox(
                "✏️ Standardize Text (trim, lowercase)",
                value=rec.get('standardize_text', False),
                help="✅ Recommended" if rec.get('standardize_text') else None
            )
            convert_types = st.checkbox(
                "🔢 Auto-convert Data Types",
                value=rec.get('convert_types', False),
                help="✅ Recommended" if rec.get('convert_types') else None
            )
        else:
            # Two columns on desktop/tablet
            col1, col2 = st.columns(2)
            
            with col1:
                remove_duplicates = st.checkbox(
                    "🔄 Remove Duplicate Rows", 
                    value=rec.get('remove_duplicates', False),
                    help="✅ Recommended" if rec.get('remove_duplicates') else None
                )
                handle_missing = st.checkbox(
                    "🔧 Handle Missing Values", 
                    value=rec.get('handle_missing', False),
                    help="✅ Recommended" if rec.get('handle_missing') else None
                )
                
                if handle_missing:
                    strategies = ["Drop rows", "Fill with mean", "Fill with median", "Fill with mode", "Forward fill"]
                    default_idx = strategies.index(default_missing_strategy) if default_missing_strategy in strategies else 0
                    missing_strategy = st.selectbox(
                        "Strategy for missing values:",
                        strategies,
                        index=default_idx
                    )
            
            with col2:
                remove_outliers = st.checkbox(
                    "📊 Remove Outliers (numeric columns)",
                    value=rec.get('remove_outliers', False),
                    help="✅ Recommended" if rec.get('remove_outliers') else None
                )
                standardize_text = st.checkbox(
                    "✏️ Standardize Text (trim, lowercase)",
                    value=rec.get('standardize_text', False),
                    help="✅ Recommended" if rec.get('standardize_text') else None
                )
                convert_types = st.checkbox(
                    "🔢 Auto-convert Data Types",
                    value=rec.get('convert_types', False),
                    help="✅ Recommended" if rec.get('convert_types') else None
                )
        
        st.divider()
        
        if st.button("🚀 Start Cleaning", type="primary"):
            with st.spinner("Cleaning in progress..."):
                cleaned_df = df.copy()
                operations = []
                
                if remove_duplicates:
                    before = len(cleaned_df)
                    cleaned_df = cleaner.remove_duplicates(cleaned_df)
                    removed = before - len(cleaned_df)
                    operations.append(f"✅ Removed {removed} duplicate rows")
                
                if handle_missing:
                    cleaned_df = cleaner.handle_missing(cleaned_df, missing_strategy)
                    operations.append(f"✅ Handled missing values using: {missing_strategy}")
                
                if remove_outliers:
                    cleaned_df = cleaner.remove_outliers(cleaned_df)
                    operations.append("✅ Removed outliers from numeric columns")
                
                if standardize_text:
                    cleaned_df = cleaner.standardize_text(cleaned_df)
                    operations.append("✅ Standardized text columns")
                
                if convert_types:
                    cleaned_df = cleaner.convert_types(cleaned_df)
                    operations.append("✅ Converted data types")
                
                st.session_state.cleaned_df = cleaned_df
                
                st.success("🎉 Cleaning completed!")
                for op in operations:
                    st.write(op)

# Page: Results
elif page == "📊 Results":
    st.header("📊 Cleaning Results")
    
    if st.session_state.cleaned_df is None:
        st.warning("⚠️ Please clean your data first!")
    else:
        original_df = st.session_state.df
        cleaned_df = st.session_state.cleaned_df
        
        # Comparison metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Rows",
                f"{len(cleaned_df):,}",
                f"{len(cleaned_df) - len(original_df):,}"
            )
        
        with col2:
            original_missing = original_df.isnull().sum().sum()
            cleaned_missing = cleaned_df.isnull().sum().sum()
            st.metric(
                "Missing Values",
                cleaned_missing,
                f"{cleaned_missing - original_missing:,}"
            )
        
        with col3:
            original_dupes = original_df.duplicated().sum()
            cleaned_dupes = cleaned_df.duplicated().sum()
            st.metric(
                "Duplicates",
                cleaned_dupes,
                f"{cleaned_dupes - original_dupes:,}"
            )
        
        st.divider()
        
        # Side by side comparison - responsive
        if st.session_state.get('compact_mode', False):
            # Tabs for mobile
            tab1, tab2 = st.tabs(["📥 Original", "✨ Cleaned"])
            
            with tab1:
                st.dataframe(original_df.head(10), use_container_width=True, height=400)
            
            with tab2:
                st.dataframe(cleaned_df.head(10), use_container_width=True, height=400)
        else:
            # Side by side on desktop/tablet
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📥 Original Data")
                st.dataframe(original_df.head(10), use_container_width=True)
            
            with col2:
                st.subheader("✨ Cleaned Data")
                st.dataframe(cleaned_df.head(10), use_container_width=True)

# Page: Export
elif page == "💾 Export":
    st.header("💾 Export Cleaned Data")
    
    if st.session_state.cleaned_df is None:
        st.warning("⚠️ Please clean your data first!")
    else:
        cleaned_df = st.session_state.cleaned_df
        
        # Responsive export layout
        if st.session_state.get('compact_mode', False):
            cols = st.columns(1)
        else:
            cols = st.columns([2, 1])
        
        with cols[0]:
            st.subheader("Choose Export Format")
            
            export_format = st.radio(
                "Format:",
                ["CSV", "Excel", "JSON"],
                horizontal=True
            )
            
            filename = st.text_input("Filename:", value="cleaned_data")
            
            # Generate export data
            try:
                if export_format == "CSV":
                    data = cleaned_df.to_csv(index=False).encode('utf-8')
                    mime = 'text/csv'
                    ext = 'csv'
                elif export_format == "Excel":
                    from io import BytesIO
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        cleaned_df.to_excel(writer, index=False, sheet_name='Cleaned Data')
                    data = buffer.getvalue()
                    mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    ext = 'xlsx'
                else:  # JSON
                    data = cleaned_df.to_json(orient='records', indent=2).encode('utf-8')
                    mime = 'application/json'
                    ext = 'json'
                
                st.download_button(
                    label=f"⬇️ Download {export_format}",
                    data=data,
                    file_name=f"{filename}.{ext}",
                    mime=mime,
                    type="primary",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Export error: {str(e)}")
                st.info("💡 Try a different format or check your data")
        
        if len(cols) > 1:
            with cols[1]:
                st.info(f"""
                **Export Summary:**
                - Rows: {len(cleaned_df):,}
                - Columns: {len(cleaned_df.columns)}
                - Format: {export_format}
                """)
        else:
            st.info(f"""
            **Export Summary:** {len(cleaned_df):,} rows × {len(cleaned_df.columns)} columns
            """)
