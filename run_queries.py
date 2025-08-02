# run_queries.py

import sqlite3
import pandas as pd

def execute_query(conn, query, title):
    print(f"\n📌 {title}")
    print("-" * 60)
    try:
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
    except Exception as e:
        print(f"❌ Error executing query: {e}")

def run_all_queries():
    db_path = "ipl_analysis.db"
    try:
        conn = sqlite3.connect(db_path)

        queries = [
            {
                "title": "Top 5 Teams by Wins",
                "query": """
                    SELECT winner AS Team, COUNT(*) AS Wins
                    FROM matches
                    WHERE winner IS NOT NULL
                    GROUP BY winner
                    ORDER BY Wins DESC
                    LIMIT 5;
                """
            },
            {
                "title": "Top 5 Players by Appearances",
                "query": """
                    SELECT player, COUNT(*) AS Matches
                    FROM (
                        SELECT player_of_match AS player FROM matches
                        UNION ALL
                        SELECT batsman AS player FROM deliveries
                    )
                    GROUP BY player
                    ORDER BY Matches DESC
                    LIMIT 5;
                """
            },
            {
                "title": "Top 5 Six Hitters",
                "query": """
                    SELECT batsman, COUNT(*) AS Sixes
                    FROM deliveries
                    WHERE batsman_runs = 6
                    GROUP BY batsman
                    ORDER BY Sixes DESC
                    LIMIT 5;
                """
            },
            {
                "title": "Top 5 Economical Bowlers (Min 300 balls)",
                "query": """
                    SELECT bowler,
                           ROUND(SUM(total_runs) * 6.0 / COUNT(*), 2) AS Economy
                    FROM deliveries
                    GROUP BY bowler
                    HAVING COUNT(*) >= 300
                    ORDER BY Economy ASC
                    LIMIT 5;
                """
            },
            {
                "title": "Top 5 Run Scorers",
                "query": """
                    SELECT batsman, SUM(batsman_runs) AS Total_Runs
                    FROM deliveries
                    GROUP BY batsman
                    ORDER BY Total_Runs DESC
                    LIMIT 5;
                """
            },
            {
                "title": "Top 5 Wicket Takers (excluding run outs)",
                "query": """
                    SELECT bowler, COUNT(*) AS Wickets
                    FROM deliveries
                    WHERE dismissal_kind NOT IN ('run out', 'retired hurt', 'obstructing the field')
                      AND dismissal_kind IS NOT NULL
                    GROUP BY bowler
                    ORDER BY Wickets DESC
                    LIMIT 5;
                """
            },
            {
                "title": "Matches Played Per Season",
                "query": """
                    SELECT season, COUNT(*) AS Total_Matches
                    FROM matches
                    GROUP BY season
                    ORDER BY season;
                """
            },
            {
                "title": "Toss Winner vs Match Winner",
                "query": """
                    SELECT CASE WHEN toss_winner = winner THEN 'Toss & Match Won'
                                ELSE 'Only Toss or Match Won' END AS Result,
                           COUNT(*) AS Count
                    FROM matches
                    GROUP BY Result;
                """
            },
            {
                "title": "Top 5 Venues with Most Matches",
                "query": """
                    SELECT venue, COUNT(*) AS Matches
                    FROM matches
                    GROUP BY venue
                    ORDER BY Matches DESC
                    LIMIT 5;
                """
            },
            {
                "title": "Win Percentage by Batting First or Second",
                "query": """
                    SELECT win_by_runs > 0 AS Batting_First,
                           COUNT(*) AS Wins
                    FROM matches
                    WHERE winner IS NOT NULL
                    GROUP BY Batting_First;
                """
            }
        ]

        for q in queries:
            execute_query(conn, q["query"], q["title"])

        conn.close()
    except Exception as e:
        print(f"❌ Failed to run queries: {e}")
