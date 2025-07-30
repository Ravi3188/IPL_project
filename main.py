import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sql_queries import (
    top_teams_query, top_batsmen_query,
    economical_bowlers_query, most_sixes_query,
    top_bowlers_query, most_matches_played_query
)
from visualizations import plot_top_teams, plot_top_batsmen
from exceptions import IPLDataError, IPLDatabaseError, IPLReportError

# Manual import of logger_config to avoid import error
import importlib.util

module_path = os.path.join(os.getcwd(), 'logger_config.py')
spec = importlib.util.spec_from_file_location("logger_config", module_path)
logger_config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logger_config)

setup_logger = logger_config.setup_logger
logger = setup_logger("main_logger")

try:
    os.makedirs("plots", exist_ok=True)

    # Load data
    try:
        matches_df = pd.read_csv("data/matches.csv")
        deliveries_df = pd.read_csv("data/deliveries.csv")
        logger.info("CSV files loaded successfully.")
    except Exception as e:
        logger.critical("Failed to load CSV files.")
        raise IPLDataError("CSV loading failed.") from e

    # Connect to SQLite DB
    try:
        conn = sqlite3.connect("ipl_analysis.db")
        logger.info("Connected to SQLite database.")
    except Exception as e:
        logger.critical("Database connection failed.")
        raise IPLDatabaseError("DB connection failed.") from e

    # Save DataFrames to SQL
    try:
        matches_df.to_sql("matches", conn, index=False, if_exists="replace")
        deliveries_df.to_sql("deliveries", conn, index=False, if_exists="replace")
        logger.info("Data written to database successfully.")
    except Exception as e:
        logger.error("Failed to write data to DB.")
        raise IPLDatabaseError("DB write failed.") from e

    # Team report
    try:
        team1_counts = matches_df['team1'].value_counts()
        team2_counts = matches_df['team2'].value_counts()
        total_matches = (team1_counts + team2_counts).reset_index()
        total_matches.columns = ['team', 'matches_played']

        total_wins = matches_df['winner'].value_counts().reset_index()
        total_wins.columns = ['team', 'matches_won']

        team_status = pd.merge(total_matches, total_wins, on='team', how='left')
        team_status['matches_won'].fillna(0, inplace=True)
        team_status['win_percentage'] = round((team_status['matches_won'] / team_status['matches_played']) * 100, 2)

        team_status.to_csv("team_report.csv", index=False)
        logger.info("Team report generated.")
    except Exception as e:
        logger.error("Failed to generate team report.")
        raise IPLReportError("Team report generation failed.") from e

    # Season report
    try:
        season_matches = pd.melt(matches_df, id_vars=['season'], value_vars=['team1', 'team2'],
                                 var_name='position', value_name='team')
        season_matches = season_matches.groupby(['season', 'team']).size().reset_index(name='matches_played')

        season_wins = matches_df.groupby(['season', 'winner']).size().reset_index(name='matches_won')
        season_wins.rename(columns={'winner': 'team'}, inplace=True)

        season_perf = pd.merge(season_matches, season_wins, on=['season', 'team'], how='left')
        season_perf['matches_won'].fillna(0, inplace=True)
        season_perf['win_rate'] = round((season_perf['matches_won'] / season_perf['matches_played']) * 100, 2)

        season_perf.to_csv("season_report.csv", index=False)
        logger.info("Season report generated.")
    except Exception as e:
        logger.error("Failed to generate season report.")
        raise IPLReportError("Season report generation failed.") from e

    # Top Teams and Batsmen from SQL
    try:
        pd.read_sql(top_teams_query, conn).to_csv("top_teams.csv", index=False)
        pd.read_sql(top_batsmen_query, conn).to_csv("top_batsmen.csv", index=False)
        logger.info("Top teams and batsmen reports saved.")
    except Exception as e:
        logger.error("SQL query execution failed.")
        raise IPLReportError("SQL report failure.") from e

    # Extra queries
    try:
        pd.read_sql(economical_bowlers_query, conn).to_csv("economical_bowlers.csv", index=False)
        pd.read_sql(most_sixes_query, conn).to_csv("most_sixes.csv", index=False)
        pd.read_sql(top_bowlers_query, conn).to_csv("top_bowlers.csv", index=False)
        pd.read_sql(most_matches_played_query, conn).to_csv("most_matches_played.csv", index=False)
        logger.info("Additional SQL reports saved.")
    except Exception as e:
        logger.error("Failed to save extra SQL results.")
        raise IPLReportError("Additional SQL report error.") from e

    # Plots
    plot_top_teams()
    plot_top_batsmen()
    logger.info("Visualizations generated successfully.")

except Exception as e:
    logger.critical("Fatal error in main execution: %s", str(e))
