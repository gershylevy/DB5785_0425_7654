# config_fixed.py - Fixed Database Configuration
import os
import subprocess

class DatabaseConfig:
    """Simple database configuration management"""
    
    def _init_(self):
        """Initialize with default configuration"""
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5050'),
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

def get_docker_postgres_ip():
    """Get Docker PostgreSQL container IP address"""
    try:
        result = subprocess.run(
            ['docker', 'inspect', '--format={{.NetworkSettings.IPAddress}}', 'postgres'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return None

def test_connection(config):
    """Test database connection with given configuration"""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            connect_timeout=config.get('connection_timeout', 10)
        )
        conn.close()
        return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False

# Docker helper commands
def get_docker_commands():
    """Get common Docker commands for PostgreSQL"""
    return {
        'start_postgres': 'docker start postgres',
        'stop_postgres': 'docker stop postgres',
        'postgres_status': 'docker ps | grep postgres',
        'postgres_logs': 'docker logs postgres',
        'connect_psql': 'docker exec -it postgres psql -U postgres'
    }

def print_docker_help():
    """Print Docker help commands"""
    commands = get_docker_commands()
    print("\nDocker PostgreSQL Commands:")
    print("-" * 30)
    for name, cmd in commands.items():
        print(f"{name:15}: {cmd}")

# Main execution for testing
if __name__ == "__main__":
    print("Database Configuration Test")
    print("=" * 40)
    
    try:
        # Test configuration
        db_config = DatabaseConfig()
        config = db_config.get_config()
        
        print("Default configuration:")
        for key, value in config.items():
            if key == 'password':
                display_value = '*' * len(str(value)) if value else '(empty)'
            else:
                display_value = value
            print(f"  {key:18}: {display_value}")
        
        print(f"\nConnection string: {db_config.get_connection_string()}")
        
        # Test Docker IP detection
        docker_ip = get_docker_postgres_ip()
        if docker_ip:
            print(f"\nDocker PostgreSQL IP: {docker_ip}")
            db_config.update_config(host=docker_ip)
            print("Updated configuration to use Docker IP")
        else:
            print("\nDocker PostgreSQL container not found or not running")
            print_docker_help()
        
        # Test connection (only if password is provided)
        if config['password']:
            print(f"\nTesting connection...")
            if test_connection(config):
                print("✅ Connection successful!")
            else:
                print("❌ Connection failed!")
        else:
            print("\n⚠  No password set - skipping connection test")
            print("   Set password with: db_config.update_config(password='your_password')")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 40)
    print("Configuration test completed")