DROP TABLE PROBLEM_TUTORIALS;


CREATE TABLE PROBLEM_TUTORIALS (
	TUTORIAL_ID NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY,
	AUTHOR VARCHAR2(255),
	CONTEST_ID NUMBER,
	PROBLEM_INDEX VARCHAR2(10),
	CREATION_TIME DATE,
	LAST_UPDATE_TIME DATE,
	CONTENT CLOB,
	UP_VOTES NUMBER,
	CONSTRAINT PROBLEM_TUTORIALS_PK 
	PRIMARY KEY (TUTORIAL_ID)
);

ALTER TABLE PROBLEM_TUTORIALS
ADD CONSTRAINT PROBLEM_TUTORIALS_AUTHOR_FK
	FOREIGN KEY (AUTHOR)
	REFERENCES USERS (USERNAME)
;

ALTER TABLE PROBLEM_TUTORIALS
ADD CONSTRAINT PROBLEM_TUTORIALS_PROBLEM_ID_FK
	FOREIGN KEY (CONTEST_ID, PROBLEM_INDEX)
	REFERENCES PROBLEMS (CONTEST_ID, PROBLEM_INDEX)
;

SELECT * FROM PROBLEM_TUTORIALS;

INSERT INTO
PROBLEM_TUTORIALS (AUTHOR)
VALUES ('utchchhwas')
;