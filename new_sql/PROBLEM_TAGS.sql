
DROP TABLE PROBLEM_TAGS;

CREATE TABLE PROBLEM_TAGS (
	CONTEST_ID NUMBER,
	PROBLEM_INDEX VARCHAR2(10),
	TAG_NAME VARCHAR2(255)
);

ALTER TABLE PROBLEM_TAGS
ADD	CONSTRAINT PROBLEMS_TAGS_PK 
		PRIMARY KEY (CONTEST_ID, PROBLEM_INDEX, TAG_NAME);
		
ALTER TABLE PROBLEM_TAGS
ADD CONSTRAINT PROBLEM_TAGS_FK
	FOREIGN KEY (CONTEST_ID, PROBLEM_INDEX) 
	REFERENCES PROBLEMS (CONTEST_ID, PROBLEM_INDEX);
	
SELECT COUNT(*) FROM PROBLEM_TAGS;

SELECT CONTEST_ID, PROBLEM_INDEX FROM PROBLEM_TAGS
GROUP BY CONTEST_ID, PROBLEM_INDEX;

DELETE FROM PROBLEM_TAGS;

SELECT 
		T.TAG_NAME,
		(
		SELECT
				COUNT(*)
		FROM
				(
				SELECT 
						CONTEST_ID, PROBLEM_INDEX
				FROM 
						PROBLEMS
						INNER JOIN SUBMISSIONS
						USING (CONTEST_ID, PROBLEM_INDEX)
						INNER JOIN PROBLEM_TAGS
						USING (CONTEST_ID, PROBLEM_INDEX)
				WHERE
						TAG_NAME = T.TAG_NAME
						AND CF_HANDLE = 'utchchhwas'
						AND VERDICT = 'OK'
				GROUP BY
						CONTEST_ID,
						PROBLEM_INDEX
				)
		) NUM
FROM
		( 
				SELECT 
						DISTINCT TAG_NAME 
				FROM 
						PROBLEM_TAGS
		) T
ORDER BY
		T.TAG_NAME ASC
	