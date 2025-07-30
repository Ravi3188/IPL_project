import pandas as pd
import os
import matplotlib.pyplot as plt

# Mapping from menu choices to CSV and plot files
file_map = {
    "1": ("team_report.csv", "plots/team_plot.png"),
    "2": ("season_report.csv", "plots/season_plot.png"),
    "3": ("top_teams.csv", "plots/top_teams_plot.png"),
    "4": ("top_batsmen.csv", "plots/top_batsmen_plot.png"),
    "5": ("most_sixes.csv", "plots/most_sixes_plot.png"),
    "6": ("economical_bowlers.csv", "plots/economical_bowlers.png"),
}

# Show menu
print("\n📊 Choose a report to preview:\n")
print("1. Team Report")
print("2. Season Report")
print("3. Top Teams")
print("4. Top Batsmen")
print("5. Most Sixes")
print("6. Economical Bowlers")

# Get user choice
choice = input("\nEnter your choice (1-6): ")

if choice in file_map:
    csv_file, plot_file = file_map[choice]
    
    # Show CSV content
    try:
        df = pd.read_csv(csv_file)
        print(f"\n📄 Full contents of '{csv_file}':\n")
        print(df.to_string(index=False))
    except FileNotFoundError:
        print(f"❌ File '{csv_file}' not found.")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")

    # Display plot image if exists
    if os.path.exists(plot_file):
        try:
            img = plt.imread(plot_file)
            plt.imshow(img)
            plt.axis('off')
            plt.title(f"📊 {os.path.basename(plot_file)}")
            plt.show()
        except Exception as e:
            print(f"❌ Failed to display image: {e}")
    else:
        print(f"📁 No plot found for this report at '{plot_file}'")
else:
    print("⚠️ Invalid choice. Please enter a number from 1 to 6.")
