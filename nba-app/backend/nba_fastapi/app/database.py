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
        
player = "player"

def drop_tables():
    with PgDatabase() as db:
        db.cursor.execute(f"DROP TABLE IF EXISTS {player} CASCADE;")
        db.connection.commit()
        print("Tables are dropped...")

def create_tables():
    with PgDatabase() as db:
        db.cursor.execute(f"""CREATE TABLE {player} (
                player_id INT PRIMARY KEY,
                team_id CHAR(3), 
                name VARCHAR(255),
                age INT,
                position VARCHAR(255),
                games_started INT,
                rank INT
            );
        """)
        db.connection.commit()
        print("Tables are created successfully...")


def get_player_by_name(name: str) -> dict:
    with PgDatabase() as db:
        query = f"""
        SELECT player_id, team_id, name, age, position, games_started, rank
        FROM player
        WHERE name = '{name}';
        """
        
        db.cursor.execute(query)
        result = db.cursor.fetchone()  
        
        if result:
            player_info = {
                "player_id": result[0],
                "team_id": result[1],
                "name": result[2],
                "age": result[3],
                "position": result[4],
                "games_started": result[5],
                "rank": result[6]
            }
            return player_info
        else:
            return None