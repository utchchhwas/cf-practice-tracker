
DROP TABLE PROBLEM_LOGS;

CREATE TABLE PROBLEM_LOGS (
	USERNAME VARCHAR2(255),
	CONTEST_ID NUMBER,
	PROBLEM_INDEX VARCHAR2(10),
	PROBLEM_STATUS VARCHAR2(255),
	PERSONAL_COMMENT CLOB
);

ALTER TABLE PROBLEM_LOGS
ADD	CONSTRAINT PROBLEM_LOGS_PK
		PRIMARY KEY (USERNAME, CONTEST_ID, PROBLEM_INDEX);

ALTER TABLE PROBLEM_LOGS
ADD CONSTRAINT PROBLEM_LOGS_FK_1
	FOREIGN KEY (CONTEST_ID, PROBLEM_INDEX)
	REFERENCES PROBLEMS (CONTEST_ID, PROBLEM_INDEX);

ALTER TABLE PROBLEM_LOGS
ADD CONSTRAINT PROBLEM_LOGS_USERNAME_FK_2
	FOREIGN KEY (USERNAME)
	REFERENCES USERS (USERNAME);

SELECT * FROM PROBLEM_LOGS
WHERE
	USERNAME = 'utchchhwas'
	AND CONTEST_ID = 4
	AND PROBLEM_INDEX = 'A'
;

SELECT
	* 
FROM
	PROBLEM_LOGS 
WHERE
	USERNAME = 'utchchhwas'
	AND CONTEST_ID = 4
	AND PROBLEM_INDEX = 'A'

DELETE FROM PROBLEM_LOGS;

INSERT INTO
PROBLEM_LOGS
VALUES ('utchchhwas', 4, 'A', 'TODO', '# This is a Heading');


SELECT 
	*
FROM 
	PROBLEM_LOGS
	INNER JOIN PROBLEMS
	USING (CONTEST_ID, PROBLEM_INDEX)
WHERE
	USERNAME = 'utchchhwas'
	AND PROBLEM_STATUS = 'TODO'
;
