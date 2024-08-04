import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Setting a style for the plots
sns.set(style="whitegrid")

def plot_streaming_performance():
    # Example data for streaming performance by platform
    data_platform_performance = pd.DataFrame({
        'Platform': ['Apple Music', 'YouTube Music', 'Tidal', 'Spotify', 'Amazon Music'],
        'Total Streams': [1.4e6, 1.2e6, 0.8e6, 1.6e6, 0.6e6],
        'Average Likes': [8500, 6500, 7500, 9000, 5500]
    })

    # Plotting
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Platform', y='Total Streams', data=data_platform_performance, color='b', label='Total Streams')
    ax2 = ax.twinx()
    sns.lineplot(x='Platform', y='Average Likes', data=data_platform_performance, color='r', marker='o', ax=ax2, label='Average Likes')
    ax.figure.legend()
    plt.title('Streaming Performance by Platform')
    plt.show()

def plot_listener_demographics_and_engagement():
    # Example data for listener demographics and engagement
    demographics_data = {'Demographic': ['18-24, Female, Urban', '25-34, Male, Urban', '35-44, Non-binary, Rural', '45-54, Male, Suburban', '18-24, Non-binary, Suburban'],
                          'Count': [300, 500, 200, 100, 400]}
    engagement_data = {'Demographic': ['18-24, Female, Urban', '25-34, Male, Urban', '35-44, Non-binary, Rural', '45-54, Male, Suburban', '18-24, Non-binary, Suburban'],
                       'Average Engagement Score': [150000, 120000, 100000, 90000, 110000]}

    df_demographics = pd.DataFrame(demographics_data)
    df_engagement = pd.DataFrame(engagement_data)

    # Pie chart
    plt.figure(figsize=(14, 7))
    plt.subplot(1, 2, 1)
    plt.pie(df_demographics['Count'], labels=df_demographics['Demographic'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("viridis", len(df_demographics)))
    plt.title('Listener Demographics Distribution')

    # Bar chart
    plt.subplot(1, 2, 2)
    sns.barplot(x='Demographic', y='Average Engagement Score', data=df_engagement, palette='viridis')
    plt.xticks(rotation=45)
    plt.title('Average Engagement Score by Demographic')
    plt.tight_layout()
    plt.show()

def plot_creative_activity_and_collaborations():
    # Example data for creative activity
    data_creative_activity = pd.DataFrame({
        'Creative Name': ['Artist A', 'Artist B', 'Artist C', 'Artist D', 'Artist E'],
        'Performances': [10, 5, 8, 15, 2],
        'Collaborations': [2, 3, 1, 4, 5]
    })

    # Plotting creative activity
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Creative Name', y='Performances', data=data_creative_activity, color='blue', label='Performances')
    sns.barplot(x='Creative Name', y='Collaborations', data=data_creative_activity, color='orange', label='Collaborations', bottom=data_creative_activity['Performances'])
    plt.ylabel('Count')
    plt.title('Creative Activity: Performances and Collaborations')
    plt.legend()
    plt.show()

# Calling functions to execute the plots
plot_streaming_performance()
plot_listener_demographics_and_engagement()
plot_creative_activity_and_collaborations()
