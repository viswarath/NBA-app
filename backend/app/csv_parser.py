import csv
from app.database import PgDatabase

csv_file_path = "stats.csv"
import os

def insert_player_data_from_csv():
    count = 0
    with PgDatabase() as db:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            # Iterate through each row (player data) in the CSV
            for row in reader:
                print(count)
                # Extract player data from the row
                player_id = count
                name = row['Player']
                position = row['Pos']
                age = int(row['Age'])
                team_id = row['Tm']
                games_started = int(row['GS'])

                # Stats data
                games_played = int(row['G'])
                minutes_played = float(row['MP'])
                FG = float(row['FG'])
                FGA = float(row['FGA'])
                FG_percentage = float(row['FG%'])
                three_point_made = float(row['3P'])
                three_point_attempts = float(row['3PA'])
                three_point_percentage = float(row['3P%'])
                two_point_made = float(row['2P'])
                two_point_attempts = float(row['2PA'])
                two_point_percentage = float(row['2P%'])
                eFG_percentage = float(row['eFG%'])
                FT = float(row['FT'])
                FTA = float(row['FTA'])
                FT_percentage = float(row['FT%'])
                ORB = float(row['ORB'])
                DRB = float(row['DRB'])
                TRB = float(row['TRB'])
                AST = float(row['AST'])
                STL = float(row['STL'])
                BLK = float(row['BLK'])
                TOV = float(row['TOV'])
                PF = float(row['PF'])
                points = float(row['PTS'])
                
                count += 1
                # Insert the team if not exists (simplified logic, add your own conflict handling)
                db.cursor.execute("""
                    INSERT INTO team (team_id, div_name, div_place, conf_name, conf_place) 
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (team_id) DO NOTHING
                """, (team_id, 'Atlantic', 1, 'Eastern', 1))

                # Insert player data
                db.cursor.execute("""
                    INSERT INTO player (player_id, team_id, name, age, position, games_started) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (player_id, team_id, name, age, position, games_started))

                # Insert Free Throw Stats
                db.cursor.execute("""
                    INSERT INTO free_throw_stats (free_throw_stats_id, FTA, FT, FT_Perc) 
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (free_throw_stats_id) DO NOTHING
                """, (player_id, FTA, FT, FT_percentage))

                # Insert Shoot Stats
                db.cursor.execute("""
                    INSERT INTO shoot_stats (shoot_stats_id, FG, FGA, FG_Perc, three_point, three_point_attempted, 
                    three_point_perctange, two_point, two_point_attempted, two_point_percentage, eFG_Perc) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (shoot_stats_id) DO NOTHING
                """, (player_id, FG, FGA, FG_percentage, three_point_made, three_point_attempts, 
                    three_point_percentage, two_point_made, two_point_attempts, two_point_percentage, eFG_percentage))


                # Insert Other Stats
                db.cursor.execute("""
                    INSERT INTO other_stats (other_stats_id, ORB, DRB, TRB, AST, STL, BLK, TOV, PF) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (other_stats_id) DO NOTHING
                """, (player_id, ORB, DRB, TRB, AST, STL, BLK, TOV, PF))

                # Insert Player Stats
                db.cursor.execute("""
                    INSERT INTO player_stats (player_id, games_played, mins_played, free_throw_stats_id, shoot_stats_id, other_stats_id) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (player_id) DO NOTHING
                """, (player_id, games_played, minutes_played, player_id, player_id, player_id))

        # Commit the changes to the database
        db.connection.commit()
        print("Player data inserted successfully.")