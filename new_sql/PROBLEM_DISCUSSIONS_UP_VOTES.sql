
DROP TABLE PROBLEM_DISCUSSIONS_UP_VOTES;

CREATE TABLE PROBLEM_DISCUSSIONS_UP_VOTES  (
	ID NUMBER,
	USERNAME VARCHAR2(255)
);

ALTER TABLE PROBLEM_DISCUSSIONS_UP_VOTES
ADD	CONSTRAINT PROBLEM_DISCUSSIONS_UP_VOTES_PK 
	PRIMARY KEY (ID, USERNAME);
	

ALTER TABLE PROBLEM_DISCUSSIONS_UP_VOTES
ADD	CONSTRAINT PROBLEM_DISCUSSIONS_UP_VOTES_FK_1 
	FOREIGN KEY (ID)
	REFERENCES PROBLEM_DISCUSSIONS (ID);


ALTER TABLE PROBLEM_DISCUSSIONS_UP_VOTES
ADD	CONSTRAINT PROBLEM_DISCUSSIONS_UP_VOTES_FK_2
	FOREIGN KEY (USERNAME)
	REFERENCES USERS (USERNAME);