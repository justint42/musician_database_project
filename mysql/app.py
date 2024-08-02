# db_connection_viz.py

import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ykwim2020',  # Update with your MySQL root password
            database='musician'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(connection, query):
    """Execute a given SQL query and return the results."""
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def plot_pie_chart(data, title):
    """Plot a pie chart for the given data."""
    labels = [x[0] for x in data]
    sizes = [x[1] for x in data]
    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def plot_bar_chart(data, title, xlabel, ylabel):
    """Plot a bar chart for the given data."""
    labels = [x[0] for x in data]
    values = [x[1] for x in data]
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_heatmap(data, title):
    """Plot a heatmap for event locations by month with months displayed horizontally."""
    df = pd.DataFrame(data, columns=['Month', 'Location', 'Count'])
    # Convert 'Month' to a categorical type with ordered categories
    months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
    df['Month'] = pd.Categorical(df['Month'], categories=months_order, ordered=True)
    df_pivot = df.pivot("Location", "Month", "Count")
    plt.figure(figsize=(14, 8))
    sns.heatmap(df_pivot, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Event Count'})
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel('Location')
    plt.xticks(rotation=45)  # Rotate month labels for better readability
    plt.show()





def main():
    connection = create_connection()
    if connection:
        # Execute each query and directly output results
        results = {
            "Listeners": execute_query(connection, "SELECT Name FROM Listeners;"),
            "Total Number of Listeners per Platform": execute_query(connection, """
                SELECT SP.Name AS PlatformName, COUNT(LSP.ListenerID) AS TotalListeners
                FROM StreamingPlatforms SP
                JOIN ListenerStreamingPlatforms LSP ON SP.PlatformID = LSP.PlatformID
                GROUP BY SP.Name
                ORDER BY TotalListeners DESC;
            """),
            "Creatives and Their Managed Events": execute_query(connection, """
                SELECT C.Name AS CreativeName, E.Name AS EventName, E.Date, E.Location, CEM.Role
                FROM Creatives C
                INNER JOIN CreativeEventManagement CEM ON C.CreativeID = CEM.CreativeID
                INNER JOIN Events E ON CEM.EventID = E.EventID;
            """),
            "Listeners on Popular Platform": execute_query(connection, """
                SELECT L.Name AS ListenerName
                FROM Listeners L
                WHERE L.ListenerID IN (
                    SELECT LSP.ListenerID
                    FROM ListenerStreamingPlatforms LSP
                    WHERE LSP.PlatformID = (
                        SELECT SP.PlatformID
                        FROM StreamingPlatforms SP
                        JOIN ListenerStreamingPlatforms LSP ON SP.PlatformID = LSP.PlatformID
                        GROUP BY SP.PlatformID
                        ORDER BY COUNT(LSP.ListenerID) DESC
                        LIMIT 1
                    )
                );
            """),
            "Creatives in New York": execute_query(connection, """
                SELECT C.Name AS CreativeName
                FROM Creatives C
                WHERE EXISTS (
                    SELECT 1
                    FROM CreativeEventManagement CEM
                    JOIN Events E ON CEM.EventID = E.EventID
                    WHERE CEM.CreativeID = C.CreativeID
                    AND E.Location = 'New York'
                );
            """),
            "Listeners Interested in Sophia Davis": execute_query(connection, """
                SELECT L.Name AS ListenerName
                FROM Listeners L
                WHERE EXISTS (
                    SELECT 1
                    FROM ListenerPreferences LP
                    WHERE LP.ListenerID = L.ListenerID
                    AND LP.CreativeID = (SELECT CreativeID FROM Creatives WHERE Name = 'Sophia Davis')
                );
            """),
            "Listeners on Streaming/Social Media": execute_query(connection, """
                SELECT L.Name AS ListenerName, 'Streaming' AS PlatformType
                FROM Listeners L
                JOIN ListenerStreamingPlatforms LSP ON L.ListenerID = LSP.ListenerID

                UNION

                SELECT L.Name AS ListenerName, 'Social Media' AS PlatformType
                FROM Listeners L
                JOIN ListenerSocialMediaPlatforms LSM ON L.ListenerID = LSM.ListenerID;
            """),
            "Creatives with 2024 Events": execute_query(connection, """
                SELECT C.Name AS CreativeName, E.Name AS MostRecentEventName, E.Date AS MostRecentEventDate
                FROM Creatives C
                JOIN (
                    SELECT CEM.CreativeID, MAX(E.Date) AS MostRecentEventDate
                    FROM CreativeEventManagement CEM
                    JOIN Events E ON CEM.EventID = E.EventID
                    WHERE YEAR(E.Date) = 2024
                    GROUP BY CEM.CreativeID
                ) RecentEvents ON C.CreativeID = RecentEvents.CreativeID
                JOIN Events E ON RecentEvents.MostRecentEventDate = E.Date AND RecentEvents.CreativeID = C.CreativeID;
            """)
        }

        # Print results
        for key, value in results.items():
            print(f"\n{key}:")
            for row in value:
                print(row)

        # Query for Event Engagements
        event_engagement_query = """
            SELECT ET.Name AS EventType, AVG(LP.EngagementScore) AS AverageEngagement
            FROM ListenerPreferences LP
            JOIN Creatives C ON LP.CreativeID = C.CreativeID
            JOIN CreativeEventManagement CEM ON C.CreativeID = CEM.CreativeID
            JOIN Events E ON CEM.EventID = E.EventID
            JOIN EventTypes ET ON E.TypeID = ET.TypeID
            GROUP BY ET.Name
            ORDER BY AverageEngagement DESC;
        """
        event_engagement_data = execute_query(connection, event_engagement_query)
        plot_bar_chart(event_engagement_data, 'Average Engagement Scores by Event Type', 'Event Type', 'Average Engagement Score')

        # Query for Listener Distribution on Platforms
        platform_distribution_query = """
            SELECT SP.Name AS PlatformName, COUNT(LSP.ListenerID) AS ListenerCount
            FROM StreamingPlatforms SP
            JOIN ListenerStreamingPlatforms LSP ON SP.PlatformID = LSP.PlatformID
            GROUP BY SP.Name
            ORDER BY ListenerCount DESC;
        """
        platform_distribution_data = execute_query(connection, platform_distribution_query)
        plot_pie_chart(platform_distribution_data, 'Distribution of Listeners Across Streaming Platforms')


        # New query for heatmap data
        event_location_data = execute_query(connection, """
            SELECT MONTHNAME(E.Date) AS Month, E.Location, COUNT(*) AS Count
            FROM Events E
            GROUP BY MONTHNAME(E.Date), E.Location
            ORDER BY STR_TO_DATE(CONCAT('01-', Month), '%d-%M') ASC;
        """)

        plot_heatmap(event_location_data, 'Monthly Distribution of Events Across Locations')

        connection.close()

if __name__ == "__main__":
    main()
