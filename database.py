import json

### DATABASE.PY ###
# This file is used to read the database.json file and return the data as a dictionary.
###################



database = None


async def get_database():
    global database
    if database == None :
        with open('database.json') as f:
            database = json.load(f)
    return database


async def add_message(id : int, authorId : int) -> None :
    if database == None :
        await get_database()

    database["messages"] = database["messages"] | {str(id) : authorId}

    await save_database()

async def is_waiting(id : int) -> bool :
    if database == None :
        await get_database()
    return id in database["messages"].values()

async def remove_message(id : int, authorId : int) -> None :
    if database == None :
        await get_database()
        
    if str(id) in database["messages"] :
        if database["messages"][str(id)] == authorId :
            del database["messages"][str(id)]
            await save_database()
        else :
            pass
    else :
        pass



async def get_messages(id : int) -> tuple[int, int]:
    if database == None :
        await get_database()

    if str(id) in database["messages"] :
        return (id, database["messages"][str(id)])
    else :
        return None
    

async def save_database():
    global database
    if database != None :
        with open('database.json', 'w') as f:
            json.dump(database, f)


async def init_conf(id : int) -> None :
    global database
    if database == None :
        await get_database()
    database['init'] = id
    await save_database()


async def get_conf() -> int:
    global database
    if database == None :
        await get_database()
    return database['init']
