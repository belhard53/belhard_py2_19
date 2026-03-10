import redis

r = redis.Redis()

r.set("q", '123')
a = r.get("q")

print(a)