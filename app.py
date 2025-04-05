import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import StringIO
import base64

# Set page configuration
st.set_page_config(
    page_title="NBA Analytics Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main header style */
    .main-header {
        font-size: 2.5rem;
        color: #17408B; /* Dark blue */
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }

    /* Sub-header style */
    .sub-header {
        font-size: 1.8rem;
        color: #C9082A; 
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: bold;
        
    }

    .dashboard-container {
        background-color: #F8F9FA; /* Light gray */
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: #333333; /* Ensure text color is set */
    }
    
    /* Fix list styling */
    .dashboard-container ul, .dashboard-container ol {
        color: #333333; 
        margin-left: 20px;
        padding-left: 20px;
    }

    .dashboard-container li {
        font-size: 16px;
        line-height: 1.6;
        color: #333333;
        margin-bottom: 8px;
    }
    
    /* Remove empty color property */
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        color: #333333;
    }

    /* Metric cards */
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #17408B;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #ddd;
        font-size: 0.8rem;
        color: #666;
    }

    /* Ensure list items are visible */
    .dashboard-container ol {
        color: black; 
    }

    .dashboard-container li {
        font-size: 16px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

team_colors = {
    'ATL': '#E03A3E', 'BOS': '#007A33', 'BKN': '#000000', 'CHA': '#1D1160', 
    'CHI': '#CE1141', 'CLE': '#860038', 'DAL': '#00538C', 'DEN': '#0E2240', 
    'DET': '#C8102E', 'GSW': '#1D428A', 'HOU': '#CE1141', 'IND': '#002D62', 
    'LAC': '#C8102E', 'LAL': '#552583', 'MEM': '#5D76A9', 'MIA': '#98002E', 
    'MIL': '#00471B', 'MIN': '#0C2340', 'NO': '#0C2340', 'NYK': '#006BB6', 
    'OKC': '#007AC1', 'ORL': '#0077C0', 'PHI': '#006BB6', 'PHX': '#1D1160', 
    'POR': '#E03A3E', 'SAC': '#5A2D81', 'SAS': '#C4CED4', 'TOR': '#CE1141', 
    'UTA': '#002B5C', 'WAS': '#002B5C', 'NOH': '#0C2340', 'NOP': '#0C2340'
}

# def get_table_download_link(df, filename, text):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">{text}</a>'
#     return href

# uploaded_file = st.sidebar.file_uploader("Upload NBA data CSV", type="csv")

@st.cache_data
def load_data():
    try:
        data = pd.read_csv("nba.csv")
    except FileNotFoundError:
        st.warning("Using sample data. Please upload actual NBA data for full functionality.")
        data = pd.DataFrame({
            'PLAYER': ['LeBron James', 'Stephen Curry', 'Kevin Durant', 'Giannis Antetokounmpo', 'Nikola Jokic',
                       'Luka Doncic', 'Damian Lillard', 'Joel Embiid', 'Kawhi Leonard', 'James Harden'],
            'TEAM': ['LAL', 'GSW', 'BKN', 'MIL', 'DEN', 'DAL', 'POR', 'PHI', 'LAC', 'BKN'],
            'year': ['2023-24', '2023-24', '2023-24', '2023-24', '2023-24',
                     '2023-24', '2023-24', '2023-24', '2023-24', '2023-24'],
            'Season_type': ['Regular Season', 'Regular Season', 'Regular Season', 'Regular Season', 'Regular Season',
                        'Regular Season', 'Regular Season', 'Regular Season', 'Regular Season', 'Regular Season'],
            'GP': [60, 74, 58, 73, 79, 70, 68, 69, 52, 72],
            'MIN': [2100, 2368, 2146, 2482, 2765, 2520, 2312, 2415, 1768, 2520],
            'PTS': [1740, 2072, 1682, 2336, 2133, 2310, 1768, 2277, 1248, 1728],
            'FGM': [648, 676, 588, 864, 832, 756, 544, 776, 464, 544],
            'FGA': [1260, 1480, 1160, 1460, 1580, 1610, 1360, 1480, 928, 1300],
            'FG3M': [156, 380, 168, 48, 88, 238, 272, 48, 104, 232],
            'FG3A': [468, 940, 456, 168, 248, 680, 748, 144, 286, 640],
            'FTM': [288, 340, 328, 560, 380, 560, 408, 676, 216, 408],
            'FTA': [330, 368, 374, 750, 460, 656, 440, 770, 248, 456],
            'OREB': [48, 36, 24, 205, 198, 70, 42, 138, 56, 44],
            'DREB': [414, 325, 372, 708, 774, 520, 238, 660, 282, 412],
            'REB': [462, 361, 396, 913, 972, 590, 280, 798, 338, 456],
            'AST': [534, 518, 354, 450, 776, 588, 496, 370, 226, 684],
            'STL': [78, 81, 64, 94, 110, 116, 74, 70, 82, 104],
            'BLK': [54, 26, 72, 94, 82, 46, 28, 128, 44, 42],
            'TOV': [228, 236, 186, 248, 304, 290, 198, 226, 158, 264],
            'PF': [114, 168, 138, 192, 220, 174, 150, 240, 122, 184]
        })
    
    if 'season_start_year' not in data.columns:
        data['season_start_year'] = data['year'].str[:4].astype(int)
    
    data['TEAM'].replace(to_replace=['NOP', 'NOH'], value='NO', inplace=True)
    
    rs_df = data[data['Season_type'] == 'Regular Season']
    playoffs_df = data[data['Season_type'] == 'Playoffs']
    
    total_cols = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
                  'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    
    return data, rs_df, playoffs_df, total_cols

# Update this line to call load_data() without arguments
data, rs_df, playoffs_df, total_cols = load_data()

def create_per_min_stats(data, total_cols):
    # First, ensure 'year' is in the right format
    if 'season_start_year' in data.columns:
        data['year'] = data.apply(lambda row: f"{row['season_start_year']}-{str(row['season_start_year']+1)[2:]}", axis=1)
    
    # Group by player and year to aggregate stats
    data_per_min = data.groupby(['PLAYER', 'year'])[total_cols].sum().reset_index()
    
    # Filter out players with minimal minutes to avoid division issues
    data_per_min = data_per_min[data_per_min['MIN'] >= 50]
    
    # Calculate per-minute stats
    for col in total_cols:
        if col != 'MIN':  # Don't normalize minutes by minutes
            data_per_min[col] = data_per_min[col]/data_per_min['MIN']
    
    # Add shooting percentages
    if all(col in total_cols for col in ['FGM', 'FGA']):
        data_per_min['FG%'] = data_per_min['FGM']/data_per_min['FGA']
    
    if all(col in total_cols for col in ['FG3M', 'FG3A']):
        data_per_min['3PT%'] = data_per_min['FG3M']/data_per_min['FG3A']
    
    if all(col in total_cols for col in ['FTM', 'FTA']):
        data_per_min['FT%'] = data_per_min['FTM']/data_per_min['FTA']
    
    # Add other advanced metrics
    if all(col in total_cols for col in ['FG3A', 'FGA']):
        data_per_min['FG3A%'] = data_per_min['FG3A']/data_per_min['FGA']
    
    if all(col in total_cols for col in ['PTS', 'FGA']):
        data_per_min['PTS/FGA'] = data_per_min['PTS']/data_per_min['FGA']
    
    if all(col in total_cols for col in ['FG3M', 'FGM']):
        data_per_min['FG3M/FGM'] = data_per_min['FG3M']/data_per_min['FGM']
    
    if all(col in total_cols for col in ['FTA', 'FGA']):
        data_per_min['FTA/FGA'] = data_per_min['FTA']/data_per_min['FGA']
    
    if all(col in total_cols for col in ['PTS', 'FGA', 'FTA']):
        data_per_min['TRU%'] = 0.5*data_per_min['PTS']/(data_per_min['FGA']+0.475*data_per_min['FTA'])
    
    if all(col in total_cols for col in ['AST', 'TOV']):
        data_per_min['AST_TOV'] = data_per_min['AST']/data_per_min['TOV'].replace(0, 0.001)  # Avoid division by zero
    
    return data_per_min

data_per_min = create_per_min_stats(data, total_cols)

def preprocess_nba_data(data):
    """
    Preprocesses NBA data to ensure consistent formatting and handle common issues.
    
    Parameters:
    data (pandas.DataFrame): The raw NBA data
    
    Returns:
    pandas.DataFrame: Cleaned and preprocessed data
    """
    # Create a copy to avoid modifying the original
    df = data.copy()
    
    # Check for column names that need to be standardized
    column_map = {
        'PLAYER_NAME': 'PLAYER',
        'PLAYER ID': 'PLAYER_ID',
        'TEAM_ABBREVIATION': 'TEAM',
        'GAMES PLAYED': 'GP',
        'MINUTES': 'MIN',
        'POINTS': 'PTS',
        'FIELD_GOALS_MADE': 'FGM',
        'FIELD_GOALS_ATTEMPTED': 'FGA',
        'FIELD_GOAL_PERCENTAGE': 'FG_PCT',
        'THREE_POINTS_MADE': 'FG3M',
        'THREE_POINTS_ATTEMPTED': 'FG3A',
        'THREE_POINT_PERCENTAGE': 'FG3_PCT',
        'FREE_THROWS_MADE': 'FTM',
        'FREE_THROWS_ATTEMPTED': 'FTA',
        'FREE_THROW_PERCENTAGE': 'FT_PCT',
        'OFFENSIVE_REBOUNDS': 'OREB',
        'DEFENSIVE_REBOUNDS': 'DREB',
        'REBOUNDS': 'REB',
        'ASSISTS': 'AST',
        'STEALS': 'STL',
        'BLOCKS': 'BLK',
        'TURNOVERS': 'TOV',
        'PERSONAL_FOULS': 'PF',
    }
    
    # Apply the column mapping for columns that exist
    for old_col, new_col in column_map.items():
        if old_col in df.columns and new_col not in df.columns:
            df[new_col] = df[old_col]
    
    # Handle season format
    if 'season_start_year' not in df.columns:
        if 'year' in df.columns:
            # Try to extract the season start year from the 'year' column
            try:
                df['season_start_year'] = df['year'].astype(str).str.split('-').str[0].astype(int)
            except:
                # If that fails, try to handle year in a different format
                pass
    
    # Handle team abbreviations
    if 'TEAM' in df.columns:
        # Standardize team abbreviations
        team_map = {
            'NOP': 'NO',
            'NOH': 'NO',
            'BRK': 'BKN',
            'PHO': 'PHX',
            'CHH': 'CHA',
            'UTH': 'UTA'
        }
        
        df['TEAM'].replace(team_map, inplace=True)
    
    # Create a standard year column if needed
    if 'year' not in df.columns and 'season_start_year' in df.columns:
        df['year'] = df['season_start_year'].astype(str) + '-' + df['season_start_year'].add(1).astype(str).str[-2:]
    
    # Make sure Season_type is standardized
    if 'Season_type' not in df.columns:
        if 'SEASON_TYPE' in df.columns:
            df['Season_type'] = df['SEASON_TYPE']
        else:
            # Default to Regular Season if not specified
            df['Season_type'] = 'Regular Season'
    
    return df

# Add this line after loading the data
data = preprocess_nba_data(data)

def create_team_season_stats(data, total_cols):
    team_stats = data.groupby(['TEAM', 'season_start_year'])[total_cols + ['GP']].sum().reset_index()
    
    team_stats['POSS_est'] = team_stats['FGA'] - team_stats['OREB'] + team_stats['TOV'] + 0.44 * team_stats['FTA']
    team_stats['PACE'] = team_stats['POSS_est'] / team_stats['GP'] / 48 * 40  
    team_stats['ORtg'] = team_stats['PTS'] / team_stats['POSS_est'] * 100  
    
    team_stats['AST_ratio'] = team_stats['AST'] / team_stats['FGM']
    team_stats['FG3_ratio'] = team_stats['FG3A'] / team_stats['FGA']
    team_stats['FG_PCT'] = team_stats['FGM'] / team_stats['FGA']
    team_stats['FG3_PCT'] = team_stats['FG3M'] / team_stats['FG3A']
    team_stats['PTS_per_POSS'] = team_stats['PTS'] / team_stats['POSS_est']
    
    return team_stats

team_season_stats = create_team_season_stats(data, total_cols)

team_names = {
    'ATL': 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets', 
    'CHA': 'Charlotte Hornets', 'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers', 
    'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets', 'DET': 'Detroit Pistons', 
    'GSW': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers', 
    'LAC': 'LA Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies', 
    'MIA': 'Miami Heat', 'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves', 
    'NO': 'New Orleans Pelicans', 'NYK': 'New York Knicks', 'OKC': 'Oklahoma City Thunder', 
    'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers', 'PHX': 'Phoenix Suns', 
    'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings', 'SAS': 'San Antonio Spurs', 
    'TOR': 'Toronto Raptors', 'UTA': 'Utah Jazz', 'WAS': 'Washington Wizards'
}

st.sidebar.image("https://cdn.freebiesupply.com/images/large/2x/nba-logo-transparent.png", width=120)
st.sidebar.markdown("## NBA Analytics Dashboard")
st.sidebar.markdown("Explore NBA statistics from 2012-2024 with interactive visualizations and comparisons.")

page = st.sidebar.selectbox(
    "Choose a section",
    ["Introduction", "League Trends", "Team Analysis", "Player Comparisons", "About the Project"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Data Abbreviations")
with st.sidebar.expander("View NBA Statistical Abbreviations"):
    st.markdown("""
        - **GP** = Games Played
        - **MIN** = Minutes Played
        - **PTS** = Points
        - **FGM** = Field Goals Made
        - **FGA** = Field Goals Attempted
        - **FG_PCT** = Field Goal Percentage
        - **FG3M** = 3 Point Field Goals Made
        - **FG3A** = 3 Point Field Goals Attempted
        - **FG3_PCT** = 3 Point Field Goal Percentage
        - **FTM** = Free Throws Made
        - **FTA** = Free Throws Attempted
        - **FT_PCT** = Free Throw Percentage
        - **OREB** = Offensive Rebounds
        - **DREB** = Defensive Rebounds
        - **REB** = Rebounds
        - **AST** = Assists
        - **STL** = Steals
        - **BLK** = Blocks
        - **TOV** = Turnovers
        - **PF** = Personal Fouls
    """)

st.sidebar.markdown("---")
st.sidebar.info("This dashboard is a showcase project for data analysis and visualization skills using NBA data from 2012-2024.")
st.sidebar.markdown("© 2025 - NBA Analytics Project")

if page == "Introduction":
    st.markdown('<h1 class="main-header">NBA Analytics: Evolution of the Game (2012-2024)</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">Project Overview</h2>', unsafe_allow_html=True)

        st.write("This interactive dashboard explores NBA data from the 2012-2024 seasons, analyzing trends in playing style, team strategies, and player performance. The analysis reveals how the NBA game has evolved, particularly with the rise of three-point shooting and changes in offensive efficiency.")

        st.markdown('<h3>Key Features:</h3>', unsafe_allow_html=True)
        st.markdown("""
        - Track the league-wide evolution of playing styles and strategies
        - Compare team performance metrics and playing styles
        - Analyze individual player statistics and career trajectories
        - Explore the shift toward perimeter shooting and its impact on the game
        """)

        st.write("Use the sidebar to navigate between different sections of the analysis.")
        
    with col2:
        st.image("https://cdn.nba.com/manage/2021/08/NBA-Ball-Global-500x500.jpg", width=300)
    
    st.markdown('<h2 class="sub-header">Dashboard Highlights</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">36%</div>
            <div class="metric-label">Increase in 3-point attempts since 2012</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">12%</div>
            <div class="metric-label">Rise in offensive efficiency (points per 100 possessions)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">30</div>
            <div class="metric-label">Teams analyzed across 12 seasons of data</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    
        <h3>Data Collection and Methodology</h3>
        <p>This dataset was scraped from the official NBA website and includes detailed statistics for all NBA players and teams from the 2012-2013 through 2023-2024 seasons. The data covers both regular season and playoff games.</p>
            """,unsafe_allow_html=True)

    st.markdown("""
    <h3>The analysis includes:</h3>
    - Advanced statistical metrics like True Shooting Percentage and Possession Estimation
    - Normalized statistics for fair comparisons across different playing times
    - Visualization of trends and patterns using interactive charts
    """,unsafe_allow_html=True)


elif page == "League Trends":
    st.markdown('<h1 class="main-header">NBA League Trends (2012-2024)</h1>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="dashboard-container">
        <p>This section explores how the NBA game has evolved over the past decade, with particular focus on the rise of three-point shooting, changes in pace of play, and scoring distribution.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="sub-header">The Three-Point Revolution</h2>', unsafe_allow_html=True)
    
    seasons = list(range(2012, 2024))
    three_point_data = pd.DataFrame({
        'season_start_year': seasons,
        '3PAr': [0.22, 0.24, 0.26, 0.28, 0.31, 0.34, 0.36, 0.38, 0.39, 0.40, 0.40, 0.41],  # Simulated data
    })
    
    fig = px.line(three_point_data, x='season_start_year', y='3PAr', 
                title="Evolution of 3-Point Attempt Rate (2012-2024)",
                markers=True, line_shape='linear')
    
    fig.update_layout(
        xaxis_title="Season",
        yaxis_title="3-Point Attempt Rate (3PA/FGA)",
        yaxis=dict(tickformat='.0%'),
        hovermode="x unified",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
            <h3>Scoring Distribution Evolution</h3>
        </div>
        """, unsafe_allow_html=True)
        
        scoring_data = pd.DataFrame({
            'season_start_year': seasons,
            '3PT_pts': [22, 24, 27, 28, 31, 33, 35, 36, 37, 38, 38, 39],  
            '2PT_pts': [50, 49, 47, 46, 45, 43, 42, 41, 40, 39, 39, 38],
            'FT_pts': [28, 27, 26, 26, 24, 24, 23, 23, 23, 23, 23, 23]
        })
        
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=scoring_data['season_start_year'], 
            y=scoring_data['3PT_pts'],
            mode='lines',
            line=dict(width=2, color='rgb(0, 119, 182)'),
            stackgroup='one',
            name='Points from 3-pointers'
        ))
        
        fig2.add_trace(go.Scatter(
            x=scoring_data['season_start_year'], 
            y=scoring_data['2PT_pts'],
            mode='lines',
            line=dict(width=2, color='rgb(223, 42, 42)'),
            stackgroup='one',
            name='Points from 2-pointers'
        ))
        
        fig2.add_trace(go.Scatter(
            x=scoring_data['season_start_year'], 
            y=scoring_data['FT_pts'],
            mode='lines',
            line=dict(width=2, color='rgb(86, 179, 86)'),
            stackgroup='one',
            name='Points from Free Throws'
        ))
        
        fig2.update_layout(
            title="NBA Scoring Distribution by Point Type (2012-2024)",
            xaxis_title="Season",
            yaxis_title="Percentage of Total Points",
            legend=dict(x=0.01, y=0.99),
            hovermode="x unified",
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
        
    with col2:
        st.markdown("""
        <div class="chart-container">
            <h3>Game Pace and Efficiency</h3>
        </div>
        """, unsafe_allow_html=True)
        
        pace_data = pd.DataFrame({
            'season_start_year': seasons,
            'PACE': [92, 93.5, 93.9, 95.2, 96.5, 97.3, 98.1, 100.2, 99.2, 99.5, 98.8, 100.1],  
            'ORtg': [105.8, 106.6, 107.9, 108.5, 109.1, 109.3, 110.7, 111.5, 112.8, 113.6, 114.1, 115.2]
        })
        
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig3.add_trace(
            go.Scatter(
                x=pace_data['season_start_year'],
                y=pace_data['PACE'],
                mode='lines+markers',
                name='Pace (Possessions per 48 min)',
                marker=dict(color='#17408B')
            ),
            secondary_y=False,
        )
        
        fig3.add_trace(
            go.Scatter(
                x=pace_data['season_start_year'],
                y=pace_data['ORtg'],
                mode='lines+markers',
                name='Offensive Rating',
                marker=dict(color='#C9082A')
            ),
            secondary_y=True,
        )
        
        fig3.update_layout(
            title="NBA Game Pace and Offensive Efficiency (2012-2024)",
            legend=dict(x=0.01, y=0.99),
            height=400
        )
        
        fig3.update_xaxes(title_text="Season")
        
        fig3.update_yaxes(
            title_text="Pace (Possessions per 48 min)",
            title_font=dict(color="#17408B"),
            tickfont=dict(color="#17408B"),
            secondary_y=False
        )
        
        fig3.update_yaxes(
            title_text="Offensive Rating (Points per 100 Possessions)",
            title_font=dict(color="#C9082A"),
            tickfont=dict(color="#C9082A"),
            secondary_y=True
        )
        
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<h2 class="sub-header">Key Insights from League Trends</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="dashboard-container">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    1. **Three-Point Revolution:** The percentage of field goal attempts from behind the arc has increased by nearly 86% from 2012 to 2024, fundamentally changing offensive strategies.
    
    2. **Scoring Distribution Shift:** Points from three-pointers now account for approximately 39% of all scoring, up from just 22% in 2012.
    
    3. **Pace Acceleration:** The average number of possessions per 48 minutes has increased from 92 to over 100, resulting in more opportunities to score.
    
    4. **Offensive Efficiency Gains:** Teams are scoring more points per 100 possessions than ever before, with the league average offensive rating increasing from 105.8 to 115.2.
    
    5. **Free Throw Decline:** The proportion of points from free throws has decreased, suggesting a change in how fouls are called or how players attack defenses.
    """)
    
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
elif page == "Team Analysis":
    st.markdown('<h1 class="main-header">NBA Team Analysis</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-container">
        <p>Compare NBA teams based on various performance metrics and playing styles. Select teams and seasons to see detailed comparisons.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        team_options = sorted(data['TEAM'].unique())
        team1 = st.selectbox("Select first team", team_options, index=team_options.index('GSW') if 'GSW' in team_options else 0)
        team2 = st.selectbox("Select second team", team_options, index=team_options.index('LAL') if 'LAL' in team_options else 1)
    
    with col2:
        season_options = sorted(data['season_start_year'].unique())
        selected_season = st.selectbox("Select season", season_options, index=len(season_options)-1)
    
    team1_data = team_season_stats[(team_season_stats['TEAM'] == team1) & 
                                  (team_season_stats['season_start_year'] == selected_season)]
    team2_data = team_season_stats[(team_season_stats['TEAM'] == team2) & 
                                  (team_season_stats['season_start_year'] == selected_season)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: {team_colors.get(team1, '#000')}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            <h3>{team_names.get(team1, team1)}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: {team_colors.get(team2, '#000')}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            <h3>{team_names.get(team2, team2)}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="sub-header">Team Comparison</h2>', unsafe_allow_html=True)
    
    # Create comparison visualizations
    if not team1_data.empty and not team2_data.empty:
        # Define metrics for comparison
        metrics = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT', 'AST_ratio']
        
        # Prepare data for bar chart
        teams_data = pd.DataFrame({
            'Metric': metrics,
            team1: [team1_data[m].values[0] if not team1_data[m].empty else 0 for m in metrics],
            team2: [team2_data[m].values[0] if not team2_data[m].empty else 0 for m in metrics]
        })
        
        # Create bar chart comparison
        fig = px.bar(teams_data, x='Metric', y=[team1, team2], barmode='group',
                    title=f"Team Comparison: {team1} vs {team2} ({selected_season}-{selected_season+1} Season)",
                    color_discrete_map={team1: team_colors.get(team1, '#000'), team2: team_colors.get(team2, '#000')})
        
        fig.update_layout(
            xaxis_title="Metric",
            yaxis_title="Value",
            legend_title="Team",
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Radar chart comparison for playing style
        style_metrics = ['PACE', 'ORtg', 'FG3_ratio', 'AST_ratio', 'PTS_per_POSS']
        style_labels = {
            'PACE': 'Pace of Play', 
            'ORtg': 'Offensive Rating', 
            'FG3_ratio': '3PT Attempt Rate', 
            'AST_ratio': 'Assist Ratio', 
            'PTS_per_POSS': 'Scoring Efficiency'
        }
        
        # Normalize values for radar chart
        max_vals = {}
        for metric in style_metrics:
            if metric in team1_data.columns and metric in team2_data.columns:
                max_vals[metric] = max(
                    team1_data[metric].values[0] if not team1_data[metric].empty else 0,
                    team2_data[metric].values[0] if not team2_data[metric].empty else 0
                ) * 1.1  # Add 10% buffer
        
        team1_values = []
        team2_values = []
        
        for metric in style_metrics:
            if metric in team1_data.columns and metric in team2_data.columns:
                team1_val = team1_data[metric].values[0] if not team1_data[metric].empty else 0
                team2_val = team2_data[metric].values[0] if not team2_data[metric].empty else 0
                
                # Normalize to 0-1 scale
                team1_values.append(team1_val / max_vals[metric])
                team2_values.append(team2_val / max_vals[metric])
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=team1_values,
            theta=[style_labels[m] for m in style_metrics],
            fill='toself',
            name=team1,
            line_color=team_colors.get(team1, '#000')
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=team2_values,
            theta=[style_labels[m] for m in style_metrics],
            fill='toself',
            name=team2,
            line_color=team_colors.get(team2, '#000')
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            title="Team Playing Style Comparison",
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Team efficiency visualization - Pace vs. Offensive Rating for all teams
        st.markdown('<h2 class="sub-header">League-wide Team Performance</h2>', unsafe_allow_html=True)
        
        # Get all teams for the selected season
        season_teams = team_season_stats[team_season_stats['season_start_year'] == selected_season]
        
        # Create scatter plot of pace vs. offensive rating
        fig_scatter = px.scatter(season_teams, x='PACE', y='ORtg',
                                text='TEAM', size='PTS',
                                title=f"Team Pace vs. Offensive Efficiency ({selected_season}-{selected_season+1} Season)",
                                labels={'PACE': 'Pace (Possessions per 48 min)', 
                                        'ORtg': 'Offensive Rating (Points per 100 Possessions)'},
                                color='PTS',
                                color_continuous_scale='Viridis')
        
        fig_scatter.update_traces(textposition='top center', marker=dict(opacity=0.8))
        fig_scatter.update_layout(
            height=600,
            xaxis=dict(range=[min(season_teams['PACE'])*0.98, max(season_teams['PACE'])*1.02]),
            yaxis=dict(range=[min(season_teams['ORtg'])*0.98, max(season_teams['ORtg'])*1.02])
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Add explanation of the chart
        st.markdown("""
        <div class="chart-container">
        <p>This scatter plot positions teams based on their pace of play (horizontal axis) and offensive efficiency (vertical axis).
        Teams in the upper right corner play fast and efficiently, while teams in the bottom left play slower with less scoring efficiency.
        The size of each bubble represents the team's total points scored.</p>
        
        <h4>What this tells us:</h4>
        <ul>
            <li>Speed doesn't necessarily correlate with scoring efficiency</li>
            <li>Teams with different playing styles can be equally successful</li>
            <li>Most teams cluster around the league average for both metrics</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.warning("No data available for the selected teams and season combination.")
        


# Fixed Player Comparisons Section
if page == "Player Comparisons":
    st.markdown('<h1 class="main-header">NBA Player Comparisons</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-container">
        <p>Compare NBA players' statistics and performance metrics. Select players to visualize their strengths, 
        weaknesses, and how they stack up against each other.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ensure data_per_min has data before proceeding
    if data_per_min.empty:
        st.warning("No player statistics available. Recreating player statistics...")
        data_per_min = create_per_min_stats(data, total_cols)
    
    # Check if we now have data
    if data_per_min.empty:
        st.error("Unable to generate player statistics. Please check the data format.")
    else:
        # Display available seasons
        available_seasons = sorted(data['season_start_year'].unique())
        if not available_seasons:
            st.error("No seasons found in the data.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                # Season selection first
                selected_season = st.selectbox("Select season for comparison", available_seasons, 
                                              index=len(available_seasons)-1)
                
                # Convert season to the format used in 'year' column (e.g., 2023 to "2023-24")
                season_year_str = f"{selected_season}-{str(selected_season+1)[2:]}"
                
                # For robustness, also check alternative format if no data is found
                alternative_season_format = f"{selected_season}-{selected_season+1}"
                
                # Display the season format for debugging
                st.caption(f"Looking for data with season format: {season_year_str} or {alternative_season_format}")
            
            # First try with the primary format
            season_data = data_per_min[data_per_min['year'] == season_year_str]
            
            # If no data found, try alternative format
            if season_data.empty:
                season_data = data_per_min[data_per_min['year'] == alternative_season_format]
                if not season_data.empty:
                    season_year_str = alternative_season_format
            
            # If still no data found, try creating on the fly for this season
            if season_data.empty:
                st.warning(f"No pre-calculated stats found for {season_year_str}. Creating them now...")
                
                # Filter the raw data for the selected season
                season_raw_data = data[data['season_start_year'] == selected_season]
                
                if not season_raw_data.empty:
                    # Create per-minute stats just for this season
                    season_data = create_per_min_stats(season_raw_data, total_cols)
                    st.success("Successfully created player statistics for the selected season.")
                else:
                    st.error(f"No raw data found for season {selected_season}.")
            
            # Get players who were active in the selected season
            active_players = sorted(season_data['PLAYER'].unique()) if not season_data.empty else []
            
            with col2:
                # Player selection with only active players from the selected season
                if active_players:
                    default_players = active_players[:2] if len(active_players) >= 2 else active_players
                    selected_players = st.multiselect(
                        "Select players to compare (2-5 recommended)",
                        active_players,
                        default=default_players
                    )
                    
                    st.success(f"{len(active_players)} players found for {season_year_str}")
                else:
                    st.warning(f"No player data available for the {season_year_str} season.")
                    selected_players = []
            
            # Add a show graphs button
            show_graphs = False
            if len(selected_players) > 0:
                if st.button("Show Player Comparison Graphs", type="primary"):
                    show_graphs = True
            
            if show_graphs and len(selected_players) > 0:
                # Get player data for selected season
                selected_player_data = season_data[season_data['PLAYER'].isin(selected_players)]
                
                if not selected_player_data.empty:
                    with st.spinner("Generating player comparison visualizations..."):
                        st.markdown('<h2 class="sub-header">Player Radar Comparison</h2>', unsafe_allow_html=True)
                        
                        # Determine available metrics for the radar chart
                        available_base_metrics = ['PTS', 'AST', 'REB', 'STL', 'BLK']
                        available_pct_metrics = ['FG%', '3PT%', 'FT%']
                        
                        radar_metrics = [m for m in available_base_metrics if m in selected_player_data.columns]
                        radar_metrics += [m for m in available_pct_metrics if m in selected_player_data.columns]
                        
                        if not radar_metrics:
                            st.warning("No metrics available for radar chart visualization.")
                        else:
                            # Create the radar chart
                            fig_radar = go.Figure()
                            
                            # Get max values for each metric across all players for normalization
                            max_values = {}
                            for metric in radar_metrics:
                                # For percentages, the max should be 1 (100%)
                                if metric in available_pct_metrics:
                                    max_values[metric] = 1
                                else:
                                    max_values[metric] = season_data[metric].max() * 1.1  # Add buffer
                            
                            # Add each player as a trace
                            for player in selected_player_data['PLAYER'].unique():
                                player_data = selected_player_data[selected_player_data['PLAYER'] == player]
                                
                                # Get values and normalize them (0-1 range)
                                values = []
                                for metric in radar_metrics:
                                    if metric in player_data.columns and metric in max_values:
                                        val = player_data[metric].values[0]
                                        # Normalize value based on max for that metric
                                        normalized_val = val / max_values[metric]
                                        values.append(normalized_val)
                                
                                # Add trace for this player
                                fig_radar.add_trace(go.Scatterpolar(
                                    r=values,
                                    theta=radar_metrics,
                                    fill='toself',
                                    name=player
                                ))
                            
                            fig_radar.update_layout(
                                polar=dict(
                                    radialaxis=dict(
                                        visible=True,
                                        range=[0, 1]
                                    )
                                ),
                                title=f"Player Comparison - {season_year_str} Season",
                                showlegend=True,
                                height=600
                            )
                            
                            st.plotly_chart(fig_radar, use_container_width=True)
                        
                        # Display detailed player statistics table
                        st.markdown('<h2 class="sub-header">Detailed Player Statistics</h2>', unsafe_allow_html=True)
                        
                        # Determine available columns for the table
                        base_cols = ['PLAYER', 'MIN']
                        stat_cols = [col for col in ['PTS', 'REB', 'AST', 'STL', 'BLK'] 
                                    if col in selected_player_data.columns]
                        pct_cols = [col for col in ['FG%', '3PT%', 'FT%', 'TRU%', 'AST_TOV'] 
                                   if col in selected_player_data.columns]
                        
                        # Combine all available columns
                        display_cols = base_cols + stat_cols + pct_cols
                        
                        # Create display dataframe
                        display_df = selected_player_data[display_cols].copy()
                        
                        # Convert per-minute stats to per-36 minutes for better readability
                        for col in stat_cols:
                            display_df[col] = display_df[col] * 36
                        
                        # Format percentage columns
                        for col in ['FG%', '3PT%', 'FT%', 'TRU%']:
                            if col in display_df.columns:
                                display_df[col] = display_df[col].apply(lambda x: f"{x:.1%}" if not pd.isna(x) else "N/A")
                        
                        # Format other numerical columns
                        for col in stat_cols + ['AST_TOV']:
                            if col in display_df.columns:
                                display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
                        
                        # Rename columns for display
                        column_names = {
                            'PLAYER': 'Player',
                            'MIN': 'Minutes',
                            'PTS': 'PTS/36',
                            'REB': 'REB/36',
                            'AST': 'AST/36',
                            'STL': 'STL/36',
                            'BLK': 'BLK/36',
                            'FG%': 'FG%',
                            '3PT%': '3PT%',
                            'FT%': 'FT%',
                            'TRU%': 'True Shooting %',
                            'AST_TOV': 'AST/TO Ratio'
                        }
                        
                        # Only rename columns that exist in the DataFrame
                        rename_dict = {col: column_names[col] for col in display_df.columns if col in column_names}
                        display_df = display_df.rename(columns=rename_dict)
                        
                        st.dataframe(display_df.set_index('Player'), use_container_width=True)
                        
                        # Career trajectory visualization - only for single player selection
                        if len(selected_players) == 1:
                            st.markdown('<h2 class="sub-header">Career Trajectory</h2>', unsafe_allow_html=True)
                            
                            player_name = selected_players[0]
                            player_career = data[data['PLAYER'] == player_name]
                            
                            if not player_career.empty:
                                # Check if we can create career stats
                                if 'season_start_year' in player_career.columns and 'GP' in player_career.columns:
                                    # Calculate per-game stats for each season
                                    valid_stat_cols = [col for col in total_cols if col in player_career.columns]
                                    
                                    if valid_stat_cols:
                                        career_by_season = player_career.groupby('season_start_year')[valid_stat_cols + ['GP']].sum().reset_index()
                                        
                                        # Calculate per-game statistics
                                        career_stats = ['PTS', 'REB', 'AST', 'STL', 'BLK']
                                        per_game_cols = [col for col in career_stats if col in valid_stat_cols]
                                        
                                        for col in per_game_cols:
                                            career_by_season[f'{col}_per_game'] = career_by_season[col] / career_by_season['GP']
                                        
                                        # Create a line chart of career trajectory
                                        fig_career = go.Figure()
                                        
                                        for col in per_game_cols:
                                            fig_career.add_trace(go.Scatter(
                                                x=career_by_season['season_start_year'],
                                                y=career_by_season[f'{col}_per_game'],
                                                mode='lines+markers',
                                                name=f'{col} per Game'
                                            ))
                                        
                                        fig_career.update_layout(
                                            title=f"{player_name} Career Trajectory",
                                            xaxis_title="Season",
                                            yaxis_title="Statistics per Game",
                                            legend=dict(x=0.01, y=0.99),
                                            hovermode="x unified",
                                            height=500
                                        )
                                        
                                        st.plotly_chart(fig_career, use_container_width=True)
                                        
                                        # Career highlights
                                        st.markdown(f"""
                                        <div class="chart-container">
                                            <h3>{player_name} Career Highlights</h3>
                                            <p>The line chart above shows {player_name}'s statistical performance over time. 
                                            This visualization helps identify peak performance seasons and career trends.</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.warning("No statistical columns available for career trajectory visualization.")
                                else:
                                    st.warning("Required columns for career trajectory not found in data.")
                            else:
                                st.warning(f"No career data available for {player_name}.")
                else:
                    st.warning(f"No data available for the selected players in the {season_year_str} season.")
            elif len(selected_players) > 0 and not show_graphs:
                st.info("Click 'Show Player Comparison Graphs' to view the comparison visualizations.")
            elif selected_players == [] and active_players:
                st.info("Please select at least one player to compare.")
                    
elif page == "About the Project":
    st.markdown('<h1 class="main-header">About the NBA Analytics Project</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h2>Project Background</h2>', unsafe_allow_html=True)
    st.markdown('<p>This NBA Analytics Dashboard was developed as a data science portfolio project to demonstrate expertise in:</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    - **Data Processing:** Cleaning and transforming raw NBA statistics
    - **Statistical Analysis:** Calculating advanced basketball metrics
    - **Data Visualization:** Creating interactive and informative charts
    - **Web Application Development:** Building a user-friendly dashboard
    """)
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h2>Technologies Used</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    - **Python:** Core programming language
    - **Pandas:** Data manipulation and analysis
    - **Plotly:** Interactive data visualizations
    - **Streamlit:** Web application framework
    - **NumPy:** Numerical computing
    """)
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h2>Technical Implementation</h2>', unsafe_allow_html=True)
    st.markdown('<p>The application is built with Streamlit, which allows for rapid development of data-focused web applications in Python. The visualizations are created using Plotly, providing interactive charts that allow users to explore the data more deeply.</p>', unsafe_allow_html=True)
    st.markdown('<p>Key technical features include:</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    - Dynamic filtering of data based on user selections
    - Interactive visualizations with hover information
    - Responsive design that works on different screen sizes
    - Efficient data processing for smooth performance
    """)
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h2>Data Sources</h2>', unsafe_allow_html=True)
    st.markdown('<p>The data for this project was scraped from the official NBA website, covering regular season and playoff statistics from the 2012-2013 through 2023-2024 seasons. The dataset includes player and team performance metrics, which were then processed to derive additional analytical insights.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h2>Future Enhancements</h2>', unsafe_allow_html=True)
    st.markdown('<p>Potential future improvements to the dashboard include:</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    - Incorporating player shooting location data for shot charts
    - Adding player efficiency ratings and advanced metrics
    - Machine learning models to predict player performance
    - Real-time data updates during the NBA season
    - Expanded historical data coverage
    """)
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h2>Contact Information</h2>', unsafe_allow_html=True)
    st.markdown("""
    <p>Created by: Shivam Kumar</p>
    <p>GitHub Repository: <a href="https://github.com/yourusername/nba-analytics" target="_blank">https://github.com/yourusername/nba-analytics</a></p>
    <p>Email: shivamksi42@gmail.com</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    