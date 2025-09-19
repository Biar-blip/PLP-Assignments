# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
from datetime import datetime
import re  # Added for better text processing

# Set page configuration
st.set_page_config(
    page_title="CORD-19 Research Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .stDownloadButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">CORD-19 Research Dataset Analysis</h1>', unsafe_allow_html=True)

# Introduction
st.write("""
This interactive dashboard provides an analysis of the COVID-19 Open Research Dataset (CORD-19), 
which contains scholarly articles about COVID-19, SARS-CoV-2, and related coronaviruses.
""")

# File uploader option
uploaded_file = st.sidebar.file_uploader("Upload metadata.csv", type="csv")

# Load data function with caching
@st.cache_data
def load_data(file_path=None, uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, low_memory=False)
    else:
        # Try to load the data from different possible paths
        try:
            df = pd.read_csv('data/metadata.csv', low_memory=False)
        except FileNotFoundError:
            try:
                df = pd.read_csv('metadata.csv', low_memory=False)
            except FileNotFoundError:
                st.error("""
                Could not find the metadata.csv file. Please download it from Kaggle:
                https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge
                
                And place it in the 'data' folder or in the root directory of this application.
                Alternatively, you can upload it using the file uploader in the sidebar.
                """)
                return None
    
    # Data preprocessing
    # Convert publish_time to datetime
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    
    # Extract year from publish_time
    df['year'] = df['publish_time'].dt.year
    df['year'] = df['year'].fillna(0).astype(int)  # Handle NaN values
    
    # Fill missing abstracts with empty string
    df['abstract'] = df['abstract'].fillna('')
    
    # Filter out papers without titles
    df = df[df['title'].notna()]
    
    return df

# Load the data
df = load_data(uploaded_file=uploaded_file)

if df is not None:
    # Sidebar for filters
    st.sidebar.title("Filters")
    
    # Year filter - handle cases where year might be 0
    valid_years = df[df['year'] > 0]['year']
    if len(valid_years) > 0:
        min_year = int(valid_years.min())
        max_year = int(valid_years.max())
        year_range = st.sidebar.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
    else:
        st.sidebar.warning("No valid years found in the dataset")
        year_range = (0, 0)
    
    # Source filter
    if 'source_x' in df.columns:
        sources = df['source_x'].dropna().unique()
        selected_sources = st.sidebar.multiselect(
            "Select Sources",
            options=sources,
            default=sources[:min(5, len(sources))] if len(sources) > 0 else []
        )
    else:
        st.sidebar.warning("No 'source_x' column found in the dataset")
        selected_sources = []
    
    # Apply filters
    if year_range != (0, 0) and len(selected_sources) > 0:
        filtered_df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1]) &
            (df['source_x'].isin(selected_sources))
        ]
    elif year_range != (0, 0):
        filtered_df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1])
        ]
    elif len(selected_sources) > 0:
        filtered_df = df[df['source_x'].isin(selected_sources)]
    else:
        filtered_df = df
    
    # Display dataset info
    st.sidebar.write(f"Total papers: {len(df):,}")
    st.sidebar.write(f"Filtered papers: {len(filtered_df):,}")
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h2 class="section-header">Dataset Overview</h2>', unsafe_allow_html=True)
        
        # Basic statistics
        st.subheader("Basic Statistics")
        st.write(f"Total number of papers: {len(df):,}")
        st.write(f"Number of papers with abstracts: {df['abstract'].str.len().gt(0).sum():,}")
        
        # Handle date range display
        valid_dates = df[df['publish_time'].notna()]['publish_time']
        if len(valid_dates) > 0:
            min_date = valid_dates.min().strftime('%Y-%m-%d')
            max_date = valid_dates.max().strftime('%Y-%m-%d')
            st.write(f"Date range: {min_date} to {max_date}")
        else:
            st.write("No valid dates found in the dataset")
        
        # Top journals
        st.subheader("Top 10 Journals")
        if 'journal' in df.columns:
            top_journals = df['journal'].value_counts().head(10)
            if len(top_journals) > 0:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax)
                ax.set_xlabel('Number of Papers')
                ax.set_ylabel('Journal')
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.write("No journal data available")
        else:
            st.write("No 'journal' column found in the dataset")
    
    with col2:
        st.markdown('<h2 class="section-header">Temporal Analysis</h2>', unsafe_allow_html=True)
        
        # Publications over time
        st.subheader("Publications Over Time")
        valid_dates = df[df['publish_time'].notna()]['publish_time']
        if len(valid_dates) > 0:
            publications_by_time = valid_dates.dt.to_period('M').value_counts().sort_index()
            publications_by_time.index = publications_by_time.index.astype(str)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            publications_by_time.plot(ax=ax)
            ax.set_xlabel('Time (Monthly)')
            ax.set_ylabel('Number of Publications')
            ax.tick_params(axis='x', rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.write("No date data available for temporal analysis")
    
    # Word cloud of abstracts
    st.markdown('<h2 class="section-header">Word Cloud of Abstracts</h2>', unsafe_allow_html=True)
    
    # Generate word cloud
    if len(filtered_df) > 0 and filtered_df['abstract'].str.len().sum() > 0:
        text = ' '.join(filtered_df['abstract'].astype(str))
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.write("No abstract data available for word cloud")
    
    # Top authors
    st.markdown('<h2 class="section-header">Top Authors</h2>', unsafe_allow_html=True)
    
    # Process authors
    if 'authors' in df.columns:
        authors = df['authors'].dropna()
        all_authors = []
        for author_list in authors:
            try:
                if isinstance(author_list, str):
                    # Improved author extraction with regex
                    authors_split = re.split(r'[;,]|\band\b', author_list)
                    for author in authors_split:
                        author_clean = author.strip().replace('[', '').replace(']', '').replace("'", "").replace('"', '')
                        if author_clean and len(author_clean) > 2:  # Filter out very short strings
                            all_authors.append(author_clean)
            except:
                continue
        
        if all_authors:
            author_counts = pd.Series(all_authors).value_counts().head(15)
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.barplot(x=author_counts.values, y=author_counts.index, ax=ax)
            ax.set_xlabel('Number of Papers')
            ax.set_ylabel('Author')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.write("No author data available")
    else:
        st.write("No 'authors' column found in the dataset")
    
    # Interactive exploration
    st.markdown('<h2 class="section-header">Interactive Exploration</h2>', unsafe_allow_html=True)
    
    # Show sample data
    if st.checkbox("Show Sample Data"):
        columns_to_show = [col for col in ['title', 'authors', 'journal', 'publish_time'] if col in filtered_df.columns]
        if columns_to_show:
            st.dataframe(filtered_df[columns_to_show].head(10))
        else:
            st.write("No relevant columns available for display")
    
    # Search functionality
    st.subheader("Search Papers")
    search_term = st.text_input("Enter search term (title or abstract):")
    
    if search_term:
        search_columns = []
        if 'title' in filtered_df.columns:
            search_columns.append(filtered_df['title'].str.contains(search_term, case=False, na=False))
        if 'abstract' in filtered_df.columns:
            search_columns.append(filtered_df['abstract'].str.contains(search_term, case=False, na=False))
        
        if search_columns:
            # Combine search conditions
            search_condition = search_columns[0]
            for condition in search_columns[1:]:
                search_condition = search_condition | condition
            
            search_results = filtered_df[search_condition]
            st.write(f"Found {len(search_results)} papers matching '{search_term}'")
            
            if len(search_results) > 0:
                for idx, row in search_results.head(5).iterrows():
                    with st.expander(row.get('title', 'No title')):
                        if 'authors' in row:
                            st.write(f"**Authors:** {row['authors']}")
                        if 'journal' in row:
                            st.write(f"**Journal:** {row['journal']}")
                        if 'publish_time' in row:
                            st.write(f"**Published:** {row['publish_time']}")
                        if 'abstract' in row:
                            st.write(f"**Abstract:** {row['abstract'][:500]}...")
        else:
            st.write("No searchable columns available")
    
    # Download button for filtered data
    st.sidebar.markdown("---")
    if len(filtered_df) > 0:
        csv = filtered_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_cord19_data.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.warning("No data available to download")

else:
    st.info("Please upload the metadata.csv file using the sidebar uploader to proceed with the analysis.")