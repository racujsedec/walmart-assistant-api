import json,os
async def get_cached(key:str):
 if not os.getenv('REDIS_URL'):return None
 from redis.asyncio import from_url
 client=from_url(os.environ['REDIS_URL'],decode_responses=True)
 try:
  raw=await client.get(key);return json.loads(raw) if raw else None
 finally:await client.aclose()
async def set_cached(key:str,value:dict,ttl:int=15):
 if not os.getenv('REDIS_URL'):return
 from redis.asyncio import from_url
 client=from_url(os.environ['REDIS_URL'],decode_responses=True)
 try:await client.set(key,json.dumps(value),ex=ttl)
 finally:await client.aclose()
