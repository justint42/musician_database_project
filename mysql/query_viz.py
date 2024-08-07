import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import config

sns.set_theme(style="white")

def get_data(query):
    """Fetch data from the MySQL database."""
    connection = mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database
    )
    data = pd.read_sql(query, connection)
    connection.close()
    return data

def visualize_streaming_performance():
    """Visualize streaming performance by platform."""
    query = """
    SELECT sp.platformName, SUM(s.streamCount) AS TotalStreams, AVG(em.likes) AS AverageLikes
    FROM Stream s
    JOIN EngagementMetrics em ON s.engagementMetricID = em.engagementMetricID
    JOIN StreamingPlatforms sp ON sp.platformID = s.streamID
    GROUP BY sp.platformName;
    """
    data = get_data(query)
    print("\nStreaming Performance by Platform:\n", data)

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='platformName', y='TotalStreams', data=data, palette='Blues_d', label='Total Streams')
    ax.grid(False)
    ax2 = ax.twinx()
    line = sns.lineplot(x='platformName', y='AverageLikes', data=data, color='red', marker='o', label='Average Likes', ax=ax2)
    line.grid(False)
    ax.set_xlabel('Platform')
    ax.set_ylabel('Total Streams')
    ax2.set_ylabel('Average Likes')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title('Streaming Performance by Platform')
    plt.show()

def visualize_creative_activity_and_collaborations():
    """Visualize creative activity including performances and collaborations."""
    query = """
    SELECT c.creativeName, COUNT(cp.performanceID) AS Performances, COALESCE(SUM(coll.collaborationID), 0) AS Collaborations
    FROM Creatives c
    LEFT JOIN CreativePerformances cp ON c.creativeID = cp.creativeID
    LEFT JOIN Collaborations coll ON c.creativeID = coll.artist1ID OR c.creativeID = coll.artist2ID
    GROUP BY c.creativeName
    HAVING Performances > 0 OR Collaborations > 0
    ORDER BY Performances + Collaborations DESC;
    """
    data = get_data(query)
    print("\nCreative Activity and Collaborations:\n", data)

    plt.figure(figsize=(12, 8))
    sns.barplot(x='creativeName', y='Performances', data=data, color='skyblue', label='Performances')
    sns.barplot(x='creativeName', y='Collaborations', data=data, color='orange', label='Collaborations', bottom=data['Performances'])
    plt.xticks(rotation=45)
    plt.xlabel('Creative Name')
    plt.ylabel('Number of Activities')
    plt.title('Creative Activity')
    plt.legend()
    plt.tight_layout()
    plt.show()

def visualize_likes_histogram():
    """Visualize the distribution of average likes."""
    query = """
    SELECT AVG(em.likes) AS AverageLikes
    FROM EngagementMetrics em
    GROUP BY em.demographicsID;
    """
    data = get_data(query)
    print("\nAverage Likes by Demographics:\n", data)

    plt.figure(figsize=(8, 6))
    sns.histplot(data['AverageLikes'], bins=20, color='green', kde=True)
    plt.title('Distribution of Average Likes Across Demographics')
    plt.xlabel('Average Likes')
    plt.ylabel('Demographic Group Count')
    plt.show()

def visualize_stream_distribution():
    """Visualize the distribution of total streams across different platforms."""
    query = """
    SELECT sp.platformName, SUM(s.streamCount) AS TotalStreams
    FROM Stream s
    JOIN StreamingPlatforms sp ON sp.platformID = s.streamID
    GROUP BY sp.platformName;
    """
    data = get_data(query)
    print("\nStream Distribution by Platform:\n", data)

    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(data['TotalStreams'], labels=data['platformName'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    plt.title('Total Streams by Platform Distribution')
    plt.show()

if __name__ == "__main__":
    visualize_streaming_performance()
    visualize_creative_activity_and_collaborations()
    visualize_likes_histogram()
    visualize_stream_distribution()
