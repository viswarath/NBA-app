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

def get_teams_by_SOS(SOS: float) -> dict:
    with PgDatabase() as db:
        query = """
            SELECT team.team_id, name, rank, wins, losses, SOS
            FROM team
            JOIN schedule_strength ON team.team_id = schedule_strength.team_id
            WHERE SOS > %s;
        """

        db.cursor.execute(query, (SOS,))
        result = db.cursor.fetchall()
        
        if result:
            team_info = [
                {
                    "team_id": row[0],
                    "name": row[1],
                    "rank": row[2],
                    "wins": row[3],
                    "losses": row[4],
                    "SOS": row[5],
                }
                for row in result
            ]
            return team_info
        else:
            return None

def trade_transaction(player1_id: int, player2_id: int) -> dict:
    with PgDatabase() as db:
        try:
            # Begin the transaction
            db.cursor.execute("BEGIN;")
            
            # Get the current team IDs of both players
            query_get_teams = """
                SELECT team_id 
                FROM player 
                WHERE player_id = %s;
            """
            db.cursor.execute(query_get_teams, (player1_id,))
            team1_id = db.cursor.fetchone()[0]  # Team ID for player 1

            db.cursor.execute(query_get_teams, (player2_id,))
            team2_id = db.cursor.fetchone()[0]  # Team ID for player 2

            # Update player 1's team to player 2's team
            query_update_player1 = """
                UPDATE player
                SET team_id = %s
                WHERE player_id = %s;
            """
            db.cursor.execute(query_update_player1, (team2_id, player1_id))

            # Update player 2's team to player 1's team
            query_update_player2 = """
                UPDATE player
                SET team_id = %s
                WHERE player_id = %s;
            """
            db.cursor.execute(query_update_player2, (team1_id, player2_id))

            # Insert trade details into the trades table
            query_insert_trade = """
                INSERT INTO trades (player1_id, new_team1_id, player2_id, new_team2_id)
                VALUES (%s, %s, %s, %s);
            """
            db.cursor.execute(
                query_insert_trade,
                (player1_id, team2_id, player2_id, team1_id)
            )

            query_read_trade = """
                SELECT * 
                FROM trades
                WHERE player1_id = %s AND player2_id = %s
                ORDER BY trade_id DESC
                LIMIT 1;
            """
            db.cursor.execute(query_read_trade, (player1_id, player2_id))
            result = db.cursor.fetchall()

            # Commit the transaction
            db.cursor.execute("COMMIT;")

            if result:
              trade_info = [
                {
                    "trade_id": row[0],
                    "player1_id": row[1],
                    "new_team1_id": row[2],
                    "player2_id": row[3],
                    "new_team2_id": row[4],
                    "trade_date": row[5],
                }
                for row in result
              ]
              return trade_info
            else:
              return None

        except Exception as e:
            # Rollback transaction in case of error
            db.cursor.execute("ROLLBACK;")
            raise e



def get_all_trades():
  with PgDatabase() as db:
          query_read_trade = """
                SELECT * 
                FROM trades;
            """
          db.cursor.execute(query_read_trade)
          result = db.cursor.fetchall()

          
          if result:
              trade_info = [
                {
                    "trade_id": row[0],
                    "player1_id": row[1],
                    "new_team1_id": row[2],
                    "player2_id": row[3],
                    "new_team2_id": row[4],
                    "trade_date": row[5],
                }
                for row in result
              ]
              return trade_info
          else:
              return []