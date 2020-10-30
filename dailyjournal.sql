CREATE TABLE `JournalEntries` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `concept` TEXT NOT NULL,
  `entry` TEXT NOT NULL,
  `date` INTEGER NOT NULL,
  `moodId` INTEGER NOT NULL,
  FOREIGN KEY(`moodId`) REFERENCES `Moods`(`id`)
);

CREATE TABLE `Moods` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `label` TEXT NOT NULL
);

CREATE TABLE `Tags` (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name` TEXT NOT NULL
);

CREATE TABLE `EntryTags` (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`entry_id` INTEGER NOT NULL,
	`tag_id` INTEGER NOT NULL,
	FOREIGN KEY(`entry_id`) REFERENCES `JournalEntries`(`id`),
	FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

INSERT INTO `Moods` VALUES (null, 'Happy');
INSERT INTO `Moods` VALUES (null, 'Sad');
INSERT INTO `Moods` VALUES (null, 'Angry');
INSERT INTO `Moods` VALUES (null, 'Ok');

INSERT INTO `JournalEntries` VALUES (null, '1234', '123', 1598458543321, 1);
INSERT INTO `JournalEntries` VALUES (null, 'abc', '123', 1598458548239, 2);
INSERT INTO `JournalEntries` VALUES (null, 'Delete', 'Now Deleting', 1598458559152, 1);
INSERT INTO `JournalEntries` VALUES (null, 'ANGRY', 'fgfgdfg', 1598557358781, 3);

INSERT INTO `Tags` VALUES (null, 'Work');
INSERT INTO `Tags` VALUES (null, 'Travel');
INSERT INTO `Tags` VALUES (null, 'Good Day');
INSERT INTO `Tags` VALUES (null, 'Bad Day');

SELECT
    a.id,
    a.concept,
    a.entry,
    a.date,
    a.moodId
FROM journalentries a

SELECT
    a.id,
    a.label
FROM moods a

DELETE FROM JournalEntries
WHERE id=2

SELECT
    c.id,
    c.concept,
    c.entry,
    c.date,
    c.moodId
FROM journalentries c
WHERE term LIKE %searchTerm%

SELECT
	j.id,
	j.concept,
	j.entry,
	j.date,
	j.moodId,
	m.label
FROM journalentries j
JOIN moods m
	ON m.id = j.moodId

UPDATE journalentries
SET concept = "testing again"
WHERE id = 1

SELECT * FROM EntryTags


SELECT
	t.id,
	t.name,
	e.tag_id
FROM tags t
JOIN entrytags e
	ON t.id = e.tag_id
WHERE e.entry_id = 14
