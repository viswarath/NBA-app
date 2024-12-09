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

def get_players_by_points(points: int) -> dict:
    with PgDatabase() as db:
        query = """
            SELECT player.player_id, team_id, name, age, position, games_started, (two_point*2 + three_point*3) AS total_points
            FROM player
            INNER JOIN player_stats ON player.player_id = player_stats.player_id 
            INNER JOIN shoot_stats ON player_stats.shoot_stats_id = shoot_stats.shoot_stats_id
            WHERE (shoot_stats.three_point*3 + shoot_stats.two_point*2) > %s;
        """
        db.cursor.execute(query, (points,))
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
                    "total_points": row[6],
                }
                for row in result
            ]
            return players_info
        else:
            return None

def get_players_by_assists(assists: int) -> dict:
    with PgDatabase() as db:
        query = """
            SELECT player.player_id, team_id, name, age, position, games_started, AST as assists
            FROM player
            INNER JOIN player_stats ON player.player_id = player_stats.player_id 
            INNER JOIN other_stats ON player_stats.other_stats_id = other_stats.other_stats_id
            WHERE AST > %s;
        """
        db.cursor.execute(query, (assists,))
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
                    "AST": row[6],
                }
                for row in result
            ]
            return players_info
        else:
            return None

def get_players_by_FTPerc(FTPerc: float) -> dict:
    with PgDatabase() as db:
        query = """
            SELECT player.player_id, team_id, name, age, position, games_started, FT_Perc
            FROM player
            INNER JOIN player_stats ON player.player_id = player_stats.player_id 
            INNER JOIN free_throw_stats ON player_stats.free_throw_stats_id = free_throw_stats.free_throw_stats_id
            WHERE FT_Perc > %s;
        """
        db.cursor.execute(query, (FTPerc,))
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
                    "FT_Perc": row[6],
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

# insertion of player

def insert_player_row(team_id:str, name: str, age: int, position: str, games_started: int) -> dict:
    with PgDatabase() as db:
        try:
            # Begin the transaction
            db.cursor.execute("BEGIN;")

            # Fetch the maximum player_id
            # COALESCE is -1 if table is empty
            max_id_query = "SELECT COALESCE(MAX(player_id), -1) FROM player;"
            db.cursor.execute(max_id_query)
            result = db.cursor.fetchone()

            if result is None or len(result) == 0:
                raise Exception("Failed to fetch the maximum player_id.")
            
            max_player_id = result[0]

            # Assign the new player_id as max_player_id + 1
            player_id = max_player_id + 1

            # Insert the new player into the player table
            insert_query = """
                INSERT INTO player (player_id, team_id, name, age, position, games_started)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            db.cursor.execute(insert_query, (player_id, team_id, name, age, position, games_started))

            # fetch the same player through a query to confirm it
            select_player_query = """
                SELECT * 
                FROM player
                WHERE player_id = %s;
            """
            db.cursor.execute(select_player_query, (player_id,))
            result = db.cursor.fetchall()

            db.cursor.execute("COMMIT;")

            if result:
                insert_player_info = [
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
                return insert_player_info
            else:
                return None

        except Exception as e:
            db.cursor.execute("ROLLBACK;")
            raise Exception(f"Error inserting player: {e}")

# insertion of player

def update_player_row(player_id:int, team_id:str, name: str, age: int, position: str, games_started: int) -> dict:
    with PgDatabase() as db:
        try:
            # Begin the transaction
            db.cursor.execute("BEGIN;")

            # Insert the new player into the player table
            update_player_query = """
                UPDATE player
                SET team_id = %s, name = %s, age = %s, position = %s, games_started = %s
                WHERE player_id = %s;
            """
            db.cursor.execute(update_player_query, (team_id, name, age, position, games_started, player_id,))

            # fetch the same player through a query to confirm it
            select_player_query = """
                SELECT * 
                FROM player
                WHERE player_id = %s;
            """
            db.cursor.execute(select_player_query, (player_id,))
            result = db.cursor.fetchall()

            db.cursor.execute("COMMIT;")

            if result:
                update_player_info = [
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
                return update_player_info
            else:
                return None

        except Exception as e:
            db.cursor.execute("ROLLBACK;")
            raise Exception(f"Error updating player: {e}")

# Deletion of player
def delete_player_row(player_id:int) -> dict:
    with PgDatabase() as db:
        try:
            # Begin the transaction
            db.cursor.execute("BEGIN;")

            # The delete will cascade to the statistical tables
            delete_player_query = """
                DELETE 
                FROM player
                WHERE player_id = %s;
            """
            db.cursor.execute(delete_player_query, (player_id,))

            db.cursor.execute("COMMIT;")
            return []

        except Exception as e:
            db.cursor.execute("ROLLBACK;")
            raise Exception(f"Error deleting player: {e}")
