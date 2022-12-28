# algorithms.py
"""
Title: Algorithms for Fashion Program
Date: December 16, 2022
"""
# --- LIBRARIES --- #
import pathlib
import sqlite3
import flask


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

    # non empty information does not get deleted, will get updated
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


def generateOutfit(SETTINGS):
    """
    Generates outfit when given some settings
    :param SETTINGS: list [color1, color2, color3, style1, style2, fabric1, fabric2, weather]
    :return: 2d list
    """
    # Initialize arrays
    TOPS = []
    BOTTOMS = []
    SHOES = []
    SWEATERS = []
    JACKETS = []
    ACCESSORIES = []
    # For colors
    COLOR_SETTINGS = SETTINGS[0:3]
    for COLOR in COLOR_SETTINGS:
        POSSIBLE_CLOTHING = CURSOR.execute("""
            SELECT 
                CLOTHING_ID,
                TYPE
            FROM
                Clothing
            WHERE
                COLOR1 = ?
        ;""", [COLOR]).fetchall()


def getClothingInformation():
    pass


def getOutfitInformation():
    pass


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
