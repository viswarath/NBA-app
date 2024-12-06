from fastapi import FastAPI, status, Query # type: ignore
from fastapi.exceptions import HTTPException  # type: ignore
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware # type: ignore


from app.database import create_tables, drop_tables
from app.player_queries import get_player_by_name, get_all_players, get_players_by_points
from app.team_queries import get_team_by_name, get_all_teams, get_num_team_awards, get_num_road_games
from app.game_queries import get_game_by_team_id, get_all_games
from app.csv_parser import insert_player_data_from_csv, insert_team_data_from_csv, insert_game_data_from_csv, insert_award_data
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def index():
    return {'message': 'Welcome to nba app!'}



@app.post('/initdb')
async def initdb():
    try:
        drop_tables()
        print("Done")
        create_tables()
        insert_team_data_from_csv()
        insert_game_data_from_csv()
        insert_player_data_from_csv()
        insert_award_data()
        return {"message": "Tables ; and created!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error {e}"
        )

@app.get('/players', response_model=List[dict])
async def get_players(name: Optional[str] = Query(None, alias="name")) -> List[dict]:
    try:
        if name: 
            player_info = get_player_by_name(name)  # Function to fetch a player by name
        else: 
            player_info = get_all_players()  # Function to fetch all players
        
        if player_info:
            return player_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Player not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )

@app.get('/playerPoints', response_model=List[dict])
async def get_players_points(points: Optional[int] = Query(None, alias="points")) -> List[dict]:
    try:
        if points: 
            player_info = get_players_by_points(points)  # Function to fetch a player by points
        
        if player_info:
            return player_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Players with listed points not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )


# Team query routes

@app.get('/teams', response_model=List[dict])
async def get_teams(name: Optional[str] = Query(None, alias="name")) -> List[dict]:
    try:
        if name: 
            team_info = get_team_by_name(name)  # Function to fetch a team by name
        else: 
            team_info = get_all_teams()  # Function to fetch all teams
        
        if team_info:
            return team_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )

@app.get('/teamAwards')
async def get_team_award_count() -> List[dict]:
    try:
        team_award_info = get_num_team_awards()
        
        if team_award_info:
            return team_award_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team award counts not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )

# Game query routes

@app.get('/games', response_model=List[dict])
async def get_teams(team_id: Optional[str] = Query(None, alias="team_id")) -> List[dict]:
    try:
        if team_id: 
            game_info = get_game_by_team_id(team_id)  # Function to fetch a team by name
        else: 
            game_info = get_all_games()  # Function to fetch all teams
        
        if game_info:
            return game_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )

@app.get('/roadgames')
async def get_road_games() -> List[dict]:
    try:
        road_game_info = get_num_road_games()
        
        if road_game_info:
            return road_game_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )