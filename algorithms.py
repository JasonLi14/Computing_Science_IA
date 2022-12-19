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
    CURSOR.execute("""
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
    SCORE = int(input("Score: "))
    IMAGE_LINK = input("Link: ")
    CLOTHING_TYPE = input("Type: ")

    # Format information
    CLOTHING_INFORMATION = [CLOTHING_NAME, COLOR_LIST, STYLE_LIST, FABRIC_LIST, SCORE, IMAGE_LINK, CLOTHING_TYPE]
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
        ORDER_BY
            Clothing_ID DESC
    """).fetchone()
    return RECENT_PRIMARY_KEY


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
        CLOTHING_INFORMATION[0],
        CLOTHING_INFORMATION[1][0],
        CLOTHING_INFORMATION[2][0],
        CLOTHING_INFORMATION[3][0],
        CLOTHING_INFORMATION[4],
        CLOTHING_INFORMATION[5],
        CLOTHING_INFORMATION[6],
        CLOTHING_INFORMATION[7]
    ]

    CURSOR.execute("""
    INSERT INTO 
        Clothing (
            Name, Color1, Style1, Fabric1, Weather, Score, Link, Type
        )
    VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?
    ) 
    ;""", NON_EMPTY_INFORMATION)

    # Get first clothing
    if not CLOTHING_INFORMATION[1][1] is None:
        CURSOR.execute("""
            INSERT INTO
                Additional_Color_2 
            VALUES
                ?, ?
        """, [CLOTHING_PRIMARY_KEY, CLOTHING_INFORMATION[1][1]])
    CONNECTION.commit()


def deleteClothing(Clothing_ID):
    """
    Deletes clothing
    :param Clothing_ID: integer
    :return: none
    """


def updateClothing(Clothing_ID, NEW_INFORMATION):
    """
    Updates clothing with new info
    :param Clothing_ID: integer
    :param NEW_INFORMATION: list
    :return: none
    """


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


def deleteOutfit(OUTFIT_ID):
    pass


# Output
# --- VARIABLES --- #
FIRST_RUN = True
DATABASE_NAME = "Fashion.db"

if (pathlib.Path.cwd() / DATABASE_NAME).exists():
    print("b")
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_NAME)
CURSOR = CONNECTION.cursor()

# --- MAIN PROGRAM CODE --- #
if __name__ == "__main__":
    if FIRST_RUN:  # create tables
        setup()
