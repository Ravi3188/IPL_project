# visualizations.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_top_teams():
    df = pd.read_csv("top_teams.csv")
    plt.figure(figsize=(8, 6))
    sns.barplot(x="team", y="wins", data=df, palette="viridis")
    plt.title("Top 5 Teams by Total Wins")
    plt.xlabel("Team")
    plt.ylabel("Wins")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/top_teams.png")
    plt.close()

def plot_top_batsmen():
    df = pd.read_csv("top_batsmen.csv")
    plt.figure(figsize=(8, 6))
    sns.barplot(x="batsman", y="total_runs", data=df, palette="magma")
    plt.title("Top 5 Batsmen by Runs")
    plt.xlabel("Batsman")
    plt.ylabel("Total Runs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/top_batsmen.png")
    plt.close()
