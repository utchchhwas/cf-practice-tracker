DROP TABLE PROBLEM_TAGS;

CREATE TABLE PROBLEM_TAGS (
	CONTEST_ID NUMBER,
	PROBLEM_INDEX VARCHAR2(10),
	TAG_NAME VARCHAR2(255),
	CONSTRAINT PROBLEMS_TAGS_PK 
		PRIMARY KEY (CONTEST_ID, PROBLEM_INDEX, TAG_NAME)
);

ALTER TABLE PROBLEM_TAGS
ADD CONSTRAINT PROBLEM_TAGS_FK
	FOREIGN KEY (CONTEST_ID, PROBLEM_INDEX) 
	REFERENCES PROBLEMS (CONTEST_ID, PROBLEM_INDEX);
	
SELECT * FROM PROBLEM_TAGS;

SELECT CONTEST_ID, PROBLEM_INDEX FROM PROBLEM_TAGS
GROUP BY CONTEST_ID, PROBLEM_INDEX;

DELETE FROM PROBLEM_TAGS;