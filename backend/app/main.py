from fastapi import FastAPI, status, Query # type: ignore
from fastapi.exceptions import HTTPException  # type: ignore
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware # type: ignore


from app.database import create_tables, drop_tables
from app.queries import get_player_by_name, get_all_players
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