import pandas as pd



def cleaning_livable_surface(surface):
    surface = int(surface)
    if surface > 2000 or surface <= 0:
        raise ValueError("area should be between 0 and 2000.")
    else:
        return surface

def cleaning_proprety_type(type):
    if type == "HOUSE":
        return 1
    if type == "APARTMENT":
        return 0
    if type == "OTHERS":
        return 1
    else:
        raise ValueError("Invalid property-type. Accepted values are ['HOUSE','APARTMENT', 'OTHERS']")

def cleaning_rooms_number(rooms):
    rooms = int(rooms)
    if rooms <= 0 or rooms > 20:
        raise ValueError("rooms-number must be between 0 and 20.")
    else:
        return rooms

def cleaning_zip_code(zip):
    zip = int(zip)
    if 999 < zip < 10000:
        return zip
    else:
        raise ValueError("Invalid zip code.")

def cleaning_building_state(state):
    if state == "NEW":
        return 3
    if state == "JUST RENOVATED":
        return 2
    if state == "GOOD":
        return 1
    if state == "TO RENOVATE":
        return 0
    if state == "TO REBUILD":
        return 0
    else:
        raise ValueError("Invalid building-state. Accepted values are ['NEW','JUST RENOVATED', 'GOOD','TO RENOVATE', 'TO REBUILD']")

def cleaning_facades_number(facades):
    facades = int(facades)
    if 0 <= facades > 4:
        raise ValueError("facades-number must be between 1 and 4.")
    else: 
        return facades

def cleaning_terrace(terrace):
    if terrace == 1 or terrace == 0:
        return terrace
    else:
        raise ValueError("terrace must be 1 or 0.")

def cleaning_surface_terrace(terrace):
    terrace = int(terrace)
    if terrace <= 0:
        return 8
    else:
        return terrace

def cleaning_open_fire(fire):
    if fire == 1 or fire == 0:
        return fire
    else:
        raise ValueError("open-fire must be 1 or 0.")

def cleaning_furnished(furnished):
    furnished = int(furnished)
    if furnished == 1 or furnished == 0:
        return furnished
    else: 
        raise ValueError("furnished must be 1 or 0.")

def cleaning_pool(pool):
    pool = int(pool)
    if pool == 1:
        return pool
    else: 
        return 0

def full_address(address):
    address = str(address)
    return full_address

def cleaning_equipped_kitchen(kitchen):
    kitchen = int(kitchen)
    if kitchen == 1:
        return 2
    else:
        return 0

def cleaning_garden(garden):
    garden = int(garden)
    if garden == 1:
        return garden
    else:
        return 0

def cleaning_garden_surface(garden):
    garden = int(garden)
    if  0 < garden < 4000:
        return garden
    else:
        return 65

def preprocess(json_data):
    print("data",json_data)

    df = pd.DataFrame(json_data, index=[0])

    type = {'HOUSE': 2, 'APARTMENT': 1, "OTHERS" : 0}
    df['property_type'].replace(type, inplace=True)

    state = {'NEW': 5, 'JUST RENOVATED': 4,
                     'GOOD': 3, 'TO RENOVATE': 2, 'TO REBUILD': 1}
    df['building_state'].replace(state, inplace=True)

    kitchen = {False: 0, True: 1}
    df['equipped_kitchen'].replace(kitchen, inplace=True)

    pool = {False: 0, True: 1}
    df['swimming_pool'].replace(pool, inplace=True)

    garden = {False: 0, True: 1}
    df['garden'].replace(garden, inplace=True)

    terrace = {False: 0, True: 1}
    df['terrace'].replace(terrace, inplace=True)

    furnished = {False: 0, True: 1}
    df['furnished'].replace(furnished, inplace=True)

    open_fire = {False: 0, True: 1}
    df['open_fire'].replace(open_fire, inplace=True)

    df['land_area'].fillna(0, inplace=True)

    df['terrace_area'].fillna(0, inplace=True)

    df['facades_number'].fillna(1, inplace=True)

    df = df[[
        "area",
        "property_type",
        "rooms_number",
        "land_area",
        "zip_code",
        "garden",
        "garden_area",
        "equipped_kitchen",
        "swimming_pool",
        "furnished",
        "open_fire",
        "terrace",
        "terrace_area",
        "facades_number",
        "building_state"]]

    return df
