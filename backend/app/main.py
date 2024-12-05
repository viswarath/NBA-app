from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException 
from typing import List, Optional


from app.database import create_tables, drop_tables
from app.queries import get_player_by_name
from app.csv_parser import insert_player_data_from_csv, insert_team_data_from_csv, insert_game_data_from_csv, insert_award_data
app = FastAPI()


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

@app.get('/players/{name}', response_model=List[dict])
async def get_player(name: str) -> List[dict]:
    try:
        # Call the function to fetch players by name from the database
        player_info = get_player_by_name(name)
                
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
            detail=f"Error {e}"
        )