# algorithms.py
"""
Title: Algorithms for Fashion Program
Date: December 16, 2022
"""
# --- LIBRARIES --- #
import pathlib
import sqlite3
import flask
from itertools import combinations


# --- SUBROUTINES --- #
# Input
def setup():
    """
    Sets up the database
    :return: None
    """
    global CONNECTION, CURSOR  # to set up database
    CURSOR.execute("""
    CREATE TABLE Clothing (
        Clothing_ID INT PRIMARY KEY,
        Name TEXT NOT NULL,
        Color1 TEXT NOT NULL,
        Style1 TEXT NOT NULL,
        Fabric1 TEXT NOT NULL,
        Weather INT NOT NULL,
        Score INT NOT NULL,
        Link TEXT NOT NULL,
        Type TEXT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Color_2 (
        Clothing_ID INT PRIMARY KEY,
        Data TEXT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Color_3 (
        Clothing_ID INT PRIMARY KEY,
        Data TEXT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Style_2 (
        Clothing_ID INT PRIMARY KEY,
        Data TEXT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Fabric_2 (
        Clothing_ID INT PRIMARY KEY,
        Data TEXT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Outfits (
        Outfit_ID INT PRIMARY KEY,
        Name TEXT NOT NULL,
        Top INT NOT NULL,
        Bottom INT NOT NULL,
        Shoes INT NOT NULL,
        Comment INT NOT NULL,
        Rating INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Sweater (
        Outfit_ID INT PRIMARY KEY,
        Clothing_ID INT NOT NULL
    )
    ;""")
    CURSOR.execute(f"""
    CREATE TABLE Additional_Jacket (
        Outfit_ID INT PRIMARY KEY,
        Clothing_ID INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Accessory_1 (
        Outfit_ID INT PRIMARY KEY,
        Clothing_ID INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Accessory_2 (
        Outfit_ID INT PRIMARY KEY,
        Clothing_ID INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Accessory_3 (
        Outfit_ID INT PRIMARY KEY,
        Clothing_ID INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Accessory_4 (
        Outfit_ID INT PRIMARY KEY,
        Clothing_ID INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Accessory_5 (
        Outfit_ID INT PRIMARY KEY,
        Clothing_ID INT NOT NULL
    );
    """)
    CONNECTION.commit()


def inputNewClothing():
    """
    Gets input and formats into list
    :return: list
    """
    # Input
    CLOTHING_NAME = input("Clothing: ")
    FIRST_COLOR = input("1 Color: ")
    SECOND_COLOR = input("2 Color: ")
    THIRD_COLOR = input("3 Color: ")
    COLOR_LIST = [FIRST_COLOR, SECOND_COLOR, THIRD_COLOR]
    FIRST_STYLE = input("1 Style: ")
    SECOND_STYLE = input("2 Style: ")
    STYLE_LIST = [FIRST_STYLE, SECOND_STYLE]
    FIRST_FABRIC = input("1 Fabric: ")
    SECOND_FABRIC = input("2 Fabric: ")
    FABRIC_LIST = [FIRST_FABRIC, SECOND_FABRIC]
    WEATHER = input("Weather: ")
    SCORE = int(input("Score: "))
    IMAGE_LINK = input("Link: ")
    CLOTHING_TYPE = input("Type: ")

    # Format information
    CLOTHING_INFORMATION = [CLOTHING_NAME, COLOR_LIST, STYLE_LIST, FABRIC_LIST,
                            WEATHER, SCORE, IMAGE_LINK, CLOTHING_TYPE]
    return CLOTHING_INFORMATION


def inputEditClothing():
    pass


def inputOutfit():
    """
    Get user input for the outfit
    :return: list
    """
    """
        Name TEXT NOT NULL,
        Top INT NOT NULL,
        Bottom INT NOT NULL,
        Shoes INT NOT NULL,
        Comment INT NOT NULL,
        Rating INT NOT NULL
    """
    OUTFIT_NAME = input("Outfit: ")
    TOP_ID = int(input("Top: "))
    BOTTOM_ID = int(input("Bottom: "))
    SHOES_ID = int(input("Shoes: "))
    SWEATER_ID = int(input("Sweater: "))
    JACKET_ID = int(input("Jacket: "))
    ACCESSORY_1_ID = int(input("Accessory 1: "))
    ACCESSORY_2_ID = int(input("Accessory 2: "))
    ACCESSORY_3_ID = int(input("Accessory 3: "))
    ACCESSORY_4_ID = int(input("Accessory 4: "))
    ACCESSORY_5_ID = int(input("Accessory 5: "))
    ACCESSORY_LIST = []

    # Format accessory list in ascending id
    # Only sort non-empty
    if not(ACCESSORY_1_ID is None or ACCESSORY_1_ID == "" or ACCESSORY_1_ID == 0):
        ACCESSORY_LIST.append(ACCESSORY_1_ID)
    if not(ACCESSORY_2_ID is None or ACCESSORY_2_ID == "" or ACCESSORY_2_ID == 0):
        ACCESSORY_LIST.append(ACCESSORY_2_ID)
    if not(ACCESSORY_3_ID is None or ACCESSORY_3_ID == "" or ACCESSORY_3_ID == 0):
        ACCESSORY_LIST.append(ACCESSORY_3_ID)
    if not(ACCESSORY_4_ID is None or ACCESSORY_4_ID == "" or ACCESSORY_4_ID == 0):
        ACCESSORY_LIST.append(ACCESSORY_4_ID)
    if not(ACCESSORY_5_ID is None or ACCESSORY_5_ID == "" or ACCESSORY_5_ID == 0):
        ACCESSORY_LIST.append(ACCESSORY_5_ID)
    ACCESSORY_LIST.sort()

    # Get to length of 5
    while len(ACCESSORY_LIST) < 5:
        ACCESSORY_LIST.append(None)

    COMMENT = input("Comment: ")
    RATING = int(input("Rating: "))

    # Format of information: name, top, bottom, shoes, sweater, jacket, accessories, comment, rating
    return [OUTFIT_NAME, TOP_ID, BOTTOM_ID, SHOES_ID, SWEATER_ID,
            JACKET_ID, ACCESSORY_LIST, COMMENT, RATING]


# Processing
def recentClothingID():
    """
    Find most recent primary key in clothing table
    :return: integer
    """
    global CURSOR
    # Go into database
    RECENT_PRIMARY_KEY = CURSOR.execute("""
        SELECT
            Clothing_ID
        FROM
            Clothing
        ORDER BY
            Clothing_ID DESC
    """).fetchone()
    if RECENT_PRIMARY_KEY is None:
        RECENT_PRIMARY_KEY = [999]  # all primary keys have 4 digits
    return RECENT_PRIMARY_KEY[0]


def recentOutfitID():
    """
    Find most recent primary key in outfit table
    :return: integer
    """
    global CURSOR
    # Go into database
    RECENT_PRIMARY_KEY = CURSOR.execute("""
        SELECT
            Outfit_ID
        FROM
            Outfits
        ORDER BY
            Outfit_ID DESC
    """).fetchone()
    if RECENT_PRIMARY_KEY is None:
        RECENT_PRIMARY_KEY = [999]  # all primary keys have 4 digits
    return RECENT_PRIMARY_KEY[0]


def insertNewClothing(CLOTHING_INFORMATION):
    """
    Insert new clothing into the database
    :param CLOTHING_INFORMATION: list
    :return: none
    """
    global CURSOR, CONNECTION
    # FIND PRIMARY KEY
    # Find most recent primary key
    CLOTHING_PRIMARY_KEY = recentClothingID() + 1

    # Find information that is always not null
    NON_EMPTY_INFORMATION = [
        CLOTHING_PRIMARY_KEY,
        CLOTHING_INFORMATION[0],
        CLOTHING_INFORMATION[1][0],
        CLOTHING_INFORMATION[2][0],
        CLOTHING_INFORMATION[3][0],
        CLOTHING_INFORMATION[4],
        CLOTHING_INFORMATION[5],
        CLOTHING_INFORMATION[6],
        CLOTHING_INFORMATION[7],
    ]

    # Find information that may be null
    OPTIONAL_INFORMATION = [
        ["Additional_Color_2", CLOTHING_INFORMATION[1][1]],
        ["Additional_Color_3", CLOTHING_INFORMATION[1][2]],
        ["Additional_Style_2", CLOTHING_INFORMATION[2][1]],
        ["Additional_Fabric_2", CLOTHING_INFORMATION[3][1]]
    ]

    CURSOR.execute("""
        INSERT INTO 
            Clothing 
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        ) 
    ;""", NON_EMPTY_INFORMATION)

    # Get other colors if they exist
    for INFORMATION in OPTIONAL_INFORMATION:
        if not (INFORMATION[1] is None or INFORMATION[1] == ""):
            CURSOR.execute(f"""
            INSERT INTO
                {INFORMATION[0]}
            VALUES (
                ?, ?
            )
            ;""", [CLOTHING_PRIMARY_KEY, INFORMATION[1]])
    CONNECTION.commit()


def deleteOutfit(OUTFIT_ID):
    """
    Deletes outfit with the outfit id
    :param OUTFIT_ID: int
    :return: none
    """
    global CURSOR, CONNECTION, OPTIONAL_CLOTHING_DATA

    # Main outfit table
    CURSOR.execute("""
    DELETE FROM
        Outfits
    WHERE
        Outfit_ID = ?
    ;""", [OUTFIT_ID])

    # Side accessory tables
    for ADDITIONAL_TABLE in OPTIONAL_OUTFIT_DATA:
        CURSOR.execute(f"""
            DELETE FROM
                {ADDITIONAL_TABLE}
            WHERE
                Outfit_ID = {OUTFIT_ID}
        ;""")

    CONNECTION.commit()


def deleteClothing(CLOTHING_ID):
    """
    Deletes clothing
    :param CLOTHING_ID: integer
    :return: none
    """
    global CURSOR, CONNECTION, OPTIONAL_CLOTHING_DATA

    # Find the type of clothing
    DELETING_CLOTHING_TYPE = CURSOR.execute("""
        SELECT
            Type
        FROM
            CLOTHING
        WHERE
            Clothing_ID = ?
        ;""", [CLOTHING_ID]).fetchone()

    # Find outfits with this clothing

    # Initialize an array for outfit ids to delete
    OUTFITS_TO_DELETE = []

    # Check if in main outfit table
    if DELETING_CLOTHING_TYPE in ["Top", "Bottom", "Shoes"]:
        TO_DELETE = CURSOR.execute(f"""
            SELECT
                Outfit_ID
            FROM
                Outfits
            WHERE
                {DELETING_CLOTHING_TYPE} = ?
        ;""", [CLOTHING_ID]).fetchall()
        OUTFITS_TO_DELETE += TO_DELETE

    # If a sweater or jacket
    if DELETING_CLOTHING_TYPE in ["Sweater", "Jacket"]:
        TO_DELETE = CURSOR.execute(f"""
            SELECT
                Outfit_ID
            FROM
                Additional_{DELETING_CLOTHING_TYPE}
            WHERE
                Clothing_ID = ?
        ;""", [CLOTHING_ID]).fetchall()
        OUTFITS_TO_DELETE += TO_DELETE

    # If an accessory
    if DELETING_CLOTHING_TYPE == "Accessory":
        for i in range(5):  # Search in all extra accessory tables
            TO_DELETE = CURSOR.execute(f"""
                SELECT
                    Outfit_ID
                FROM
                    Additional_Accessory_{i+1}
                WHERE
                    Clothing_ID = ?
            ;""", [CLOTHING_ID]).fetchall()
            OUTFITS_TO_DELETE += TO_DELETE

    # Delete the outfits
    OUTFIT_NAMES = []  # Log the outfits that will be deleted
    for OUTFIT in OUTFITS_TO_DELETE:
        # Find names of all the outfits to help inform user
        NAME = CURSOR.execute(f"""
        SELECT
            Name
        FROM
            Outfits
        WHERE
            Outfit_ID = ?
        ;""", [OUTFIT]).fetchone()
        OUTFIT_NAMES += NAME
        deleteOutfit(OUTFIT)

    # Main clothing
    CURSOR.execute("""
        DELETE FROM
            Clothing
        WHERE
            Clothing_ID = ?
    ;""", [CLOTHING_ID])

    # Additional information
    for ADDITIONAL_TABLE in OPTIONAL_CLOTHING_DATA:
        CURSOR.execute(f"""
            DELETE FROM
                {ADDITIONAL_TABLE}
            WHERE
                Clothing_ID = {CLOTHING_ID}
        ;""")

    CONNECTION.commit()


def getExistingClothingInfo(CLOTHING_PRIMARY_KEY):
    """
    Gets all the information about the clothing with the primary key
    :param CLOTHING_PRIMARY_KEY: int
    :return: list
    """
    global CURSOR
    FILLED_INFORMATION = CURSOR.execute("""
    SELECT
        *
    FROM
        Clothing
    WHERE
        Clothing_ID = ?
    ;""", [CLOTHING_PRIMARY_KEY]).fetchone()

    # turn clothing information into a list, not a tuple
    CLOTHING_INFORMATION = []
    for INFORMATION in FILLED_INFORMATION:
        CLOTHING_INFORMATION.append(INFORMATION)

    # Find additional information
    ADDITIONAL_COLOR_2 = CURSOR.execute("""
    SELECT
        Data
    FROM
        Additional_Color_2
    WHERE
        Clothing_ID = ?
    ;""", [CLOTHING_PRIMARY_KEY]).fetchone()
    ADDITIONAL_COLOR_3 = CURSOR.execute("""
    SELECT
        Data
    FROM
        Additional_Color_3
    WHERE
        Clothing_ID = ?
    ;""", [CLOTHING_PRIMARY_KEY]).fetchone()
    ADDITIONAL_FABRIC_2 = CURSOR.execute("""
    SELECT
        Data
    FROM
        Additional_Fabric_2
    WHERE
        Clothing_ID = ?
    ;""", [CLOTHING_PRIMARY_KEY]).fetchone()
    ADDITIONAL_STYLE_2 = CURSOR.execute("""
    SELECT
        Data
    FROM
        Additional_Style_2
    WHERE
        Clothing_ID = ?
    ;""", [CLOTHING_PRIMARY_KEY]).fetchone()

    # Format list
    CLOTHING_INFORMATION[2] = [CLOTHING_INFORMATION[2]]
    CLOTHING_INFORMATION[3] = [CLOTHING_INFORMATION[3]]
    CLOTHING_INFORMATION[4] = [CLOTHING_INFORMATION[4]]

    # Add additional information if it is not null
    if ADDITIONAL_COLOR_2 is not None:
        CLOTHING_INFORMATION[2].append(ADDITIONAL_COLOR_2[0])
    if ADDITIONAL_COLOR_3 is not None:
        CLOTHING_INFORMATION[2].append(ADDITIONAL_COLOR_3[0])
    if ADDITIONAL_STYLE_2 is not None:
        CLOTHING_INFORMATION[3].append(ADDITIONAL_STYLE_2[0])
    if ADDITIONAL_FABRIC_2 is not None:
        CLOTHING_INFORMATION[4].append(ADDITIONAL_FABRIC_2[0])

    return CLOTHING_INFORMATION


def getExistingOutfitInfo(OUTFIT_PRIMARY_KEY):
    """
    Gets all the information about the clothing with the primary key
    :param OUTFIT_PRIMARY_KEY: int
    :return: list, list
    """
    global CURSOR, OPTIONAL_OUTFIT_DATA
    FILLED_INFORMATION = CURSOR.execute("""
    SELECT
        *
    FROM
        Outfits
    WHERE
        Outfit_ID = ?
    ;""", [OUTFIT_PRIMARY_KEY]).fetchone()

    # turn clothing information into a list, not a tuple
    OUTFIT_INFORMATION = []
    for INFORMATION in FILLED_INFORMATION:
        OUTFIT_INFORMATION.append(INFORMATION)

    # Find additional information
    OPTIONAL_OUTFIT_INFORMATION = []
    for i in range(len(OPTIONAL_OUTFIT_DATA)):
        OPTIONAL_ITEM = CURSOR.execute(f"""
            SELECT
                Clothing_ID
            FROM
                {OPTIONAL_OUTFIT_DATA[i]}
            WHERE
                Outfit_ID = ?
        ;""", [OUTFIT_PRIMARY_KEY])
        OPTIONAL_OUTFIT_INFORMATION.append(OPTIONAL_ITEM)

    return FILLED_INFORMATION, OPTIONAL_OUTFIT_INFORMATION


def updateClothing(CLOTHING_PRIMARY_KEY, NEW_INFORMATION):
    """
    Updates clothing with new info
    :param CLOTHING_PRIMARY_KEY: integer
    :param NEW_INFORMATION: list
    :return: none
    """
    global CURSOR, CONNECTION, OPTIONAL_CLOTHING_DATA
    # Find existing information
    EXISTING_INFORMATION = getExistingClothingInfo(CLOTHING_PRIMARY_KEY)

    # Get information in main table
    for i in range(len(NEW_INFORMATION)):
        if NEW_INFORMATION[i] is None or NEW_INFORMATION[i] == "":
            NEW_INFORMATION[i] = EXISTING_INFORMATION[i + 1]  # Fill in with existing information

    # non-empty information does not get deleted, will get updated
    NON_EMPTY_INFORMATION = [
        NEW_INFORMATION[0],
        NEW_INFORMATION[1][0],
        NEW_INFORMATION[2][0],
        NEW_INFORMATION[3][0],
        NEW_INFORMATION[4],
        NEW_INFORMATION[5],
        NEW_INFORMATION[6],
        NEW_INFORMATION[7],
        CLOTHING_PRIMARY_KEY]
    # Get information in side tables
    # Feature of program: if additional are left empty, then it is deleted
    # Make sure indices exist
    while len(EXISTING_INFORMATION[2]) < 3:
        EXISTING_INFORMATION[2].append(None)
    while len(EXISTING_INFORMATION[3]) < 2:
        EXISTING_INFORMATION[3].append(None)
    while len(EXISTING_INFORMATION[4]) < 2:
        EXISTING_INFORMATION[4].append(None)

    # Format it
    EXISTING_OPTIONAL_INFORMATION = [
        EXISTING_INFORMATION[2][1],
        EXISTING_INFORMATION[2][2],
        EXISTING_INFORMATION[3][1],
        EXISTING_INFORMATION[4][1]
    ]
    OPTIONAL_INFORMATION = [
        NEW_INFORMATION[1][1],
        NEW_INFORMATION[1][2],
        NEW_INFORMATION[2][1],
        NEW_INFORMATION[3][1]
    ]
    # Update
    CURSOR.execute("""
        UPDATE
            Clothing
        SET
            Name = ?,
            Color1 = ?,
            Style1 = ?,
            Fabric1 = ?,
            Weather = ?,
            Score = ?,
            Link = ?,
            Type = ?  
        WHERE
            Clothing_ID = ?
    ;""", NON_EMPTY_INFORMATION)

    # Update other tables
    for i in range(len(OPTIONAL_CLOTHING_DATA)):
        if OPTIONAL_INFORMATION[i] is not None and OPTIONAL_INFORMATION[i] != "":
            # columns exist
            if EXISTING_OPTIONAL_INFORMATION[i] is not None:
                CURSOR.execute(f"""
                UPDATE
                    {OPTIONAL_CLOTHING_DATA[i]}
                SET
                    Data = ?
                WHERE
                    Clothing_ID = ?
                ;""", [OPTIONAL_INFORMATION[i], CLOTHING_PRIMARY_KEY])
            # columns do not exist
            else:
                CURSOR.execute(f"""
                INSERT INTO
                    {OPTIONAL_CLOTHING_DATA[i]}
                VALUES (
                    ?, ?
                )
                ;""", [CLOTHING_PRIMARY_KEY, OPTIONAL_INFORMATION[i]])
        else:  # no information provided for extra fields
            # columns exist
            if EXISTING_OPTIONAL_INFORMATION[i] is not None:
                CURSOR.execute(f"""
                DELETE FROM
                    {OPTIONAL_CLOTHING_DATA[i]}
                WHERE
                    Clothing_ID = ?
                ;""", [CLOTHING_PRIMARY_KEY])
            # else, nothing happens
    CONNECTION.commit()


def insertOutfit(OUTFIT_INFORMATION):
    """
    Inserts new outfit into database
    :param OUTFIT_INFORMATION: list
    :return: none
    """
    global CURSOR, CONNECTION, OPTIONAL_OUTFIT_DATA
    # Find new primary key
    OUTFIT_PRIMARY_KEY = recentOutfitID() + 1

    # Get important information from argument
    # Want: [name, top, bottom, shoes, comment, rating]
    # OUTFIT_INFORMATION: [name, top, bottom, shoes, sweater, jacket, accessories, comment, rating]
    FILLED_INFORMATION = [
        OUTFIT_PRIMARY_KEY,
        OUTFIT_INFORMATION[0],
        OUTFIT_INFORMATION[1],
        OUTFIT_INFORMATION[2],
        OUTFIT_INFORMATION[3],
        OUTFIT_INFORMATION[7],
        OUTFIT_INFORMATION[8]
    ]

    # Find optional information: [sweater, jacket, accessories]
    OPTIONAL_INFORMATION = [
        OUTFIT_INFORMATION[4],
        OUTFIT_INFORMATION[5]
    ]
    # For accessories to be on one line
    for ACCESSORY in OUTFIT_INFORMATION[6]:
        if not(ACCESSORY is None or ACCESSORY == "" or ACCESSORY == 0):
            OPTIONAL_INFORMATION.append(ACCESSORY)

    # Insert information that is not null
    CURSOR.execute("""
    INSERT INTO
        Outfits
    VALUES (
        ?, ?, ?, ?, ?, ?, ?
    )
    ;""", FILLED_INFORMATION)

    # Insert other information in their own tables
    for i in range(len(OPTIONAL_INFORMATION)):
        if not(OPTIONAL_INFORMATION[i] is None or OPTIONAL_INFORMATION[i] == "" or OPTIONAL_INFORMATION[i] == 0):
            CURSOR.execute(f"""
                INSERT INTO
                    {OPTIONAL_OUTFIT_DATA[i]}
                VALUES (
                    ?, ?
                )
            ;""", [OUTFIT_PRIMARY_KEY, OPTIONAL_INFORMATION[i]])

    CONNECTION.commit()


def combineListsNoDuplicates(LIST_1, LIST_2, LIST_3=(), LIST_4=()):
    """
    Combines all lists in parameters
    :param LIST_1: list
    :param LIST_2: list
    :param LIST_3: list
    :param LIST_4: list
    :return: list
    """
    # Combine all together
    COMBINED_LIST = LIST_1 + LIST_2 + LIST_3 + LIST_4
    # Get rid of duplicates
    return list(set(COMBINED_LIST))


def intersectionOfLists(LIST_1, LIST_2):
    """
    Returns list of only values that are in both lists
    :param LIST_1: list
    :param LIST_2: list
    :return: list
    """
    INTERSECTION_LIST = []
    # If there is a none, then return other list (i.e. those settings not selected)
    if LIST_1 is None and LIST_2 is None:
        return None
    elif LIST_1 is None:
        return LIST_2
    elif LIST_2 is None:
        return LIST_1
    else:
        for ITEM in LIST_1:
            if ITEM in LIST_2:
                INTERSECTION_LIST.append(ITEM)

    return INTERSECTION_LIST


def getScore(OUTFIT):
    """
    For sorting, the key
    :param OUTFIT: list
    :return: int
    """
    return OUTFIT[1]


def generateOutfit(SETTINGS):
    """
    Generates outfit when given some settings
    :param SETTINGS: list [color1, color2, color3, style1, style2, fabric1, fabric2, weather]
    :return: 2d list
    """

    # Split SETTINGS into its categories
    COLOR_SETTINGS = SETTINGS[0:3]
    STYLE_SETTINGS = SETTINGS[3:5]
    FABRIC_SETTINGS = SETTINGS[5:7]
    WEATHER_SETTING = SETTINGS[8]

    # Initialize possible clothing lists to do operations
    if len(COLOR_SETTINGS) > 0:
        POSSIBLE_CLOTHING_COLOR = []
    else:
        POSSIBLE_CLOTHING_COLOR = None
    if len(STYLE_SETTINGS) > 0:
        POSSIBLE_CLOTHING_STYLE = []
    else:
        POSSIBLE_CLOTHING_STYLE = None
    if len(FABRIC_SETTINGS) > 0:
        POSSIBLE_CLOTHING_FABRIC = []
    else:
        POSSIBLE_CLOTHING_FABRIC = None

    # For colors
    for COLOR in COLOR_SETTINGS:  # This finds all clothing with the color as one of their colors
        COLOR_1_CLOTHING = CURSOR.execute("""
            SELECT 
                Clothing_ID,
                Type
            FROM
                Clothing
            WHERE
                Color1 = ?
        ;""", [COLOR]).fetchall()
        COLOR_2_CLOTHING = CURSOR.execute("""
            SELECT
                Additional_Color_2.Clothing_ID,
                Clothing.Type
            FROM 
                Additional_Color_2
            JOIN
                Clothing
            ON
                Additional_Color_2.Clothing_ID = Clothing.Clothing_ID
            WHERE
                Additional_Color_2.Data = ?
        ;""", [COLOR]).fetchall()
        COLOR_3_CLOTHING = CURSOR.execute("""
            SELECT
                Additional_Color_3.Clothing_ID,
                Clothing.Type
            FROM 
                Additional_Color_3
            JOIN
                Clothing
            ON
                Additional_Color_3.Clothing_ID = Clothing.Clothing_ID
            WHERE
                Additional_Color_3.Data = ?
        ;""", [COLOR]).fetchall()
        # Combine lists together
        POSSIBLE_CLOTHING_COLOR = combineListsNoDuplicates(COLOR_1_CLOTHING, COLOR_2_CLOTHING, COLOR_3_CLOTHING)

    # For styles
    for STYLE in STYLE_SETTINGS:
        STYLE_1_CLOTHING = CURSOR.execute("""
            SELECT 
                Clothing_ID,
                Type
            FROM
                Clothing
            WHERE
                Style1 = ?
        ;""", [STYLE]).fetchall()
        STYLE_2_CLOTHING = CURSOR.execute("""
            SELECT
                Additional_Style_2.Clothing_ID,
                Clothing.Type
            FROM 
                Additional_Style_2
            JOIN
                Clothing
            ON
                Additional_Style_2.Clothing_ID = Clothing.Clothing_ID
            WHERE
                Additional_Style_2.Data = ?
        ;""", [STYLE]).fetchall()
        POSSIBLE_CLOTHING_STYLE = combineListsNoDuplicates(STYLE_1_CLOTHING, STYLE_2_CLOTHING)

    # For fabrics
    for FABRIC in FABRIC_SETTINGS:
        FABRIC_1_CLOTHING = CURSOR.execute("""
            SELECT 
                Clothing_ID,
                Type
            FROM
                Clothing
            WHERE
                Fabric1 = ?
        ;""", [FABRIC]).fetchall()
        FABRIC_2_CLOTHING = CURSOR.execute("""
            SELECT
                Additional_Fabric_2.Clothing_ID,
                Clothing.Type
            FROM 
                Additional_Fabric_2
            JOIN
                Clothing
            ON
                Additional_Fabric_2.Clothing_ID = Clothing.Clothing_ID
            WHERE
                Additional_Fabric_2.Data = ?
        ;""", [FABRIC]).fetchall()
        POSSIBLE_CLOTHING_FABRIC = combineListsNoDuplicates(FABRIC_1_CLOTHING, FABRIC_2_CLOTHING)

    if WEATHER_SETTING != "" and WEATHER_SETTING is not None:
        # For weather
        POSSIBLE_CLOTHING_WEATHER = CURSOR.execute("""
            SELECT
                Clothing_ID,
                Type
            FROM
                Clothing
            WHERE
                Weather = ?
            OR
                Weather = Neutral
        ;""", [WEATHER_SETTING]).fetchall()
    else:
        POSSIBLE_CLOTHING_WEATHER = None

    # Get intersections of lists
    CLOTHING_COLOR_AND_STYLE = intersectionOfLists(POSSIBLE_CLOTHING_COLOR, POSSIBLE_CLOTHING_STYLE)
    CLOTHING_FABRIC_AND_WEATHER = intersectionOfLists(POSSIBLE_CLOTHING_FABRIC, POSSIBLE_CLOTHING_WEATHER)
    # Find clothing that meets settings
    QUALIFIED_CLOTHING = intersectionOfLists(CLOTHING_COLOR_AND_STYLE, CLOTHING_FABRIC_AND_WEATHER)

    # Separate clothing into their types

    # Initialize categories
    TOPS = []
    BOTTOMS = []
    SHOES = []
    SWEATERS = []
    JACKETS = []
    ACCESSORIES = []

    # Initialize mandatory and non-mandatory lists
    ESSENTIALS = []
    ACCESSORIES_COMBINATIONS = []
    NON_ESSENTIALS = []
    OUTFITS = []

    # Iterate over all clothing
    for ITEM in QUALIFIED_CLOTHING:
        # Find the type of clothing
        if ITEM[1] == "Top":
            TOPS.append(ITEM[0])
        elif ITEM[1] == "Bottom":
            BOTTOMS.append(ITEM[0])
        elif ITEM[1] == "Shoes":
            SHOES.append(ITEM[0])
        elif ITEM[1] == "Sweater":
            SWEATERS.append(ITEM[0])
        elif ITEM[1] == "Jacket":
            JACKETS.append(ITEM[0])
        elif ITEM[1] == "Accessory":
            ACCESSORIES.append(ITEM[0])

    # Get combinations

    # Find combinations of mandatory parts
    for TOP in TOPS:
        for BOTTOM in BOTTOMS:
            for SHOE in SHOES:
                ESSENTIALS.append([TOP, BOTTOM, SHOE])

    # Find combinations of accessories
    for COMBINATION_LENGTH in range(min(len(ACCESSORIES) + 1, 5)):  # combinations from 0 length to 5 length
        ACCESSORIES_COMBINATIONS.append(list(combinations(ACCESSORIES, COMBINATION_LENGTH)))

    # Find combinations of non-essentials
    for SWEATER in SWEATERS:
        for JACKET in JACKETS:
            for ACCESSORIES_COMBINATION in ACCESSORIES_COMBINATIONS:
                NON_ESSENTIALS.append([SWEATER, JACKET, ACCESSORIES_COMBINATION])

    # Find combinations of essentials and non-essentials
    for ESSENTIALS_COMBINATION in ESSENTIALS:
        for NON_ESSENTIALS_COMBINATION in NON_ESSENTIALS:
            NEW_OUTFIT = [ESSENTIALS_COMBINATION[0], ESSENTIALS_COMBINATION[1], ESSENTIALS_COMBINATION[2],
                          NON_ESSENTIALS_COMBINATION[0], NON_ESSENTIALS_COMBINATION[1], NON_ESSENTIALS_COMBINATION[2]]
            OUTFITS.append(NEW_OUTFIT)

    # Sort outfits

    # Auto-generate outfit score based on rating of individual clothing
    for i in range(len(OUTFITS)):
        # Initialize summing variables
        SUM = 0
        NUMBER_OF_ITEMS = 0
        for j in range(len(OUTFITS[i])):
            # Treat accessories differently
            if j == 5:
                for ACCESSORY in OUTFITS[i][j]:
                    # Find rating
                    ACCESSORY_RATING = CURSOR.execute("""
                    SELECT
                        Score
                    FROM
                        Clothing
                    WHERE
                        Clothing_ID = ?
                    ;""", [ACCESSORY]).fetchone()
                    SUM += ACCESSORY_RATING
                    NUMBER_OF_ITEMS += 1
            else:  # everything but accessories
                # Find rating
                CLOTHING_RATING = CURSOR.execute("""
                SELECT
                    Score
                FROM
                    Clothing
                WHERE
                    CLOTHING_ID = ?
                ;""", [OUTFITS[j]]).fetchone()
                SUM += CLOTHING_RATING
                NUMBER_OF_ITEMS += 1

        # Find average sum
        AVERAGE_SUM = SUM/NUMBER_OF_ITEMS

        # Add to outfit list, make score on 100 scale
        OUTFITS[i] = [OUTFITS[i], AVERAGE_SUM * 10]
    # Sort list
    OUTFITS.sort(key=getScore, reverse=True)
    return OUTFITS


def editOutfit(OUTFIT_PRIMARY_KEY, NEW_OUTFIT_INFORMATION):
    """
    Edit existing outfits with new information
    :param OUTFIT_PRIMARY_KEY: int
    :param NEW_OUTFIT_INFORMATION: list
    :return: none
    """
    global CURSOR, CONNECTION, OPTIONAL_OUTFIT_DATA

    FILLED_INFORMATION = [
        NEW_OUTFIT_INFORMATION[0],
        NEW_OUTFIT_INFORMATION[1],
        NEW_OUTFIT_INFORMATION[2],
        NEW_OUTFIT_INFORMATION[3],
        NEW_OUTFIT_INFORMATION[7],
        NEW_OUTFIT_INFORMATION[8],
        OUTFIT_PRIMARY_KEY
    ]

    # Find optional information: [sweater, jacket, accessories]
    OPTIONAL_INFORMATION = [
        NEW_OUTFIT_INFORMATION[4],
        NEW_OUTFIT_INFORMATION[5],
    ]

    # For accessories to be on one line
    for ACCESSORY in NEW_OUTFIT_INFORMATION[6]:
        if not (ACCESSORY is None or ACCESSORY == "" or ACCESSORY == 0):
            OPTIONAL_INFORMATION.append(ACCESSORY)
        else:
            # Make them none as placeholder
            OPTIONAL_INFORMATION.append(None)

    # Find existing information
    EXISTING_FILLED_INFORMATION, EXISTING_OPTIONAL_INFORMATION = getExistingOutfitInfo(OUTFIT_PRIMARY_KEY)

    # Replace filled information with existing information
    for i in range(len(FILLED_INFORMATION)):
        if i != 6 and (FILLED_INFORMATION[i] == 0 or FILLED_INFORMATION[i] is None or FILLED_INFORMATION[i] == ""):
            FILLED_INFORMATION[i] = EXISTING_FILLED_INFORMATION[i]

    # Main table
    CURSOR.execute("""
    UPDATE
        Outfits
    SET 
        Name = ?,
        Rating = ?,
        Top = ?,
        Bottom = ?,
        Shoes = ?,
        Comment = ?
    WHERE
        Outfit_ID = ?
    ;""", FILLED_INFORMATION)

    # Side tables
    # Update other tables
    for i in range(len(OPTIONAL_OUTFIT_DATA)):
        if OPTIONAL_INFORMATION[i] is not None and OPTIONAL_INFORMATION[i] != "" and OPTIONAL_INFORMATION[i] != 0:
            # columns exist
            if EXISTING_OPTIONAL_INFORMATION[i] is not None:
                # Regular update
                CURSOR.execute(f"""
                    UPDATE
                        {OPTIONAL_OUTFIT_DATA[i]}
                    SET
                        Clothing_ID = ?
                    WHERE
                        Outfit_ID = ?
                    ;""", [OPTIONAL_INFORMATION[i], OUTFIT_PRIMARY_KEY])
            else:  # columns do not exist
                # Have to insert
                CURSOR.execute(f"""
                    INSERT INTO
                        {OPTIONAL_OUTFIT_DATA[i]}
                    VALUES (
                        ?, ?
                    )
                    ;""", [OUTFIT_PRIMARY_KEY, OPTIONAL_INFORMATION[i]])
        else:  # no information provided for extra fields
            # columns exist
            if EXISTING_OPTIONAL_INFORMATION[i] is not None:
                CURSOR.execute(f"""
                    DELETE FROM
                        {OPTIONAL_OUTFIT_DATA[i]}
                    WHERE
                        Outfit_ID = ?
                    ;""", [OUTFIT_PRIMARY_KEY])
            # else, nothing happens
    CONNECTION.commit()


# Output
# --- VARIABLES --- #
FIRST_RUN = True
DATABASE_NAME = "Fashion.db"

if (pathlib.Path.cwd() / DATABASE_NAME).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_NAME)
CURSOR = CONNECTION.cursor()

# Additional information tables
OPTIONAL_CLOTHING_DATA = ("Additional_Color_2", "Additional_Color_3",
                          "Additional_Style_2", "Additional_Fabric_2")

OPTIONAL_OUTFIT_DATA = ("Additional_Sweater", "Additional_Jacket", "Additional_Accessory_1",
                        "Additional_Accessory_2", "Additional_Accessory_3",
                        "Additional_Accessory_4", "Additional_Accessory_5")
# --- MAIN PROGRAM CODE --- #
if __name__ == "__main__":
    if FIRST_RUN:  # create tables
        setup()
    # insertNewClothing(inputNewClothing())
    # updateClothing(1001, inputNewClothing())
    # deleteClothing(1001)
    # insertOutfit(inputOutfit())
    # deleteOutfit(1000)
    editOutfit(1000, inputOutfit())
