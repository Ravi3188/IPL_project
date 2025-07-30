import pandas as pd
import numpy as np
import sqlite3
import os

# Step 1: Set database file path
db_path = "ipl_analysis.db"

# Step 2: Read CSV files from 'data' folder
matches_df = pd.read_csv("data/matches.csv")
deliveries_df = pd.read_csv("data/deliveries.csv")

# Step 3: Create SQLite DB as a file (not in memory)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 4: Store data into SQL tables
matches_df.to_sql("matches", conn, index=False, if_exists="replace")
deliveries_df.to_sql("deliveries", conn, index=False, if_exists="replace")

# ------------------ TEAM-WISE OVERALL STATUS ------------------

# Step 5: Total matches played (team1 + team2)
total_matches = pd.concat([matches_df['team1'], matches_df['team2']]).value_counts().reset_index()
total_matches.columns = ['team', 'total_matches']

# Step 6: Total wins
total_wins = matches_df['winner'].value_counts().reset_index()
total_wins.columns = ['team', 'total_wins']

# Step 7: Merge and calculate win percentage
team_status = pd.merge(total_matches, total_wins, on='team', how='left')
team_status['total_wins'] = team_status['total_wins'].fillna(0).astype(int)
team_status['win_percentage'] = round((team_status['total_wins'] / team_status['total_matches']) * 100, 2)

# Step 8: Display and save report
print("\n=== TEAM-WISE OVERALL STATUS ===")
print(team_status.sort_values(by='win_percentage', ascending=False))
team_status.to_csv("team_report.csv", index=False)

# ------------------ SEASON-WISE PERFORMANCE ------------------

# Step 9: Matches played per season
season_matches = pd.melt(matches_df, id_vars=['season'], value_vars=['team1', 'team2'],
                         var_name='team_role', value_name='team')
season_matches = season_matches.groupby(['season', 'team']).size().reset_index(name='matches_played')

# Step 10: Matches won per season
season_wins = matches_df.groupby(['season', 'winner']).size().reset_index(name='matches_won')
season_wins.rename(columns={'winner': 'team'}, inplace=True)

# Step 11: Merge and calculate win rate
season_perf = pd.merge(season_matches, season_wins, on=['season', 'team'], how='left')
season_perf['matches_won'] = season_perf['matches_won'].fillna(0).astype(int)
season_perf['win_rate'] = round((season_perf['matches_won'] / season_perf['matches_played']) * 100, 2)

# Step 12: Display and save report
print("\n=== SEASON-WISE PERFORMANCE ===")
print(season_perf.sort_values(['season', 'win_rate'], ascending=[True, False]))
season_perf.to_csv("season_report.csv", index=False)

# Step 13: Completion Message
print("\nReports saved successfully: 'team_report.csv' and 'season_report.csv'")
print(f"Database created at: {os.path.abspath(db_path)}")
