CREATE TABLE Listeners (
    ListenerID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE StreamingPlatforms (
    PlatformID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Region VARCHAR(255)
);

CREATE TABLE SocialMediaPlatforms (
    PlatformID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Type VARCHAR(255)
);

CREATE TABLE ListenerStreamingPlatforms (
    ListenerID INT NOT NULL,
    PlatformID INT NOT NULL,
    UserIdentifier VARCHAR(255) NOT NULL,
    PRIMARY KEY (ListenerID, PlatformID),
    FOREIGN KEY (ListenerID) REFERENCES Listeners(ListenerID),
    FOREIGN KEY (PlatformID) REFERENCES StreamingPlatforms(PlatformID)
);

CREATE TABLE ListenerSocialMediaPlatforms (
    ListenerID INT NOT NULL,
    PlatformID INT NOT NULL,
    UserIdentifier VARCHAR(255) NOT NULL,
    PRIMARY KEY (ListenerID, PlatformID),
    FOREIGN KEY (ListenerID) REFERENCES Listeners(ListenerID),
    FOREIGN KEY (PlatformID) REFERENCES SocialMediaPlatforms(PlatformID)
);

CREATE TABLE EventTypes (
    TypeID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE Events (
    EventID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Date DATE,
    Location VARCHAR(255),
    TypeID INT NOT NULL,
    FOREIGN KEY (TypeID) REFERENCES EventTypes(TypeID)
);

CREATE TABLE Creatives (
    CreativeID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Type VARCHAR(255) NOT NULL
);

CREATE TABLE CreativePlatforms (
    CreativeID INT NOT NULL,
    PlatformID INT NOT NULL,
    UserIdentifier VARCHAR(255) NOT NULL,
    PlatformType VARCHAR(255) NOT NULL,
    PRIMARY KEY (CreativeID, PlatformID),
    FOREIGN KEY (CreativeID) REFERENCES Creatives(CreativeID)
);

CREATE TABLE ContentDistribution (
    ContentID INT NOT NULL,
    ContentType VARCHAR(255) NOT NULL,
    PlatformID INT NOT NULL,
    ReleaseDate DATE,
    Status VARCHAR(255) NOT NULL,
    PerformanceMetrics VARCHAR(255),
    PRIMARY KEY (ContentID, ContentType, PlatformID),
    FOREIGN KEY (PlatformID) REFERENCES StreamingPlatforms(PlatformID)
);

CREATE TABLE RecordingStudios (
    StudioID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Location VARCHAR(255)
);

CREATE TABLE RecordingProjects (
    ProjectID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Date DATE,
    StudioID INT NOT NULL,
    ProducerID INT NOT NULL,
    ManyProducers BOOLEAN NOT NULL,
    FOREIGN KEY (StudioID) REFERENCES RecordingStudios(StudioID)
);

CREATE TABLE Albums (
    AlbumID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    ReleaseDate DATE,
    ProjectID INT NOT NULL,
    DesignerID INT,
    ManyDesigners BOOLEAN NOT NULL,
    FOREIGN KEY (ProjectID) REFERENCES RecordingProjects(ProjectID)
);

CREATE TABLE Songs (
    SongID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Length TIME,
    IsStandaloneTrack BOOLEAN NOT NULL
);

CREATE TABLE SongAlbums (
    ContentID INT NOT NULL,
    ContentType VARCHAR(255) NOT NULL,
    AssociatedContentID INT NOT NULL,
    AssociatedContentType VARCHAR(255) NOT NULL,
    TrackNumber INT,
    PRIMARY KEY (ContentID, ContentType, AssociatedContentID, AssociatedContentType)
);

CREATE TABLE SongWriters (
    SongID INT NOT NULL,
    SongwriterID INT NOT NULL,
    PRIMARY KEY (SongID, SongwriterID)
);

CREATE TABLE Performances (
    PerformanceID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Date DATE,
    Location VARCHAR(255),
    EventID INT,
    IsImpromptu BOOLEAN NOT NULL,
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE CreativePerformances (
    CreativeID INT NOT NULL,
    PerformanceID INT NOT NULL,
    PRIMARY KEY (CreativeID, PerformanceID),
    FOREIGN KEY (CreativeID) REFERENCES Creatives(CreativeID),
    FOREIGN KEY (PerformanceID) REFERENCES Performances(PerformanceID)
);

CREATE TABLE CreativeEventManagement (
    CreativeID INT NOT NULL,
    EventID INT NOT NULL,
    Role VARCHAR(255) NOT NULL,
    IsPrimaryManager BOOLEAN NOT NULL,
    PRIMARY KEY (CreativeID, EventID),
    FOREIGN KEY (CreativeID) REFERENCES Creatives(CreativeID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE ListenerPreferences (
    ListenerID INT NOT NULL,
    CreativeID INT NOT NULL,
    EngagementScore INT NOT NULL,
    PRIMARY KEY (ListenerID, CreativeID),
    FOREIGN KEY (ListenerID) REFERENCES Listeners(ListenerID),
    FOREIGN KEY (CreativeID) REFERENCES Creatives(CreativeID)
);
