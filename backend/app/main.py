from fastapi import FastAPI, status, Query, Request # type: ignore
from fastapi.exceptions import HTTPException  # type: ignore
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware # type: ignore


from app.database import create_tables, drop_tables
from app.player_queries import get_player_by_name, get_all_players, get_players_by_points, get_players_by_assists, get_players_by_FTPerc, insert_player_row, update_player_row, delete_player_row
from app.team_queries import get_team_by_name, get_all_teams, get_num_team_awards, get_num_road_games, get_teams_by_SOS, trade_transaction, get_all_trades
from app.game_queries import get_game_by_team_id, get_all_games, get_advanced_game_stats_by_team_id
from app.csv_parser import insert_player_data_from_csv, insert_team_data_from_csv, insert_game_data_from_csv, insert_award_data
from app.player_validation import is_valid_team_id, is_valid_age, is_valid_position, is_valid_games_started, is_valid_player_name
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
async def get_players_points(points: Optional[int] = Query(0, alias="points")) -> List[dict]:
    try:
        
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

@app.get('/playerAssists', response_model=List[dict])
async def get_players_points(assists: Optional[int] = Query(0, alias="assists")) -> List[dict]:
    try:
        player_info = get_players_by_assists(assists)  # Function to fetch a player by points
        
        if player_info:
            return player_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Players with listed assists not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )

@app.get('/playerFTPerc', response_model=List[dict])
async def get_players_FTPerc(FTPerc: Optional[float] = Query(0, alias="FTPerc")) -> List[dict]:
    try:
        player_info = get_players_by_FTPerc(FTPerc)  # Function to fetch a player by points
                
        if player_info:
            return player_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Players with listed FT percentage not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )

# Player insertion
@app.post('/insertPlayer', response_model=List[dict])
async def insert_player(request: Request):
    try:
        # Parse the request body as JSON
        body = await request.json()

        # Extract player info
        team_id = body.get("team_id")
        name = body.get("name")
        age = body.get("age")
        position = body.get("position")
        games_started = body.get("games_started")

        # Validate fields
        try:
            is_valid_team_id(team_id)
            is_valid_player_name(name)
            is_valid_age(age)
            is_valid_position(position)
            is_valid_games_started(games_started)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        insert_info = insert_player_row(team_id, name, age, position, games_started)

        if insert_info:
            return insert_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="player insertion info not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )

# Player update
@app.put('/updatePlayer', response_model=List[dict])
async def update_player(request: Request):
    try:
        body = await request.json()

        player_id = body.get("player_id")
        team_id = body.get("team_id")
        name = body.get("name")
        age = body.get("age")
        position = body.get("position")
        games_started = body.get("games_started")

        # Validate fields
        try:
            is_valid_team_id(team_id)
            is_valid_player_name(name)
            is_valid_age(age)
            is_valid_position(position)
            is_valid_games_started(games_started)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        update_player_info = update_player_row(player_id, team_id, name, age, position, games_started)

        if update_player_info:
            return update_player_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="player update info not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )

# Player deletion
@app.delete('/deletePlayer', response_model=List[dict])
async def update_player(request: Request):
    try:
        # Parse the request body as JSON
        body = await request.json()

        # Extract player_id
        player_id = body.get("player_id")

        delete_player_info = delete_player_row(player_id)

        if not delete_player_info:
            return delete_player_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="player deletion failed"
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

@app.get('/teamSOS', response_model=List[dict])
async def get_teamSOS(SOS: Optional[float] = Query(0, alias="SOS")) -> List[dict]:
    try:
        team_info = get_teams_by_SOS(SOS)
        
        if team_info:
            return team_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team SOS not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )

@app.post('/tradePlayers', response_model=List[dict])
async def trade_players(request: Request):
    try:
        # Parse the request body as JSON
        body = await request.json()

        # Extract and validate player IDs
        player1_id = body.get("player1_id")
        player2_id = body.get("player2_id")

        if not isinstance(player1_id, int) or not isinstance(player2_id, int):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both player1_id and player2_id must be valid integers."
            )

        if player1_id is None or player2_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both player1_id and player2_id must be provided."
            )

        trade_info = trade_transaction(player1_id, player2_id)

        if trade_info:
            return trade_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trade between players unable to occur"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )

@app.get('/trades')
async def get_trades() -> List[dict]:
    try:
        trade_info = get_all_trades()
        if not trade_info:
            return trade_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error in trade_info"
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
            game_info = get_game_by_team_id(team_id)
        else: 
            game_info = get_all_games()
        
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

@app.get('/advancedGameStat', response_model=List[dict])
async def get_teams(team_id: Optional[str] = Query('', alias="team_id")) -> List[dict]:
    try:
        game_info = get_advanced_game_stats_by_team_id(team_id)  # Function to fetch a team by name
        
        if game_info:
            return game_info
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game data not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}"
        )