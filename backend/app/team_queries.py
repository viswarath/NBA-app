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