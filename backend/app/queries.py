from app.database import PgDatabase


def get_player_by_name(name: str) -> dict:
    with PgDatabase() as db:
        query = f"""
        SELECT player_id, team_id, name, age, position, games_started
        FROM player
        where player_id = {name};
        """
        
        db.cursor.execute(query)
        result = db.cursor.fetchall()  
        
        if result:
            player_info = {
                "player_id": result[0][0],
                "team_id": result[0][1],
                "name": result[0][2],
                "age": result[0][3],
                "position": result[0][4],
                "games_started": result[0][5],
            }
            return player_info
        else:
            return None
