DROP TABLE CONTESTS;

CREATE TABLE CONTESTS (
	CONTEST_ID NUMBER,
	CONTEST_NAME VARCHAR2(255) NOT NULL,
	START_TIME DATE,
	CONSTRAINT CONTESTS_PK PRIMARY KEY (CONTEST_ID)
);

SELECT * FROM CONTESTS
ORDER BY START_TIME DESC;

SELECT COUNT(*) FROM CONTESTS;


DELETE FROM CONTESTS;

INSERT INTO
CONTESTS (CONTEST_ID, CONTEST_NAME, START_TIME)
VALUES (1630, 'Codeforces Round #768 (Div. 1)', TO_DATE('2021-12-29 21:35:00', 'YYYY-MM-DD HH24:MI:SS'));

SELECT CAST(SYSTIMESTAMP AS DATE) ts_to_date
FROM   dual;