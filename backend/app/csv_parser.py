import csv
from app.database import PgDatabase

csv_players_path = "stats.csv"
csv_teams_path = "teams.csv"
csv_schedule_path = "schedule.csv"


import csv

def insert_team_data_from_csv():
    with PgDatabase() as db:
        count = 0  # This will be used to generate unique IDs
        with open(csv_teams_path, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file) 
            
            for row in csv_reader:
                team_id = row['Team'] 
                
                # Insert into the team table
                db.cursor.execute(f"""
                    INSERT INTO team (team_id, name, rank, wins, losses)
                    VALUES (%s, %s, %s, %s, %s);
                """, (team_id, row['Name'], row['Rk'], row['W'], row['L']))


                # Insert into the movement table (e.g., based on pace and age)
                movement_id = count
                db.cursor.execute(f"""
                    INSERT INTO movement (movement_id, team_id, pace, age)
                    VALUES (%s, %s, %s, %s);
                """, (
                    movement_id,
                    team_id,
                    float(row['Pace']),
                    float(row['Age'])
                ))

                # Insert into the schedule_strength table (SOS and SRS)
                strength_id = count
                db.cursor.execute(f"""
                    INSERT INTO schedule_strength (strength_id, team_id, SOS, SRS)
                    VALUES (%s, %s, %s, %s);
                """, (
                    strength_id,
                    team_id,
                    float(row['SOS']),
                    float(row['SRS'])
                ))

                # Insert into the record table (wins, losses, margin of victory)
                record_id = count
                db.cursor.execute(f"""
                    INSERT INTO record (record_id, team_id, wins, losses, margin_of_victory, PW, PL)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (
                    record_id,
                    team_id,
                    int(row['W']),
                    int(row['L']),
                    float(row['MOV▲']),
                    int(row['PW']),
                    int(row['PL'])
                ))

                # Insert into the rating table (ORtg, DRtg, NRtg)
                rating_id = count
                db.cursor.execute(f"""
                    INSERT INTO rating (rating_id, team_id, ORTG, DRTg, NRTg)
                    VALUES (%s, %s, %s, %s, %s);
                """, (
                    rating_id,
                    team_id,
                    float(row['ORtg']),
                    float(row['DRtg']),
                    float(row['NRtg'])
                ))

                # Insert into the arena table (Arena and Attendance)
                arena_name = row['Arena']
                db.cursor.execute(f"""
                    INSERT INTO arena (arena_name, arena_attend, arena_attend_game)
                    VALUES (%s, %s, %s);
                """, (
                    arena_name,
                    int(row['Attend.']),
                    int(row['Attend./G'])
                ))

                # Insert into the plays_at table (team plays at arena)
                db.cursor.execute(f"""
                    INSERT INTO plays_at (arena_name, team_id)
                    VALUES (%s, %s);
                """, (arena_name, team_id))

                count += 1
        print("Team data inserted successfully.") 
        db.connection.commit()




def insert_game_data_from_csv():
    with PgDatabase() as db:
        with open(csv_schedule_path, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                home_team_id = row['home_team']
                away_team_id = row['away_team']
                game_id = int(row['game_id'])
                game_date = row['game_date']
                preview_url = row['preview_url']
                
                # Insert into the Games table
                db.cursor.execute("""
                    INSERT INTO Games (home_team_id, away_team_id, game_id, game_date, link)
                    VALUES (%s, %s, %s, %s, %s)
                """, (home_team_id, away_team_id, game_id, game_date, preview_url))
        
        print("Game Data inserted successfully.")
        db.connection.commit()




def insert_player_data_from_csv():
    count = 0
    with PgDatabase() as db:
        with open(csv_players_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
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

        db.connection.commit()
        print("Player data inserted successfully.")



def insert_award_data():
    awards = [
        ("Most Valuable Player (Michael Jordan Trophy)", 163),
        ("Rookie of the Year (Wilt Chamberlain Trophy)", 25),
        ("Defensive Player of the Year (Hakeem Olajuwon Trophy)", 267),
        ("Most Improved Player (George Mikan Trophy)", 349),
        ("Sixth Man of the Year (John Havlicek Trophy)", 70),
        ("Clutch Player of the Year (Jerry West Trophy)", 175),
        ("NBA Hustle Award", 510)
    ]
    
    with PgDatabase() as db:
        for award_name, player_id in awards:
            db.cursor.execute(f"""
                INSERT INTO award (name, player_id)
                VALUES (%s, %s);
            """, (award_name,player_id))
        
        print("Award data inserted successfully.")
        db.connection.commit()
