-- Drop existing tables in dependency order
DROP TABLE IF EXISTS Demographics;
DROP TABLE IF EXISTS StreamingPlatforms;
DROP TABLE IF EXISTS SocialMediaPlatforms;
DROP TABLE IF EXISTS Listeners;
DROP TABLE IF EXISTS ListenerPlatforms;
DROP TABLE IF EXISTS Stream;
DROP TABLE IF EXISTS EngagementMetrics;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS EventTypes;
DROP TABLE IF EXISTS Creatives;
DROP TABLE IF EXISTS CreativePlatforms;
DROP TABLE IF EXISTS ContentDistribution;
DROP TABLE IF EXISTS RecordingProjects;
DROP TABLE IF EXISTS RecordingStudios;
DROP TABLE IF EXISTS Albums;
DROP TABLE IF EXISTS Songs;
DROP TABLE IF EXISTS SongWriters;
DROP TABLE IF EXISTS Performances;
DROP TABLE IF EXISTS CreativePerformances;
DROP TABLE IF EXISTS CreativeEventManagement;
DROP TABLE IF EXISTS ListenerPreferences;
DROP TABLE IF EXISTS Collaborations;
DROP TABLE IF EXISTS SongAlbums;

-- Create tables in the correct order

CREATE TABLE Demographics (
    demographicsID INTEGER PRIMARY KEY AUTO_INCREMENT,
    demographicInfo VARCHAR(255) NOT NULL
);

CREATE TABLE StreamingPlatforms (
    platformID INTEGER PRIMARY KEY AUTO_INCREMENT,
    platformName VARCHAR(255) NOT NULL,
    platformRegion VARCHAR(100)
);

CREATE TABLE SocialMediaPlatforms (
    platformID INTEGER PRIMARY KEY AUTO_INCREMENT,
    platformName VARCHAR(255) NOT NULL,
    platformType VARCHAR(100)
);

CREATE TABLE Listeners (
    listenerID INTEGER PRIMARY KEY AUTO_INCREMENT,
    listenerName VARCHAR(255) NOT NULL,
    listenerDemographicsID INTEGER,
    FOREIGN KEY (listenerDemographicsID) REFERENCES Demographics(demographicsID) ON DELETE SET NULL
);

CREATE TABLE ListenerPlatforms (
    listenerID INTEGER,
    platformID INTEGER,
    userIdentifier VARCHAR(255) NOT NULL,
    platformType VARCHAR(100) NOT NULL,
    PRIMARY KEY (listenerID, platformID, platformType),
    FOREIGN KEY (listenerID) REFERENCES Listeners(listenerID) ON DELETE CASCADE,
    FOREIGN KEY (platformID) REFERENCES StreamingPlatforms(platformID) ON DELETE CASCADE
);

CREATE TABLE EngagementMetrics (
    engagementMetricID INTEGER PRIMARY KEY AUTO_INCREMENT,
    streamTime TIME,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    demographicsID INTEGER,
    FOREIGN KEY (demographicsID) REFERENCES Demographics(demographicsID) ON DELETE SET NULL
);

CREATE TABLE Stream (
    streamID INTEGER PRIMARY KEY AUTO_INCREMENT,
    streamName VARCHAR(255) NOT NULL,
    streamCount INTEGER DEFAULT 0,
    streamDate DATE,
    engagementMetricID INTEGER,
    FOREIGN KEY (engagementMetricID) REFERENCES EngagementMetrics(engagementMetricID) ON DELETE CASCADE
);

CREATE TABLE EventTypes (
    eventTypeID INTEGER PRIMARY KEY AUTO_INCREMENT,
    eventTypeName VARCHAR(255) NOT NULL
);

CREATE TABLE Events (
    eventID INTEGER PRIMARY KEY AUTO_INCREMENT,
    eventName VARCHAR(255) NOT NULL,
    eventDate DATE,
    eventLocation VARCHAR(255),
    eventTypeID INTEGER,
    FOREIGN KEY (eventTypeID) REFERENCES EventTypes(eventTypeID) ON DELETE SET NULL
);

CREATE TABLE Creatives (
    creativeID INTEGER PRIMARY KEY AUTO_INCREMENT,
    creativeName VARCHAR(255) NOT NULL,
    creativeType VARCHAR(100) NOT NULL
);

CREATE TABLE CreativePlatforms (
    creativeID INTEGER,
    platformID INTEGER,
    userIdentifier VARCHAR(255) NOT NULL,
    platformType VARCHAR(100) NOT NULL,
    PRIMARY KEY (creativeID, platformID, platformType),
    FOREIGN KEY (creativeID) REFERENCES Creatives(creativeID) ON DELETE CASCADE,
    FOREIGN KEY (platformID) REFERENCES StreamingPlatforms(platformID) ON DELETE CASCADE
);

CREATE TABLE ContentDistribution (
    contentID INTEGER,
    contentType VARCHAR(100) NOT NULL,
    platformID INTEGER,
    releaseDate DATE,
    status VARCHAR(100) NOT NULL,
    performanceMetrics VARCHAR(255),
    PRIMARY KEY (contentID, contentType, platformID),
    FOREIGN KEY (platformID) REFERENCES StreamingPlatforms(platformID) ON DELETE CASCADE
);

CREATE TABLE RecordingStudios (
    recordingStudioID INTEGER PRIMARY KEY AUTO_INCREMENT,
    studioName VARCHAR(255) NOT NULL,
    studioLocation VARCHAR(255)
);

CREATE TABLE RecordingProjects (
    recordingProjectID INTEGER PRIMARY KEY AUTO_INCREMENT,
    recordingProjectName VARCHAR(255) NOT NULL,
    recordingProjectDate DATE,
    recordingStudioID INTEGER,
    FOREIGN KEY (recordingStudioID) REFERENCES RecordingStudios(recordingStudioID) ON DELETE SET NULL
);

CREATE TABLE Albums (
    albumID INTEGER PRIMARY KEY AUTO_INCREMENT,
    albumName VARCHAR(255) NOT NULL,
    releaseDate DATE,
    recordingProjectID INTEGER,
    FOREIGN KEY (recordingProjectID) REFERENCES RecordingProjects(recordingProjectID) ON DELETE SET NULL
);

CREATE TABLE Songs (
    songID INTEGER PRIMARY KEY AUTO_INCREMENT,
    songName VARCHAR(255) NOT NULL,
    albumID INTEGER,
    length TIME,
    FOREIGN KEY (albumID) REFERENCES Albums(albumID) ON DELETE SET NULL
);

CREATE TABLE SongWriters (
    songID INTEGER,
    songwriterID INTEGER,
    PRIMARY KEY (songID, songwriterID),
    FOREIGN KEY (songID) REFERENCES Songs(songID) ON DELETE CASCADE,
    FOREIGN KEY (songwriterID) REFERENCES Creatives(creativeID) ON DELETE CASCADE
);

CREATE TABLE Performances (
    performanceID INTEGER PRIMARY KEY AUTO_INCREMENT,
    performanceName VARCHAR(255) NOT NULL,
    performanceDate DATE,
    performanceLocation VARCHAR(255),
    eventID INTEGER,
    isImpromptu BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (eventID) REFERENCES Events(eventID) ON DELETE SET NULL
);

CREATE TABLE CreativePerformances (
    creativeID INTEGER,
    performanceID INTEGER,
    PRIMARY KEY (creativeID, performanceID),
    FOREIGN KEY (creativeID) REFERENCES Creatives(creativeID) ON DELETE CASCADE,
    FOREIGN KEY (performanceID) REFERENCES Performances(performanceID) ON DELETE CASCADE
);

CREATE TABLE CreativeEventManagement (
    creativeID INTEGER,
    eventID INTEGER,
    role VARCHAR(100) NOT NULL,
    isPrimaryManager BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (creativeID, eventID),
    FOREIGN KEY (creativeID) REFERENCES Creatives(creativeID) ON DELETE CASCADE,
    FOREIGN KEY (eventID) REFERENCES Events(eventID) ON DELETE CASCADE
);

CREATE TABLE ListenerPreferences (
    listenerID INTEGER,
    creativeID INTEGER,
    engagementScore INTEGER CHECK (engagementScore >= 0),
    PRIMARY KEY (listenerID, creativeID),
    FOREIGN KEY (listenerID) REFERENCES Listeners(listenerID) ON DELETE CASCADE,
    FOREIGN KEY (creativeID) REFERENCES Creatives(creativeID) ON DELETE CASCADE
);

CREATE TABLE Collaborations (
    collaborationID INTEGER PRIMARY KEY AUTO_INCREMENT,
    artist1ID INTEGER,
    artist2ID INTEGER,
    collaborationDate DATE,
    FOREIGN KEY (artist1ID) REFERENCES Creatives(creativeID) ON DELETE CASCADE,
    FOREIGN KEY (artist2ID) REFERENCES Creatives(creativeID) ON DELETE CASCADE
);

CREATE TABLE SongAlbums (
    contentID INTEGER,
    contentType VARCHAR(100) NOT NULL,
    associatedContentID INTEGER,
    associatedContentType VARCHAR(100) NOT NULL,
    trackNumber INTEGER,
    PRIMARY KEY (contentID, contentType, associatedContentID, associatedContentType)
);
