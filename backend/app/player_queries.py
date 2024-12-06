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