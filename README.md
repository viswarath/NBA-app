# NBA Stats App

## Overview

The **NBA Stats App** is a web application that provides detailed statistics for NBA players, teams, and games from the 2023 season. The app allows users to view data in a table format, as well as add and delete data entries for players, teams, and games.

The app is built using a **FastAPI** backend with a **PostgreSQL** database, and a **React** frontend with **TypeScript** and **Material-UI (MUI)** for styling. It is designed to run locally only, as specified in the project requirements.

---

## Tech Stack

- **Backend**:
  - **FastAPI** (for building the API)
  - **PostgreSQL** (database)
  - **SQL** (pure SQL for data management)
  - **Uvicorn** (ASGI server)

- **Frontend**:
  - **React** (UI framework)
  - **TypeScript** (for type safety)
  - **Material-UI** (MUI for design components)
  - **Yarn** (for package management)

---

## Features

- **View NBA Stats**:
  - Displays a table of NBA players, teams, and games for the 2023 season.
  - Players' statistics include points, assists, rebounds, and other key metrics.
  - Game data includes scores, date, and participating teams.
  - Teams' information includes roster and performance metrics.

- **Add and Delete Data**:
  - Users can add new NBA players, games, and teams to the database.
  - Users can also delete existing data from the database.

---

## Prerequisites

Before running the app, ensure the following tools are installed:

- **Python 3.8+** (for backend)
- **Node.js** and **Yarn** (for frontend)
- **PostgreSQL** (database server)
- **Postman** or similar tool for testing API endpoints (optional)

---

## Setup Instructions

### 1. Set up the Backend (FastAPI with PostgreSQL)

#### Step 1: Clone the repository

Clone the project from GitHub:

#### Step 2: Install proper things

##### Frontend:
- Install Yarn and node (nvm)
- run `yarn add` in the `\nba_stats`

##### Backend:
- Activate python virual environment:
```
python3 -m venv venv 
source venv/bin/activate 
```
- Run `pip install -r requirements.txt` fastapi and uvicorn

---

## Run Instructions: 

### Backend: 
To start the backend server, run the following command:
```
cd backend/
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
```
The backend will now be accessible at `http://localhost:8000`


### Frontend:
To start the frontend development server, run:

```
cd nba-stats/
yarn start
```
Open your browser (GOOGLE CHROME) and navigate to `http://localhost:3000` to access the frontend


