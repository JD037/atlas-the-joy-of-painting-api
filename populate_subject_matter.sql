-- Create a temporary table to store the subject matter data
CREATE TEMPORARY TABLE subjectmatter (
    episode TEXT,
    title TEXT,
    subject TEXT
);

-- Copy the data from the CSV file into the temporary table
\copy subjectmatter FROM 'atlas-the-joy-of-painting-api/SubjectMatter.csv' CSV HEADER;

-- Populate the subject_matter column in the episodes table
UPDATE episodes e
SET subject_matter = sm.subject
FROM subjectmatter sm
WHERE e.title = sm.episode;

-- Drop the temporary table
DROP TABLE subjectmatter;