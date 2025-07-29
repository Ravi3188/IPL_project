import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the reports generated earlier
team_status = pd.read_csv("team_report.csv")
season_perf = pd.read_csv("season_report.csv")

sns.set(style="whitegrid")

# --- Team-wise Win % Bar Plot ---
plt.figure(figsize=(12, 6))
sns.barplot(data=team_status.sort_values('win_percentage', ascending=False),
            x='team', y='win_percentage', palette='viridis')
plt.title('Team-wise Win Percentage')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("team_win_percentage.png")
plt.show()

# --- Season-wise Win Rate Heatmap ---
season_pivot = season_perf.pivot(index='team', columns='season', values='win_rate').fillna(0)
plt.figure(figsize=(15, 10))
sns.heatmap(season_pivot, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5)
plt.title('Season-wise Team Win Rate (%)')
plt.tight_layout()
plt.savefig("season_win_rate_heatmap.png")
plt.show()

# --- Top Team Per Season Line Plot ---
top_teams = season_perf.sort_values(['season', 'win_rate'], ascending=[True, False]) \
                       .groupby('season').first().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=top_teams, x='season', y='win_rate', hue='team', marker='o', palette='tab10')
plt.title('Top Performing Team Each Season by Win Rate')
plt.tight_layout()
plt.savefig("top_team_per_season.png")
plt.show()
