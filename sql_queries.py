# sql_queries.py

# 1. Top 5 Teams by Wins
top_teams_query = """
SELECT winner AS team, COUNT(*) AS wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY wins DESC
LIMIT 5;
"""

# 2. Top 5 Batsmen by Runs
top_batsmen_query = """
SELECT batsman, SUM(batsman_runs) AS total_runs
FROM deliveries
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 5;
"""

# 3. Most Economical Bowlers (min 300 balls)
economical_bowlers_query = """
SELECT bowler,
       ROUND(SUM(total_runs) * 6.0 / COUNT(ball), 2) AS economy
FROM deliveries
GROUP BY bowler
HAVING COUNT(ball) >= 300
ORDER BY economy ASC
LIMIT 5;
"""

# 4. Most Sixes by Batsmen
most_sixes_query = """
SELECT batsman, COUNT(*) AS sixes
FROM deliveries
WHERE batsman_runs = 6
GROUP BY batsman
ORDER BY sixes DESC
LIMIT 5;
"""

# 5. Top 5 Bowlers by Wickets (dismissals only)
top_bowlers_query = """
SELECT bowler, COUNT(*) AS wickets
FROM deliveries
WHERE dismissal_kind IN ('caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket')
GROUP BY bowler
ORDER BY wickets DESC
LIMIT 5;
"""

# 6. Most Matches Played by a Team
most_matches_played_query = """
SELECT team, COUNT(*) AS matches_played FROM (
    SELECT team1 AS team FROM matches
    UNION ALL
    SELECT team2 AS team FROM matches
) t
GROUP BY team
ORDER BY matches_played DESC
LIMIT 5;
"""
