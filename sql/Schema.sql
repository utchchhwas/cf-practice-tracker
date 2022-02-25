-- Database Schema

-- CF_USERS SCHEMA
CREATE TABLE CF_USERS (
	CF_HANDLE VARCHAR2(255),
	FIRST_NAME VARCHAR2(255),
	LAST_NAME VARCHAR2(255),
	RATING NUMBER,
	MAX_RATING NUMBER,
	RANK VARCHAR2(255),
	MAX_RANK VARCHAR2(255),
	TITLE_PHOTO_URL VARCHAR2(255),
	COUNTRY VARCHAR2(255)
);

ALTER TABLE CF_USERS
ADD CONSTRAINT CF_USERS_PK
		PRIMARY KEY (CF_HANDLE);
-- 	END OF SCHEMA

-- CONTEST TABLE SCHEMA
CREATE TABLE CONTESTS (
	CONTEST_ID NUMBER,
	CONTEST_NAME VARCHAR2(255) NOT NULL,
	START_TIME DATE NOT NULL
);

ALTER TABLE CONTESTS
ADD CONSTRAINT CONTESTS_PK
		PRIMARY KEY (CONTEST_ID);
-- END OF SCHEMA

-- PROBLEMS TABLE SCHEMA
CREATE TABLE PROBLEMS (
	CONTEST_ID NUMBER,
	PROBLEM_INDEX VARCHAR2(10),
	PROBLEM_NAME VARCHAR2(255) NOT NULL,
	PROBLEM_RATING NUMBER
);

ALTER TABLE PROBLEMS
ADD	CONSTRAINT PROBLEMS_PK
		PRIMARY KEY (CONTEST_ID, PROBLEM_INDEX);
	
ALTER TABLE PROBLEMS
ADD CONSTRAINT PROBLEMS_FK
	FOREIGN KEY (CONTEST_ID) 
	REFERENCES CONTESTS (CONTEST_ID);
-- END OF SCHEMA

-- SUBMISSIONS TABLE SCHEMA
CREATE TABLE SUBMISSIONS (
	SUBMISSION_ID NUMBER,
	CF_HANDLE VARCHAR2(255),
	CONTEST_ID NUMBER,
	PROBLEM_INDEX VARCHAR2(10),
	CREATION_TIME DATE NOT NULL,
	PROGRAMMING_LANG VARCHAR2(255) NOT NULL,
	VERDICT VARCHAR2(255) NOT NULL
);

ALTER TABLE SUBMISSIONS
ADD	CONSTRAINT SUBMISSIONS_PK
	PRIMARY KEY (SUBMISSION_ID);

ALTER TABLE SUBMISSIONS
ADD CONSTRAINT SUBMISSIONS_FK_1
	FOREIGN KEY (CF_HANDLE)
	REFERENCES CF_USERS (CF_HANDLE);

ALTER TABLE SUBMISSIONS
ADD CONSTRAINT SUBMISSIONS_FK_2
	FOREIGN KEY (CONTEST_ID, PROBLEM_INDEX) 
	REFERENCES PROBLEMS (CONTEST_ID, PROBLEM_INDEX);
-- END OF SCHEMA

-- USERS TABLE SCHEMA
CREATE TABLE USERS (
	USERNAME VARCHAR2(255),
	PASSWORD VARCHAR2(255) NOT NULL,
	CF_HANDLE VARCHAR2(255) NOT NULL,
	IS_ADMIN CHAR(1) DEFAULT 'N'
);

ALTER TABLE USERS
ADD	CONSTRAINT USERS_PK
	PRIMARY KEY (USERNAME);

ALTER TABLE USERS
ADD CONSTRAINT USERS_FK
	FOREIGN KEY (CF_HANDLE)
	REFERENCES CF_USERS (CF_HANDLE);
-- END OF SCHEMA

-- PROBLEM_TAGS SCHEMA
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
-- 	END OF SCHEMA

-- PROBLEM_LOGS SCHEMA
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
ADD CONSTRAINT PROBLEM_LOGS_FK_2
	FOREIGN KEY (USERNAME)
	REFERENCES USERS (USERNAME);
-- 	END OF SCHEMA

-- PROBLEM_DISCUSSIONS
CREATE TABLE PROBLEM_DISCUSSIONS (
	ID NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY,
	AUTHOR VARCHAR2(255),
	CONTEST_ID NUMBER,
	PROBLEM_INDEX VARCHAR2(10),
	LAST_UPDATE_TIME DATE DEFAULT SYSDATE,
	CONTENT CLOB
);

ALTER TABLE PROBLEM_DISCUSSIONS
ADD	CONSTRAINT PROBLEM_DISCUSSIONS_PK 
	PRIMARY KEY (ID);

ALTER TABLE PROBLEM_DISCUSSIONS
ADD CONSTRAINT PROBLEM_DISCUSSIONS_FK_1
	FOREIGN KEY (AUTHOR)
	REFERENCES USERS (USERNAME);

ALTER TABLE PROBLEM_DISCUSSIONS
ADD CONSTRAINT PROBLEM_DISCUSSIONS_FK_2
	FOREIGN KEY (CONTEST_ID, PROBLEM_INDEX)
	REFERENCES PROBLEMS (CONTEST_ID, PROBLEM_INDEX);
-- 	END OF SCHEMA

-- PROBLEM_DISCUSSIONS_UP_VOTES SCHEMA
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
-- 	END OF SCHEMA

-- CONTEST_PARTICIPATIONS SCHEMA
CREATE TABLE CONTEST_PARTICIPATIONS (
	CF_HANDLE VARCHAR2(255),
	CONTEST_ID NUMBER,
	CONTEST_RANK NUMBER,
	OLD_RATING NUMBER,
	NEW_RATING NUMBER
);

ALTER TABLE CONTEST_PARTICIPATIONS
ADD	CONSTRAINT CONTEST_PARTICIPATIONS_PK
	PRIMARY KEY (CF_HANDLE, CONTEST_ID);

ALTER TABLE CONTEST_PARTICIPATIONS
ADD CONSTRAINT CONTEST_PARTICIPATIONS_FK_1
	FOREIGN KEY (CF_HANDLE)
	REFERENCES CF_USERS (CF_HANDLE);

ALTER TABLE CONTEST_PARTICIPATIONS
ADD CONSTRAINT CONTEST_PARTICIPATIONS_FK_2
	FOREIGN KEY (CONTEST_ID)
	REFERENCES CONTESTS (CONTEST_ID);
-- 	END OF SCHEMA
