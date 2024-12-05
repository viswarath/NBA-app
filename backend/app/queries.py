from app.database import PgDatabase


def get_player_by_name(name: str) -> dict:
    with PgDatabase() as db:
        query = """
            SELECT player_id, team_id, name, age, position, games_started
            FROM player
            WHERE name ILIKE %s;
        """

        db.cursor.execute(query, (name + '%',))
        result = db.cursor.fetchall()
        
        if result:
            players_info = [
                {
                    "player_id": row[0],
                    "team_id": row[1],
                    "name": row[2],
                    "age": row[3],
                    "position": row[4],
                    "games_started": row[5],
                }
                for row in result
            ]
            return players_info
        else:
            return None
        
        

def get_all_players() -> dict:
    with PgDatabase() as db:
        query = """
            SELECT player_id, team_id, name, age, position, games_started
            FROM player;
        """

        db.cursor.execute(query)
        result = db.cursor.fetchall()
        
        if result:
            players_info = [
                {
                    "player_id": row[0],
                    "team_id": row[1],
                    "name": row[2],
                    "age": row[3],
                    "position": row[4],
                    "games_started": row[5],
                }
                for row in result
            ]
            return players_info
        else:
            return None
        