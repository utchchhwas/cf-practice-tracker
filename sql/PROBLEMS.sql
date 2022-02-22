DROP TABLE PROBLEMS;


CREATE TABLE PROBLEMS (
	CONTEST_ID NUMBER,
	PROBLEM_INDEX VARCHAR2(10),
	PROBLEM_NAME VARCHAR2(255) NOT NULL,
	PROBLEM_RATING NUMBER
);

ALTER TABLE PROBLEMS
ADD	CONSTRAINT PROBLEMS_PK_CONTEST_ID_PROBLEM_INDEX
		PRIMARY KEY (CONTEST_ID, PROBLEM_INDEX)

ALTER TABLE PROBLEMS
ADD CONSTRAINT PROBLEMS_FK
	FOREIGN KEY (CONTEST_ID) 
	REFERENCES CONTESTS (CONTEST_ID);

SELECT * FROM PROBLEMS;

SELECT COUNT(*) FROM PROBLEMS;

DELETE FROM PROBLEMS;