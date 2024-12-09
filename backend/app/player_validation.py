
VALID_TEAM_IDS = [
  "ATL", "BOS", "BRK", "CHO", "CHI", "CLE", "DAL", "DEN", "DET", 
  "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", 
  "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", 
  "TOR", "UTA", "WAS"
]

VALID_POSITIONS = ["PF", "PG", "SG", "C", "SF"]

NUM_GAMES_SEASON = 82

def is_valid_team_id(team_id:str):
  if not isinstance(team_id, str):
    raise ValueError(f"Invalid team_id: {team_id}. Must be a string.")
  if team_id not in VALID_TEAM_IDS:
    raise ValueError(f"Invalid team_id: {team_id}. Must be one of the teams present in the NBA.")

def is_valid_player_name(name: str):
  if not isinstance(name, str):
    raise ValueError(f"Invalid games_started: {name}. Must be an string.")
  if not name or name[0].isdigit():
    raise ValueError("Invalid name. The player's name must not be NULL or start with a number.")

def is_valid_age(age: int):
  if not isinstance(age, int):
    raise ValueError(f"Invalid age: {age}. Must be an integer.")
  if age > 100 or age < 18:
    raise ValueError(f"Invalid age: {age}. Age must be between 18 and 100.")

def is_valid_position(position: str):
  if not isinstance(position, str):
    raise ValueError(f"Invalid position: {position}. Must be a string.")
  if position not in VALID_POSITIONS:
    raise ValueError(f"Invalid position: {position}. Must be one of {VALID_POSITIONS}.")

def is_valid_games_started(games_started: int):
  if not isinstance(games_started, int):
    raise ValueError(f"Invalid games_started: {games_started}. Must be an integer.")
  if games_started > 82 or games_started < 0:
    raise ValueError(f"Invalid position: {games_started}. Must be between 0 and that of the number of games in a season: {NUM_GAMES_SEASON}.")


