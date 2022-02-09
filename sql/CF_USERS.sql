DROP TABLE CF_USERS;

CREATE TABLE CF_USERS (
	CF_HANDLE VARCHAR2(255),
	FIRST_NAME VARCHAR2(255),
	LAST_NAME VARCHAR2(255),
	RATING NUMBER,
	MAX_RATING NUMBER,
	RANK VARCHAR2(255),
	MAX_RANK VARCHAR2(255),
	CONTRIBUTION NUMBER,
	AVATAR_URL VARCHAR2(255),
	TITLE_PHOTO_URL VARCHAR2(255),
	COUNTRY VARCHAR2(255),
	CITY VARCHAR2(255),
	ORGANIZATION VARCHAR2(255),
	LAST_ONLINE_TIME DATE,
	REGISTRATION_TIME DATE,
	CONSTRAINT CF_USERS_PK 
		PRIMARY KEY (CF_HANDLE)
);

ALTER TABLE CF_USERS
ADD CONSTRAINT CF_USERS_RANK_FK
	FOREIGN KEY (RANK)
	REFERENCES CF_RANKS (RANK)
;

ALTER TABLE CF_USERS
ADD CONSTRAINT CF_USERS_MAX_RANK_FK
	FOREIGN KEY (MAX_RANK)
	REFERENCES CF_RANKS (RANK)
;

ALTER TABLE CF_USERS
DROP CONSTRAINT CF_USERS_RANK_FK;

ALTER TABLE CF_USERS
DROP CONSTRAINT CF_USERS_MAX_RANK_FK;


SELECT * FROM CF_USERS;

DELETE FROM CF_USERS;

INSERT INTO 
CF_USERS (CF_HANDLE)
VALUES ('tourist');

