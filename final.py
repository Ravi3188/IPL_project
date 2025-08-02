import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Ensure folders exist
os.makedirs("reports", exist_ok=True)
os.makedirs("charts", exist_ok=True)

def show_and_save_chart(df, x_col, y_col, title, filename, color='blue'):
    df.plot(x=x_col, y=y_col, kind='bar', legend=False, color=color)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    chart_path = f"charts/{filename}.png"
    plt.savefig(chart_path)
    plt.show()
    print(f"✅ Chart saved as {chart_path}")

def create_database():
    print("✅ Database already exists as 'ipl_analysis.db'")

def top_teams_by_wins(conn):
    query = """
        SELECT winner AS Team, COUNT(*) AS Wins
        FROM matches
        WHERE winner IS NOT NULL
        GROUP BY winner
        ORDER BY Wins DESC
        LIMIT 5;
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("reports/top_teams_by_wins.csv", index=False)
    print(df)
    show_and_save_chart(df, 'Team', 'Wins', 'Top 5 Teams by Wins', 'top_teams_by_wins')

def top_run_scorers(conn):
    query = """
        SELECT batsman AS Player, SUM(batsman_runs) AS Runs
        FROM deliveries
        GROUP BY batsman
        ORDER BY Runs DESC
        LIMIT 5;
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("reports/top_run_scorers.csv", index=False)
    print(df)
    show_and_save_chart(df, 'Player', 'Runs', 'Top 5 Run Scorers', 'top_run_scorers', 'green')

def top_wicket_takers(conn):
    query = """
        SELECT bowler AS Player, COUNT(*) AS Wickets
        FROM deliveries
        WHERE dismissal_kind NOT IN ('run out', 'retired hurt', 'obstructing the field')
        AND dismissal_kind IS NOT NULL
        GROUP BY bowler
        ORDER BY Wickets DESC
        LIMIT 5;
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("reports/top_wicket_takers.csv", index=False)
    print(df)
    show_and_save_chart(df, 'Player', 'Wickets', 'Top 5 Wicket Takers', 'top_wicket_takers', 'orange')

def top_six_hitters(conn):
    query = """
        SELECT batsman AS Player, COUNT(*) AS Sixes
        FROM deliveries
        WHERE batsman_runs = 6
        GROUP BY batsman
        ORDER BY Sixes DESC
        LIMIT 5;
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("reports/top_six_hitters.csv", index=False)
    print(df)
    show_and_save_chart(df, 'Player', 'Sixes', 'Top 5 Six Hitters', 'top_six_hitters', 'purple')

def economical_bowlers(conn):
    query = """
        SELECT bowler, ROUND(SUM(total_runs)*6.0/COUNT(*), 2) AS Economy
        FROM deliveries
        GROUP BY bowler
        HAVING COUNT(*) >= 300
        ORDER BY Economy ASC
        LIMIT 5;
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("reports/top_economical_bowlers.csv", index=False)
    print(df)
    show_and_save_chart(df, 'bowler', 'Economy', 'Top Economical Bowlers', 'top_economical_bowlers', 'red')

def matches_per_season(conn):
    query = """
        SELECT season AS Season, COUNT(*) AS Matches
        FROM matches
        GROUP BY season
        ORDER BY season;
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("reports/matches_per_season.csv", index=False)
    print(df)
    show_and_save_chart(df, 'Season', 'Matches', 'Matches Per Season', 'matches_per_season', 'blue')

def toss_vs_match_winner(conn):
    query = """
        SELECT CASE WHEN toss_winner = winner THEN 'Toss & Match Won'
                    ELSE 'Only Toss or Match Won' END AS Result,
               COUNT(*) AS Count
        FROM matches
        GROUP BY Result;
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("reports/toss_vs_match_winner.csv", index=False)
    print(df)
    show_and_save_chart(df, 'Result', 'Count', 'Toss Winner vs Match Winner', 'toss_vs_match_winner', 'cyan')

def matches_per_venue(conn):
    query = """
        SELECT venue AS Venue, COUNT(*) AS Matches
        FROM matches
        GROUP BY venue
        ORDER BY Matches DESC
        LIMIT 5;
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("reports/matches_per_venue.csv", index=False)
    print(df)
    show_and_save_chart(df, 'Venue', 'Matches', 'Top Venues by Matches', 'matches_per_venue', 'magenta')

def win_percentage_by_innings(conn):
    query = """
        SELECT CASE WHEN win_by_runs > 0 THEN 'Bat First' ELSE 'Chase' END AS Strategy,
               COUNT(*) AS Wins
        FROM matches
        WHERE winner IS NOT NULL
        GROUP BY Strategy;
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("reports/win_by_innings_strategy.csv", index=False)
    print(df)
    show_and_save_chart(df, 'Strategy', 'Wins', 'Win by Bat First vs Chase', 'win_by_innings_strategy', 'gold')

def main_menu():
    db_path = "ipl_analysis.db"
    conn = sqlite3.connect(db_path)

    options = {
        "1": ("Create Database (if not exists)", create_database),
        "2": ("Top 5 Teams by Wins", lambda: top_teams_by_wins(conn)),
        "3": ("Top 5 Run Scorers", lambda: top_run_scorers(conn)),
        "4": ("Top 5 Wicket Takers", lambda: top_wicket_takers(conn)),
        "5": ("Top 5 Six Hitters", lambda: top_six_hitters(conn)),
        "6": ("Top Economical Bowlers", lambda: economical_bowlers(conn)),
        "7": ("Matches Per Season", lambda: matches_per_season(conn)),
        "8": ("Toss Winner vs Match Winner", lambda: toss_vs_match_winner(conn)),
        "9": ("Top Venues by Matches", lambda: matches_per_venue(conn)),
        "10": ("Win % by Batting First or Chasing", lambda: win_percentage_by_innings(conn)),
        "11": ("Exit", None)
    }

    while True:
        print("\n🎯 IPL FULL ANALYSIS MENU")
        for key, (desc, _) in options.items():
            print(f"{key}. {desc}")
        choice = input("\nEnter your choice (1–11): ").strip()

        if choice == "11":
            print("👋 Exiting. Thank you!")
            break
        elif choice in options:
            print(f"\n📊 {options[choice][0]}")
            print("=" * 60)
            options[choice][1]()
        else:
            print("❌ Invalid choice. Please try again.")

    conn.close()

if __name__ == "__main__":
    main_menu()
