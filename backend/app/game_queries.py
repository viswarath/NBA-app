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

def get_advanced_game_stats_by_team_id(home_team_id: str) -> dict:
    with PgDatabase() as db:
        query = """
              SELECT 
                  g.game_date,
                  ht.team_id AS home_team_id,
                  recordht.PW AS home_team_pythagorean_wins,
                  ssht.SOS AS home_team_schedule_strength,
                  ratinght.ORTG AS home_team_ORTG,
                  at.team_id AS away_team_id,
                  recordat.PW AS away_team_pythagorean_wins,
                  ssat.SOS AS away_team_schedule_strength,
                  ratingat.ORTG AS away_team_ORTG,
                  a.arena_name AS game_arena,
                  a.arena_attend_game AS arena_attendance,
                  g.link,
                  g.game_id
              FROM games g
              JOIN team ht ON g.home_team_id = ht.team_id
              JOIN team at ON g.away_team_id = at.team_id
              JOIN record recordht ON recordht.team_id = ht.team_id
              JOIN record recordat ON recordat.team_id = at.team_id
              JOIN rating ratinght ON ratinght.team_id = ht.team_id
              JOIN rating ratingat ON ratingat.team_id = at.team_id
              JOIN schedule_strength ssht ON ssht.team_id = ht.team_id
              JOIN schedule_strength ssat ON ssat.team_id = at.team_id
              JOIN plays_at pa ON ht.team_id = pa.team_id
              JOIN arena a ON pa.arena_name = a.arena_name
              WHERE (%s = '' OR ht.team_id ILIKE %s OR at.team_id ILIKE %s)
              ORDER BY g.game_date;

        """

        db.cursor.execute(query, (home_team_id + '%', home_team_id + '%', home_team_id + '%',))
        result = db.cursor.fetchall()
        
        if result:
            game_info = [
                {
                    "game_date": row[0],
                    "home_team_id": row[1],
                    "home_team_pythagorean_wins": row[2],
                    "home_team_schedule_strength": row[3],
                    "home_team_ORTG": row[4],
                    "away_team_id": row[5],
                    "away_team_pythagorean_wins": row[6],
                    "away_team_schedule_strength": row[7],
                    "away_team_ORTG": row[8],
                    "arena_name": row[9],
                    "arena_attendance": row[10],
                    "link": row[11],
                    "game_id": row[12]
                }
                for row in result
            ]
            return game_info
        else:
            return None