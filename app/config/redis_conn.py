import os
import redis
from dotenv import load_dotenv

load_dotenv()
redis_conn = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, db=0)
