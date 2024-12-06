from app.database import PgDatabase


def get_team_by_name(name: str) -> dict:
    with PgDatabase() as db:
        query = """
            SELECT team_id, name, rank, wins, losses
            FROM team
            WHERE name ILIKE %s;
        """

        db.cursor.execute(query, (name + '%',))
        result = db.cursor.fetchall()
        
        if result:
            team_info = [
                {
                    "team_id": row[0],
                    "name": row[1],
                    "rank": row[2],
                    "wins": row[3],
                    "losses": row[4],
                }
                for row in result
            ]
            return team_info
        else:
            return None

def get_all_teams() -> dict:
    with PgDatabase() as db:
        query = """
            SELECT team_id, name, rank, wins, losses
            FROM team;
        """

        db.cursor.execute(query)
        result = db.cursor.fetchall()
        
        if result:
            team_info = [
                {
                    "team_id": row[0],
                    "name": row[1],
                    "rank": row[2],
                    "wins": row[3],
                    "losses": row[4],
                }
                for row in result
            ]
            return team_info
        else:
            return None


def get_num_team_awards() -> dict:
    with PgDatabase() as db:
        query = """
            SELECT team.team_id, team.name, rank, wins, losses, COUNT(award.name)
            FROM player
            JOIN award on player.player_id = award.player_id
            JOIN team on player.team_id = team.team_id
            GROUP BY team.team_id, team.name, rank, wins, losses;
        """

        db.cursor.execute(query)
        result = db.cursor.fetchall()
        
        if result:
            team_award_info = [
                {
                    "team_id": row[0],
                    "name": row[1],
                    "rank": row[2],
                    "wins": row[3],
                    "losses": row[4],
                    "awards": row[5],
                }
                for row in result
            ]
            return team_award_info
        else:
            return None

def get_num_road_games() -> dict:
    with PgDatabase() as db:
        query = """
            SELECT team_id, name, rank, wins, losses, COUNT(away_team_id) AS num_road_games
            FROM team, games
            WHERE team_id = away_team_id
            GROUP BY team_id, name, rank, wins, losses;
        """

        db.cursor.execute(query)
        result = db.cursor.fetchall()
        
        if result:
            road_game_info = [
                {
                    "team_id": row[0],
                    "name": row[1],
                    "rank": row[2],
                    "wins": row[3],
                    "losses": row[4],
                    "num_road_games": row[5],
                }
                for row in result
            ]
            return road_game_info
        else:
            return None