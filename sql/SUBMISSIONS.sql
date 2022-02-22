
DROP TABLE SUBMISSIONS;

CREATE TABLE SUBMISSIONS (
	SUBMISSION_ID NUMBER,
	CF_HANDLE VARCHAR2(255),
	CONTEST_ID NUMBER,
	PROBLEM_INDEX VARCHAR2(10),
	CREATION_TIME DATE,
	PROGRAMMING_LANG VARCHAR2(255),
	VERDICT VARCHAR2(255)
);

ALTER TABLE SUBMISSIONS
ADD	CONSTRAINT SUBMISSIONS_PK
	PRIMARY KEY (SUBMISSION_ID)

ALTER TABLE SUBMISSIONS
ADD CONSTRAINT SUBMISSIONS_CF_HANDLE_FK
	FOREIGN KEY (CF_HANDLE)
	REFERENCES CF_USERS (CF_HANDLE)
;

ALTER TABLE SUBMISSIONS
DROP CONSTRAINT SUBMISSIONS_CF_HANDLE_FK
;

ALTER TABLE SUBMISSIONS
ADD CONSTRAINT SUBMISSIONS_PROBLEM_ID_FK
	FOREIGN KEY (CONTEST_ID, PROBLEM_INDEX)
	REFERENCES PROBLEMS (CONTEST_ID, PROBLEM_INDEX)
;

ALTER TABLE SUBMISSIONS
DROP CONSTRAINT SUBMISSIONS_FK
;


DELETE FROM SUBMISSIONS;

SELECT * FROM SUBMISSIONS;

SELECT 
	CONTEST_ID, 
	PROBLEM_INDEX,
	PROBLEM_RATING
FROM 
	PROBLEMS
	INNER JOIN SUBMISSIONS
	USING (CONTEST_ID, PROBLEM_INDEX)
WHERE
	CF_HANDLE = 'utchchhwas'
	AND VERDICT = 'OK'
	AND PROBLEM_RATING = 2100
GROUP BY
	CONTEST_ID, 
	PROBLEM_INDEX,
	PROBLEM_RATING
ORDER BY
	CONTEST_ID, 
	PROBLEM_INDEX
;



SELECT
	PROBLEM_RATING, COUNT(*)
FROM
	( 
		SELECT 
			DISTINCT PROBLEM_RATING 
		FROM 
			PROBLEMS 
		WHERE 
			PROBLEM_RATING IS NOT NULL 
	) 
	LEFT JOIN 
	(
		SELECT
			CONTEST_ID,
			PROBLEM_INDEX,
			PROBLEM_RATING 
		FROM
			PROBLEMS
			INNER JOIN 
			SUBMISSIONS 
			USING (CONTEST_ID, PROBLEM_INDEX) 
		WHERE
			CF_HANDLE = 'utchchhwas' 
			AND VERDICT = 'OK' 
		GROUP BY
			CONTEST_ID,
			PROBLEM_INDEX,
			PROBLEM_RATING 
	) 
	USING (PROBLEM_RATING)
GROUP BY
	PROBLEM_RATING
;

SELECT
	DISTINCT P1.PROBLEM_RATING
FROM 
	PROBLEMS P1
WHERE
	P1.PROBLEM_RATING IS NOT NULL
ORDER BY
	P1.PROBLEM_RATING
;

SELECT 
	*
FROM 
	PROBLEMS
	INNER JOIN SUBMISSIONS
	USING (CONTEST_ID, PROBLEM_INDEX)
WHERE
	PROBLEM_RATING = 800
	AND CF_HANDLE = 'utchchhwas'
	AND VERDICT = 'OK'
ORDEr BY

;

SELECT
	R.PROBLEM_RATING,
	(
	SELECT
		COUNT(*)
	FROM
		(
			SELECT 
				CONTEST_ID,
				PROBLEM_INDEX
			FROM 
				PROBLEMS
				INNER JOIN SUBMISSIONS
				USING (CONTEST_ID, PROBLEM_INDEX)
			WHERE
				PROBLEM_RATING = R.PROBLEM_RATING
				AND CF_HANDLE = 'utchchhwas'
				AND VERDICT = 'OK'
			GROUP BY
				CONTEST_ID,
				PROBLEM_INDEX
		)
	)	NUM
FROM
	( 
		SELECT 
			DISTINCT PROBLEM_RATING 
		FROM 
			PROBLEMS 
		WHERE 
			PROBLEM_RATING IS NOT NULL 
	) R
ORDER BY
	R.PROBLEM_RATING ASC
;

SELECT
	I.PROBLEM_INDEX,
	(
	SELECT
		COUNT(*)
	FROM
		(
			SELECT 
				CONTEST_ID,
				PROBLEM_INDEX
			FROM 
				PROBLEMS
				INNER JOIN SUBMISSIONS
				USING (CONTEST_ID, PROBLEM_INDEX)
			WHERE
				PROBLEM_INDEX = I.PROBLEM_INDEX
				AND CF_HANDLE = 'utchchhwas'
				AND VERDICT = 'OK'
			GROUP BY
				CONTEST_ID,
				PROBLEM_INDEX
		)
	)	NUM
FROM
	( 
		SELECT 
			DISTINCT PROBLEM_INDEX 
		FROM 
			PROBLEMS 
		WHERE 
			PROBLEM_INDEX IS NOT NULL 
	) I
ORDER BY
	I.PROBLEM_INDEX ASC
;


SELECT 
	DISTINCT PROBLEM_INDEX 
FROM 
	PROBLEMS 
ORDER BY PROBLEM_INDEX
;

SELECT DISTINCT CONTEST_ID, PROBLEM_INDEX
FROM SUBMISSIONS
WHERE CF_HANDLE = 'utchchhwas'
;

SELECT	
	DISTINCT S.CONTEST_ID,
	S.PROBLEM_INDEX
FROM 
	SUBMISSIONS S
WHERE
	CF_HANDLE = 'utchchhwas'
	AND EXISTS (
		SELECT
			P.CONTEST_ID, P.PROBLEM_INDEX
		FROM
			PROBLEMS P
		WHERE
			P.CONTEST_ID = S.CONTEST_ID
			AND P.PROBLEM_INDEX = S.PROBLEM_INDEX
	)
;

SELECT
	COUNT(*)
FROM
	(
	SELECT	
		DISTINCT S.CONTEST_ID,
		S.PROBLEM_INDEX
	FROM 
		SUBMISSIONS S
	WHERE
		S.CF_HANDLE = 'utchchhwas'
		AND EXISTS (
			SELECT
				P.CONTEST_ID, P.PROBLEM_INDEX
			FROM
				PROBLEMS P
			WHERE
				P.CONTEST_ID = S.CONTEST_ID
				AND P.PROBLEM_INDEX = S.PROBLEM_INDEX
		)
	)
;

SELECT
	COUNT(*)
FROM
	(
	SELECT	
		DISTINCT S.CONTEST_ID,
		S.PROBLEM_INDEX
	FROM 
		SUBMISSIONS S
	WHERE
		CF_HANDLE = 'utchchhwas'
		AND EXISTS (
			SELECT
				P.CONTEST_ID, P.PROBLEM_INDEX
			FROM
				PROBLEMS P
			WHERE
				P.CONTEST_ID = S.CONTEST_ID
				AND P.PROBLEM_INDEX = S.PROBLEM_INDEX
		)
	)
;


SELECT
	SYSDATE,
	SYSDATE-1
FROM DUAL
;



SELECT
	DISTINCT CONTEST_ID, PROBLEM_INDEX, CREATION_TIME
FROM
	SUBMISSIONS
WHERE
		CF_HANDLE = 'utchchhwas'
		AND VERDICT = 'OK'
		AND CREATION_TIME >= SYSDATE-30
ORDER BY
	CREATION_TIME
;

SELECT
	COUNT(*) NUM
FROM
(
	SELECT
		DISTINCT CONTEST_ID, PROBLEM_INDEX
	FROM
		SUBMISSIONS
	WHERE
		CF_HANDLE = 'utchchhwas'
		AND VERDICT = 'OK'
		AND CREATION_TIME >= SYSDATE-30
		AND (CONTEST_ID, PROBLEM_INDEX)  NOT IN (
			SELECT
				DISTINCT CONTEST_ID, PROBLEM_INDEX
			FROM
				SUBMISSIONS
			WHERE
				CF_HANDLE = 'utchchhwas'
				AND VERDICT = 'OK'
				AND CREATION_TIME < SYSDATE-30
		)
)
;

