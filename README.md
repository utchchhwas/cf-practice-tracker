# Codeforces Practice Tracker

Made for Level-2 Term-2 Database Sessional Project created by [Utchchhwas Singha (1805100)](https://github.com/utchchhwas) and [Pritam Saha (1805102)](https://github.com/)

Under the kind supervision of **Mohammad Tawhidul Hasan Bhuiyan, Lecturer, CSE, BUET**

### Technologies Used
  **Front-end: HTML, Bootstrap, ChartJS**<br/>
  **Back-end: Flask (Python)**<br/>
  **Database: Oracle 19c**
  
 
## Get Started

### Prerequisites:
1. Install [Python](https://www.python.org/)
2. Install [Oracle 19c](https://www.oracle.com/database/technologies/)
3. Install [Git](https://git-scm.com/)

### Cloning and Setup
1. Clone the repo.

    ```
    git clone https://github.com/utchchhwas/cf-practice-tracker.git
    ```    
2. Go to the folder and install all required packages.

    ```
    cd cf-practice-tracker
    pip install -r requirements.txt
    ```
3. Log into ```sqlplus``` as ```sysdba``` and create a new user.

    ```
    CREATE USER c##cf IDENTIFIED BY cf;
    GRANT CREATE SESSION TO c##cf;
    GRANT ALL PRIVILEGES TO c##cf;
    ```
5. Log into ```c##cf``` and create the required tables. The schema and data dump are provied at ```cf-practice-tracker/sql```.
6. Now, run the application.
    ```
    python ./run.py
    ```
7. The server will be running on ```http://127.0.0.1:5000/```.

