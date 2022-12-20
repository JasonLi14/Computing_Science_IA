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
        Color TEXT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Color_3 (
        Clothing_ID INT PRIMARY KEY,
        Color TEXT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Style_2 (
        Clothing_ID INT PRIMARY KEY,
        Style TEXT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Fabric_2 (
        Clothing_ID INT PRIMARY KEY,
        Fabric TEXT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Outfits (
        Outfit_ID INT PRIMARY KEY,
        Name TEXT NOT NULL,
        Rating INT NOT NULL,
        Top INT NOT NULL,
        Bottom INT NOT NULL,
        Shoes INT NOT NULL,
        Comment INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Sweater (
        Outfit_ID INT PRIMARY KEY,
        Sweater INT NOT NULL
    )
    ;""")
    CURSOR.execute(f"""
    CREATE TABLE Additional_Jacket (
        Outfit_ID INT PRIMARY KEY,
        Jacket INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Accessory_1 (
        Outfit_ID INT PRIMARY KEY,
        Accessory INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Accessory_2 (
        Outfit_ID INT PRIMARY KEY,
        Accessory INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Accessory_3 (
        Outfit_ID INT PRIMARY KEY,
        Accessory INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Accessory_4 (
        Outfit_ID INT PRIMARY KEY,
        Accessory INT NOT NULL
    )
    ;""")
    CURSOR.execute("""
    CREATE TABLE Additional_Accessory_5 (
        Outfit_ID INT PRIMARY KEY,
        Accessory INT NOT NULL
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
    pass


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
    if RECENT_PRIMARY_KEY[0] is None:
        RECENT_PRIMARY_KEY[0] = 999  # all primary keys have 4 digits
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
    pass


def deleteClothing(CLOTHING_ID):
    """
    Deletes clothing
    :param CLOTHING_ID: integer
    :return: none
    """
    global CURSOR, CONNECTION

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


def updateClothing(CLOTHING_PRIMARY_KEY, NEW_INFORMATION):
    """
    Updates clothing with new info
    :param CLOTHING_PRIMARY_KEY: integer
    :param NEW_INFORMATION: list
    :return: none
    """
    global CURSOR, CONNECTION
    # Get information in main table
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



def createOutfit():
    pass


def generateOutfit():
    pass


def getClothingInformation():
    pass


def getOutfitInformation():
    pass


def editOutfit():
    pass


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

# --- MAIN PROGRAM CODE --- #
if __name__ == "__main__":
    if FIRST_RUN:  # create tables
        setup()
    insertNewClothing(inputNewClothing())
    # deleteClothing(1)
