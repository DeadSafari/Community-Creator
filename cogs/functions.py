import aiosqlite3

async def get_mod_log(uuid: str):
    conn = await aiosqlite3.connect('mydatabase.db')
    cursor = await conn.cursor()
    await cursor.execute(f"SELECT * FROM moderation_logs WHERE uuid = ?", (uuid,))
    row = await cursor.fetchone()
    modlog = {
        "member": row[0],
        "moderator_id": row[1],
        "time": row[2],
        "type": row[3],
        "reason": row[4],
        "execution_time": row[5],
        "uuid": row[6]
    }
    return modlog

async def get_mod_logs(user_id: int):
    conn = await aiosqlite3.connect('mydatabase.db')
    cursor = await conn.cursor()
    await cursor.execute(f"SELECT * FROM moderation_logs WHERE user_id = ?", (user_id,))
    rows = await cursor.fetchall()
    modlogs = []
    for row in rows:
        modlogs.append({
        "member": row[0],
        "moderator_id": row[1],
        "time": row[2],
        "type": row[3],
        "reason": row[4],
        "execution_time": row[5],
        "uuid": row[6]
    })
    return modlogs

async def create_moderation_logs_table():
    # Connect to the database
    db = await aiosqlite3.connect('mydatabase.db')

    # Create a cursor
    c = await db.cursor()

    # Create the 'moderation_logs' table
    await c.execute('''CREATE TABLE IF NOT EXISTS moderation_logs (
        user_id INTEGER,
        moderator_id INTEGER,
        time INTEGER,
        type TEXT,
        reason TEXT,
        execution_time INTEGER,
        uuid TEXT
    )''')

    await c.execute('''CREATE TABLE IF NOT EXISTS mute_roles (
        user_id INTEGER,
        roles TEXT
    )''')

    # Commit the transaction and close the connection
    await db.commit()
    await db.close()

async def add_moderation_log(user_id: int, moderator_id: int, time: int, Type: str, reason: str, execution_time: int, uuid: str):
    # Connect to the database
    db = await aiosqlite3.connect('mydatabase.db')

    # Create a cursor
    c = await db.cursor()

    # Insert a new row into the 'moderation_logs' table
    await c.execute("INSERT INTO moderation_logs (user_id, moderator_id, time, type, reason, execution_time, uuid) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, moderator_id, time, Type, reason, execution_time, uuid))

    # Commit the transaction and close the connection
    await db.commit()
    await db.close()

async def delete_moderation_log(uuid: str):
    # Connect to the database
    db = await aiosqlite3.connect('mydatabase.db')

    # Create a cursor
    c = await db.cursor()

    # Delete the row from the 'moderation_logs' table
    await c.execute("DELETE FROM moderation_logs WHERE uuid=?", (uuid,))

    # Commit the transaction and close the connection
    await db.commit()
    await db.close()

async def add_mute_role(user_id: int, roles: list):
    # Connect to the database
    db = await aiosqlite3.connect('mydatabase.db')

    # Create a cursor
    c = await db.cursor()

    # Insert a new row into the 'mute_roles' table
    await c.execute("INSERT INTO mute_roles (user_id, roles) VALUES (?, ?)", (user_id, str({'roles': roles}),))

    # Commit the transaction and close the connection
    await db.commit()
    await db.close()

async def get_mute_roles(user_id: int):
    conn = await aiosqlite3.connect('mydatabase.db')
    cursor = await conn.cursor()
    await cursor.execute(f"SELECT * FROM mute_roles WHERE user_id = ?", (user_id,))
    row = await cursor.fetchone()
    return row[1]

async def delete_mute_roles(user_id: int):
    # Connect to the database
    db = await aiosqlite3.connect('mydatabase.db')

    # Create a cursor
    c = await db.cursor()

    # Delete the row from the 'mute_roles' table
    await c.execute("DELETE FROM mute_roles WHERE user_id=?", (user_id,))

    # Commit the transaction and close the connection
    await db.commit()
    await db.close()