-- Create a temporary table to store the subject matter data
CREATE TEMPORARY TABLE subjectmatter (
    episode TEXT,
    title TEXT,
    subject TEXT
);

-- Copy the data from the CSV file into the temporary table
\copy subjectmatter FROM 'atlas-the-joy-of-painting-api/SubjectMatter.csv' CSV HEADER;

-- Populate the colors table
INSERT INTO colors (name, episode_id)
SELECT sm.color_name, e.id
FROM (
    SELECT DISTINCT episode, UNNEST(STRING_TO_ARRAY(subject, ', ')) AS color_name
    FROM subjectmatter
) sm
JOIN episodes e ON e.title = sm.episode;

-- Drop the temporary table
DROP TABLE subjectmatter;