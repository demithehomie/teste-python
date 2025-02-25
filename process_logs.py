import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool
from psycopg2.extras import execute_batch
import logging



load_dotenv()
DSN = os.getenv("DATABASE_URL")
print("DSN:", DSN)  


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabasePool:
    def __init__(self, dsn, minconn=1, maxconn=10):
        self.pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, dsn)

    def get_conn(self):
        return self.pool.getconn()

    def put_conn(self, conn):
        self.pool.putconn(conn)

    def close_all(self):
        self.pool.closeall()

def process_logs(logs, db_pool):
    conn = db_pool.get_conn()
    try:
        with conn:
            with conn.cursor() as cursor:
                log_data = [(log['timestamp'], log['level'], log['message']) for log in logs]
                execute_batch(
                    cursor,
                    "INSERT INTO logs (timestamp, level, message) VALUES (%s, %s, %s)",
                    log_data
                )
                logger.info(f"{len(log_data)} logs inseridos com sucesso.")
    except Exception as e:
        logger.error("Erro ao processar logs: %s", e)
        conn.rollback()
    finally:
        db_pool.put_conn(conn)

if __name__ == "__main__":
   
    DSN = os.getenv("DATABASE_URL")
    if not DSN:
        raise ValueError("DATABASE_URL não encontrada no arquivo .env")
    
    db_pool = DatabasePool(DSN, minconn=2, maxconn=20)
    sample_logs = [
        {'timestamp': '2025-02-24 10:00:00', 'level': 'INFO', 'message': 'start process'},
        {'timestamp': '2025-02-24 10:00:05', 'level': 'ERROR', 'message': 'fail'},
        {'timestamp': '2025-02-24 10:00:10', 'level': 'INFO', 'message': 'ending process'},
    ]
    process_logs(sample_logs, db_pool)
    db_pool.close_all()
