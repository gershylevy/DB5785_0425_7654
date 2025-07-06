# config/database.py - Database Configuration
"""
Database configuration and connection management
"""
import os
import psycopg2
from psycopg2.extras import DictCursor

class DatabaseConfig:
    """Database configuration management"""
    
    def __init__(self):
        """Initialize with default configuration"""
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'connection_timeout': 30,
            'command_timeout': 60
        }
    
    def get_config(self):
        """Get current configuration"""
        return self.config.copy()
    
    def update_config(self, **kwargs):
        """Update configuration parameters"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
    
    def get_connection_string(self):
        """Generate PostgreSQL connection string"""
        return f"postgresql://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"

class DatabaseManager:
    """Database connection manager"""
    
    def __init__(self, config=None):
        self.config = config or DatabaseConfig()
        self.connection = None
        self.cursor = None
    
    def connect(self, host, port, database, user, password):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)
            return True
        except Exception as e:
            raise Exception(f"Failed to connect to database: {str(e)}")
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def test_connection(self):
        """Test database connection"""
        try:
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()[0]
            return True, version
        except Exception as e:
            return False, str(e)
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            self.cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            raise e
