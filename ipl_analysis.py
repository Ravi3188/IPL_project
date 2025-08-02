# ipl_analysis.py

import pandas as pd
import numpy as np
import sqlite3
import os
import matplotlib.pyplot as plt
import logging

# Setup
DATA_FOLDER = "data"
DB_PATH = "db/ipl_analysis.db"
OUTPUT_FOLDER = "output"
LOG_FILE = "logs/ipl_analysis.log"

os.makedirs("db", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Logging configuration
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load data
def load_data():
    try:
        matches = pd.read_csv(os.path.join(DATA_FOLDER, "matches.csv"))
        deliveries = pd.read_csv(os.path.join(DATA_FOLDER, "deliveries.csv"))
        logging.info("CSV files loaded successfully.")
        return matches, deliveries
    except Exception as e:
        logging.error(f"Error loading CSV files: {e}")
        raise

# Create SQLite DB
def create_database():
    try:
        matches, deliveries = load_data()
        conn = sqlite3.connect(DB_PATH)
        matches.to_sql("matches", conn, index=False, if_exists="replace")
        deliveries.to_sql("deliveries", conn, index=False, if_exists="replace")
        conn.close()
        logging.info("Database created successfully.")
        print(f"✅ Database created at: {os.path.abspath(DB_PATH)}")
    except Exception as e:
        logging.error(f"DB creation failed: {e}")
        print("❌ Error creating database.")

# Team-wise Report
def generate_team_report():
    try:
        matches, _ = load_data()

        total_matches = pd.concat([matches['team1'], matches['team2']]).value_counts().reset_index()
        total_matches.columns = ['team', 'total_matches']

        total_wins = matches['winner'].value_counts().reset_index()
        total_wins.columns = ['team', 'total_wins']

        team_status = pd.merge(total_matches, total_wins, on='team', how='left')
        team_status['total_wins'] = team_status['total_wins'].fillna(0).astype(int)
        team_status['win_percentage'] = round((team_status['total_wins'] / team_status['total_matches']) * 100, 2)
        team_status = team_status.sort_values(by='win_percentage', ascending=False)

        team_status.to_csv(os.path.join(OUTPUT_FOLDER, "team_report.csv"), index=False)

        # Plot
        plt.figure(figsize=(10, 6))
        plt.bar(team_status['team'], team_status['win_percentage'], color='green')
        plt.xticks(rotation=45)
        plt.ylabel("Win Percentage")
        plt.title("Team-wise Win Percentage")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_FOLDER, "team_win_plot.png"))
        plt.close()

        print("\n📊 TEAM REPORT GENERATED:")
        print(team_status)
        logging.info("Team-wise report generated.")
        return team_status
    except Exception as e:
        logging.error(f"Error in team report: {e}")
        print("❌ Error generating team report.")

# Season-wise Report
def generate_season_report():
    try:
        matches, _ = load_data()

        season_matches = pd.melt(matches, id_vars=['season'], value_vars=['team1', 'team2'],
                                 var_name='role', value_name='team')
        season_matches = season_matches.groupby(['season', 'team']).size().reset_index(name='matches_played')

        season_wins = matches.groupby(['season', 'winner']).size().reset_index(name='matches_won')
        season_wins.rename(columns={'winner': 'team'}, inplace=True)

        season_perf = pd.merge(season_matches, season_wins, on=['season', 'team'], how='left')
        season_perf['matches_won'] = season_perf['matches_won'].fillna(0).astype(int)
        season_perf['win_rate'] = round((season_perf['matches_won'] / season_perf['matches_played']) * 100, 2)

        season_perf = season_perf.sort_values(['season', 'win_rate'], ascending=[True, False])
        season_perf.to_csv(os.path.join(OUTPUT_FOLDER, "season_report.csv"), index=False)

        print("\n📅 SEASON REPORT GENERATED:")
        print(season_perf)
        logging.info("Season-wise report generated.")
        return season_perf
    except Exception as e:
        logging.error(f"Error in season report: {e}")
        print("❌ Error generating season report.")

# Player Performance
def generate_player_analysis():
    try:
        matches, _ = load_data()
        top_players = matches['player_of_match'].value_counts().head(10).reset_index()
        top_players.columns = ['Player', 'Awards']

        top_players.to_csv(os.path.join(OUTPUT_FOLDER, "top_players.csv"), index=False)

        plt.figure(figsize=(10, 6))
        plt.barh(top_players['Player'], top_players['Awards'], color='orange')
        plt.xlabel("Player of the Match Awards")
        plt.title("Top 10 Players")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_FOLDER, "top_players_plot.png"))
        plt.close()

        print("\n🏅 PLAYER PERFORMANCE GENERATED:")
        print(top_players)
        logging.info("Player performance report generated.")
    except Exception as e:
        logging.error(f"Error in player analysis: {e}")
        print("❌ Error generating player performance report.")
