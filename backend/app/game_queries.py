from app.database import PgDatabase

def get_game_by_team_id(team_id: str) -> dict:
    with PgDatabase() as db:
        query = """
            SELECT home_team_id, away_team_id, game_id, game_date, link
            FROM games
            WHERE home_team_id ILIKE %s OR away_team_id ILIKE %s;
        """

        db.cursor.execute(query, (team_id + '%', team_id + '%',))
        result = db.cursor.fetchall()
        
        if result:
            game_info = [
                {
                    "home_team_id": row[0],
                    "away_team_id": row[1],
                    "game_id": row[2],
                    "game_date": row[3],
                    "link": row[4],
                }
                for row in result
            ]
            return game_info
        else:
            return None

def get_all_games() -> dict:
    with PgDatabase() as db:
        query = """
            SELECT home_team_id, away_team_id, game_id, game_date, link
            FROM games;
        """

        db.cursor.execute(query)
        result = db.cursor.fetchall()
        
        if result:
            game_info = [
                {
                    "home_team_id": row[0],
                    "away_team_id": row[1],
                    "game_id": row[2],
                    "game_date": row[3],
                    "link": row[4],
                }
                for row in result
            ]
            return game_info
        else:
            return None