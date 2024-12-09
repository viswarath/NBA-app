import os
from pathlib import Path
import dotenv
from abc import ABC, abstractmethod # new
import psycopg2



BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR / ".env")

class Database(ABC):
    """
    Database context manager
    """

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()
        
        
class PgDatabase(Database):
    """PostgreSQL Database context manager"""

    def __init__(self) -> None:
        self.driver = psycopg2
        super().__init__(self.driver)

    def connect_to_database(self):
        return self.driver.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        
# Table name variables
player = "player"
team = "team"
award = "award"
player_stats = "player_stats"
team_stats = "team_stats"
free_throw_stats = "free_throw_stats"
shoot_stats = "shoot_stats"
other_stats = "other_stats"
movement = "movement"
schedule_strength = "schedule_strength"
record = "record"
rating = "rating"
arena = "arena"
plays_at = "plays_at"
games = "games"
trades = "trades"



# Drop Tables Function
def drop_tables():
    with PgDatabase() as db:
        db.cursor.execute(f"DROP TABLE IF EXISTS {games} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {plays_at} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {arena} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {rating} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {record} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {schedule_strength} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {movement} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {other_stats} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {shoot_stats} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {free_throw_stats} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {team_stats} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {player_stats} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {award} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {player} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {team} CASCADE;")
        db.cursor.execute(f"DROP TABLE IF EXISTS {trades} CASCADE;")       
           
        db.connection.commit()
        print("Tables are dropped...")

def create_tables():
    with PgDatabase() as db:
        
        # Create Team table
        db.cursor.execute(f"""
            CREATE TABLE {team} (
                team_id CHAR(3) PRIMARY KEY,
                name VARCHAR(255),
                rank INT,
                wins INT,
                losses INT
            );
        """)
        
        # Create Other_Stats table
        db.cursor.execute(f"""
            CREATE TABLE {other_stats} (
                other_stats_id INT PRIMARY KEY,
                ORB INT,
                DRB INT,
                TRB INT,
                AST INT,
                STL INT,
                BLK INT,
                TOV INT,
                PF INT
            );
        """)
        
        # Create Shoot_Stats table
        db.cursor.execute(f"""
            CREATE TABLE {shoot_stats} (
                shoot_stats_id INT PRIMARY KEY,
                FG INT,
                FGA INT,
                FG_Perc DECIMAL(5,2),
                three_point INT,
                three_point_attempted INT,
                three_point_perctange DECIMAL(5,2),
                two_point INT,
                two_point_attempted INT,
                two_point_percentage DECIMAL(5,2),
                eFG_Perc DECIMAL(5,2)
            );
        """)
        
        # Create Free_Throw_Stats table
        db.cursor.execute(f"""
            CREATE TABLE {free_throw_stats} (
                free_throw_stats_id INT PRIMARY KEY,
                FTA INT,
                FT INT,
                FT_Perc DECIMAL(5, 3)
            );
        """)

        # Create Player table
        db.cursor.execute(f"""
            CREATE TABLE {player} (
                player_id INT PRIMARY KEY,
                team_id CHAR(3), 
                name VARCHAR(255),
                age INT,
                position VARCHAR(255),
                games_started INT,
                FOREIGN KEY (team_id) REFERENCES {team}(team_id)
            );
        """)

        # Create Award table
        db.cursor.execute(f"""
            CREATE TABLE {award} (
                name VARCHAR(255) PRIMARY KEY,
                player_id INT,
                FOREIGN KEY (player_id) REFERENCES {player}(player_id)
            );
        """)

        # Create Movement table
        db.cursor.execute(f"""
            CREATE TABLE {movement} (
                movement_id INT PRIMARY KEY,
                team_id CHAR(3),
                pace DECIMAL(5,2),
                age DECIMAL(5,2),
                FOREIGN KEY (team_id) REFERENCES {team}(team_id)
            );
        """)

        # Create Schedule_Strength table
        db.cursor.execute(f"""
            CREATE TABLE {schedule_strength} (
                strength_id INT PRIMARY KEY,
                team_id CHAR(3),
                SOS DECIMAL(5,2),
                SRS DECIMAL(5,2),
                FOREIGN KEY (team_id) REFERENCES {team}(team_id)
            );
        """)

        # Create Record table
        db.cursor.execute(f"""
            CREATE TABLE {record} (
                record_id INT PRIMARY KEY,
                team_id CHAR(3),
                wins INT,
                losses INT,
                margin_of_victory DECIMAL(5,2),
                PW INT,
                PL INT,
                FOREIGN KEY (team_id) REFERENCES {team}(team_id)
            );
        """)

        # Create Rating table
        db.cursor.execute(f"""
            CREATE TABLE {rating} (
                rating_id INT PRIMARY KEY,
                team_id CHAR(3),
                ORTG DECIMAL(5,2), 
                DRTg DECIMAL(5,2),
                NRTg DECIMAL(5,2),
                FOREIGN KEY (team_id) REFERENCES {team}(team_id)
            );
        """)

        # Create Arena table
        db.cursor.execute(f"""
            CREATE TABLE {arena} (
                arena_name VARCHAR(255) PRIMARY KEY,
                arena_attend INT,
                arena_attend_game INT
            );
        """)

        # Create Plays_At table
        db.cursor.execute(f"""
            CREATE TABLE {plays_at} (
                arena_name VARCHAR(255),
                team_id CHAR(3),
                PRIMARY KEY (arena_name, team_id),
                FOREIGN KEY (arena_name) REFERENCES {arena}(arena_name),
                FOREIGN KEY (team_id) REFERENCES {team}(team_id)
            );
        """)

        # Create Games table
        db.cursor.execute(f"""
            CREATE TABLE {games} (
                home_team_id CHAR(3),
                away_team_id CHAR(3),
                game_id INT,
                game_date DATE,
                link VARCHAR(255),
                PRIMARY KEY (home_team_id, away_team_id, game_id),
                FOREIGN KEY (home_team_id) REFERENCES {team}(team_id),
                FOREIGN KEY (away_team_id) REFERENCES {team}(team_id)
            );
        """)
        
        
        # Create Player_Stats table
        db.cursor.execute(f"""
            CREATE TABLE player_stats (
                player_id INT PRIMARY KEY,
                games_played INT,
                mins_played INT,
                free_throw_stats_id INT,
                shoot_stats_id INT,
                other_stats_id INT,
                FOREIGN KEY (player_id) REFERENCES {player}(player_id) ON DELETE CASCADE,
                FOREIGN KEY (free_throw_stats_id) REFERENCES {free_throw_stats}(free_throw_stats_id) ON DELETE CASCADE,
                FOREIGN KEY (shoot_stats_id) REFERENCES {shoot_stats}(shoot_stats_id) ON DELETE CASCADE,
                FOREIGN KEY (other_stats_id) REFERENCES {other_stats}(other_stats_id) ON DELETE CASCADE
            );
        """)

        # Create Team_Stats table
        db.cursor.execute(f"""
            CREATE TABLE {team_stats} (
                team_id CHAR(3) PRIMARY KEY,
                games_played INT,
                movement_id INT,
                strength_id INT,
                record_id INT,
                rating_id INT,
                FOREIGN KEY (team_id) REFERENCES {team}(team_id),
                FOREIGN KEY (movement_id) REFERENCES {movement}(movement_id),
                FOREIGN KEY (strength_id) REFERENCES {schedule_strength}(strength_id),
                FOREIGN KEY (record_id) REFERENCES {record}(record_id),
                FOREIGN KEY (rating_id) REFERENCES {rating}(rating_id)
            );
        """)

        # Create Trades table
        db.cursor.execute(f"""
            CREATE TABLE {trades} (
                trade_id SERIAL PRIMARY KEY,
                player1_id INT,
                new_team1_id CHAR(3),
                player2_id INT,
                new_team2_id CHAR(3),
                trade_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        db.cursor.execute(f"""
            CREATE INDEX idx_player_name ON player(name);
        """)

        db.cursor.execute(f"""
            CREATE INDEX idx_team_name ON team(name);
        """)

        db.cursor.execute(f"""
            CREATE INDEX idx_games_game_date ON games(game_date);

        """)
        db.connection.commit()
        print("Tables are created successfully...")
