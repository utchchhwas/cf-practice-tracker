
DROP TABLE USERS;

CREATE TABLE USERS (
	USERNAME VARCHAR2(255),
	PASSWORD VARCHAR2(255),
	CF_HANDLE VARCHAR2(255),
	IS_ADMIN CHAR(1) DEFAULT 'N'
);

ALTER TABLE USERS
ADD	CONSTRAINT USERS_PK
	PRIMARY KEY (USERNAME);
	

ALTER TABLE USERS
ADD CONSTRAINT USERS_FK
	FOREIGN KEY (CF_HANDLE)
	REFERENCES CF_USERS (CF_HANDLE);


DELETE FROM USERS;

SELECT * FROM USERS;


					
										
										
										