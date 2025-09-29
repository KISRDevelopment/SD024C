# SD024C — Arabic Reading & Spelling Diagnosis Tool (Django)

An internal web application for administering Arabic literacy assessments (primary & secondary levels).

> **Status:** Ongoing (Aug 2025)

---

## Overview

SD024C digitizes a standardized Arabic reading & spelling assessment. Each subtest has a **Training** phase (gate/eligibility) and a **Main Test** phase.

Representative subtests implemented/in progress: 
2-step practice flow (`question → immediate feedback`) then gated access to main test. Non-responses recorded.

* **Primary Test 1 — Word Reading: Accuracy & Speed**
  Training (3 items) → Main test (per‑word accuracy, timer for speed/fluency).
* **Primary Test 2 — Sentence Reading Fluency**
  Training (3 items) → Per‑word toggling, global timer with fluency formula, total score display.
* **Primary Test 3 — Reading Comprehension Fluency**
  Training (3 items) → Main test (if 3 minutes is up, test is over).
* **Primary Test 4 — Word Spelling**
  Main test (teacher records).
* **Primary Test 5 — Spelling Choice**
  Training (3 items) → Main test (if 1 minutes is up, test is over).
* **Primary Test 6 — Reading Comprehension**
  Training (2 items) → Main test (if 3 minutes is up, test is over).
  
* **Secondary Test 1 — Word Reading: Accuracy**
  Training (3 items) → Main test (per‑word accuracy, timer for speed/fluency).
* **Secondary Test 2 — Reading Comprehension Fluency**
  Training (3 items) → Main test (if 3 minutes is up, test is over).
* **Secondary Test 3 — Word Spelling**
  Main test (student writes their answer, and it will be automated corrected once submit).
* **Secondary Test 4 — Reading Comprehension**
  Training (2 items) → Main test (if 3 minutes is up, test is over).
  
  




## Tech Stack

* **Backend:** Django 5.2.3 (python 3.13)
* **DB:** SQLite for local dev
* **Frontend:** Bootstrap 5
*  **Note:** Please make sure you have the latest python version.


## Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:KISRDevelopment/SD024C.git
cd SD024C
```

### 2. Create & activate a virtual environment

```bash
python3 -m venv .venv
# On Mac
source .venv/bin/activate   
# On Windows: 
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```



### 4. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

Follow the prompts for username, email, and password.

### 6. Run the development server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to access the app.
```

##Once on the website:
1. Go to **Login** and sign in using the admin credentials you created.
2. As admin, click **Create Examiner** and fill in their details.
3. Log out, log back in as the examiner.
4. Create student details and access the tests.



---



