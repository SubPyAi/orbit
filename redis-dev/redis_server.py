import redis

# 1. Connect using explicit IPv4 and decode_responses=True
r = redis.Redis(
    host='127.0.0.1', 
    port=6379, 
    db=0, 
    decode_responses=True, # Automatically converts bytes to strings
    socket_timeout=2.0
)

print("=== Connected to Memurai successfully! ===\n")

# -------------------------------------------------------------
# 1. STRINGS (Basic Key-Value Data)
# -------------------------------------------------------------
print("--- 1. Strings ---")
# Write
r.set("app:name", "My Windows Chat App")
r.set("app:version", "1.0.0")

# Read
app_name = r.get("app:name")
app_version = r.get("app:version")
print(f"App Name: {app_name} (Version: {app_version})")


# -------------------------------------------------------------
# 2. HASHES (User Profiles & Objects)
# -------------------------------------------------------------
print("\n--- 2. Hashes (User Profiles) ---")
# Write
r.hset("user:101", mapping={
    "username": "Alice",
    "status": "online",
    "role": "admin"
})

# Read
user_profile = r.hgetall("user:101")  # Returns a Python dictionary
print(f"User 101 Profile: {user_profile}")
print(f"Username only: {user_profile.get('username')}")


# -------------------------------------------------------------
# 3. LISTS (Message History & Queues)
# -------------------------------------------------------------
print("\n--- 3. Lists (Message History) ---")
# Write (Pushing items to the list)
r.rpush("room:general:history", "Alice: Hey everyone!")
r.rpush("room:general:history", "Bob: Hi Alice, Memurai is fast!")
r.rpush("room:general:history", "Alice: Works great on Windows!")

# Read (Get all messages from index 0 to -1)
messages = r.lrange("room:general:history", 0, -1)
print("Chat History:")
for msg in messages:
    print(f"  - {msg}")


# -------------------------------------------------------------
# 4. SETS (Active Online Roster)
# -------------------------------------------------------------
print("\n--- 4. Sets (Online Users) ---")
# Write (Adds unique items)
r.sadd("room:general:active", "Alice")
r.sadd("room:general:active", "Bob")
r.sadd("room:general:active", "Alice")  # Duplicate ignored automatically

# Read
online_users = r.smembers("room:general:active")  # Returns a Python set
print(f"Users online in #general: {online_users}")


# -------------------------------------------------------------
# 5. EXPIRING KEYS (Typing Indicators)
# -------------------------------------------------------------
print("\n--- 5. Key Expiration / TTL ---")
# Set a key that auto-deletes in 5 seconds
r.set("typing:general:Alice", "true", ex=5)

ttl = r.ttl("typing:general:Alice")
print(f"Is Alice typing? {r.exists('typing:general:Alice') > 0}")
print(f"Seconds remaining before auto-delete: {ttl}s")