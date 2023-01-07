"""
Title: Website Portion
Date-Created: 2023-01-02
"""

# Import flask library
from flask import Flask, render_template, request, redirect
# Import file explorer library
from pathlib import Path
# Import algorithms from other files
import algorithms

# FLASK #
app = Flask(__name__)

# GLOBAL VARIABLES #
DATABASE_NAME = "Fashion.db"
FIRST_RUN = True

if (Path.cwd() / DATABASE_NAME).exists():
    FIRST_RUN = False


# SUBROUTINES
@app.route('/', methods=["GET", "POST"])  # the application immediately routes to the index page
def clothing():
    # clothing page
    global COLORS, STYLES, FABRICS, WEATHER, CLOTHING_TYPES
    ALERT = ""
    if request.form:
        # get the info
        CLOTHING_NAME = request.form.get("clothing name")
        FIRST_COLOR = request.form.get("first color")
        SECOND_COLOR = request.form.get("second color")
        THIRD_COLOR = request.form.get("third color")
        COLOR_LIST = [FIRST_COLOR, SECOND_COLOR, THIRD_COLOR]
        FIRST_STYLE = request.form.get("first style")
        SECOND_STYLE = request.form.get("second style")
        STYLE_LIST = [FIRST_STYLE, SECOND_STYLE]
        FIRST_FABRIC = request.form.get("first fabric")
        SECOND_FABRIC = request.form.get("second fabric")
        FABRIC_LIST = [FIRST_FABRIC, SECOND_FABRIC]
        CLOTHING_WEATHER = request.form.get("weather")
        SCORE = int(request.form.get("clothing score"))
        IMAGE_LINK = request.form.get("image link")
        CLOTHING_TYPE = request.form.get("clothing type")

        # Check required fields
        if FIRST_COLOR == "None":
            ALERT = "Please fill in the required field: First Color"
        elif FIRST_STYLE == "None":
            ALERT = "Please fill in the required field: First Style"
        elif FIRST_FABRIC == "None":
            ALERT = "Please fill in the required field: First Fabric"
        elif CLOTHING_WEATHER == "None":
            ALERT = "Please fill in the required field: Weather"
        elif CLOTHING_TYPE == "None":
            ALERT = "Please fill in the required field: Clothing Type"
        else:
            # Format information
            CLOTHING_INFORMATION = [CLOTHING_NAME, COLOR_LIST, STYLE_LIST, FABRIC_LIST,
                                    CLOTHING_WEATHER, SCORE, IMAGE_LINK, CLOTHING_TYPE]
            CLOTHING_INFORMATION = algorithms.formatClothingInput(CLOTHING_INFORMATION)

            # Insert into table
            algorithms.insertNewClothing(CLOTHING_INFORMATION)

            # Inform user
            ALERT = f"Successfully inserted {CLOTHING_NAME.lower()} into the database!"
    return render_template("clothing.html", clothes=algorithms.getAllClothes(), colors=COLORS, styles=STYLES,
                           fabrics=FABRICS, weather=WEATHER, clothing_types=CLOTHING_TYPES, alert=ALERT)


@app.route('/edit/<ID>', methods=["GET", "POST"])
def editClothing(ID):  # to edit clothing
    # For dropdowns
    global COLORS, STYLES, FABRICS, WEATHER, CLOTHING_TYPES

    EXISTING_INFORMATION = algorithms.formatClothingInput(algorithms.getExistingClothingInfo(ID))
    ALERT = ""
    if request.form:
        # get the info
        CLOTHING_NAME = request.form.get("clothing name")
        FIRST_COLOR = request.form.get("first color")
        SECOND_COLOR = request.form.get("second color")
        THIRD_COLOR = request.form.get("third color")
        COLOR_LIST = [FIRST_COLOR, SECOND_COLOR, THIRD_COLOR]
        FIRST_STYLE = request.form.get("first style")
        SECOND_STYLE = request.form.get("second style")
        STYLE_LIST = [FIRST_STYLE, SECOND_STYLE]
        FIRST_FABRIC = request.form.get("first fabric")
        SECOND_FABRIC = request.form.get("second fabric")
        FABRIC_LIST = [FIRST_FABRIC, SECOND_FABRIC]
        CLOTHING_WEATHER = request.form.get("weather")
        SCORE = int(request.form.get("clothing score"))
        IMAGE_LINK = request.form.get("image link")
        CLOTHING_TYPE = request.form.get("clothing type")

        # Check required fields
        if FIRST_COLOR == "None":
            ALERT = "Please fill in the required field: First Color"
        elif FIRST_STYLE == "None":
            ALERT = "Please fill in the required field: First Style"
        elif FIRST_FABRIC == "None":
            ALERT = "Please fill in the required field: First Fabric"
        elif CLOTHING_WEATHER == "None":
            ALERT = "Please fill in the required field: Weather"
        elif CLOTHING_TYPE == "None":
            ALERT = "Please fill in the required field: Clothing Type"
        else:
            # Format information
            CLOTHING_INFORMATION = [CLOTHING_NAME, COLOR_LIST, STYLE_LIST, FABRIC_LIST,
                                    CLOTHING_WEATHER, SCORE, IMAGE_LINK, CLOTHING_TYPE]
            CLOTHING_INFORMATION = algorithms.formatClothingInput(CLOTHING_INFORMATION)

            # Insert into table
            algorithms.editClothing(ID, CLOTHING_INFORMATION)
            print(f"Successfully edited item #{ID}: {CLOTHING_NAME} in the database!")
            return redirect("/")
    return render_template("edit.html", existing_info=EXISTING_INFORMATION, colors=COLORS, styles=STYLES,
                           fabrics=FABRICS, weather=WEATHER, clothing_types=CLOTHING_TYPES, alert=ALERT)


def formatOutfits(OUTFITS):
    """
    Formats outfits to use on website
    :param OUTFITS: list
    :return: list
    """
    for i in range(len(OUTFITS)):
        for j in range(len(OUTFITS[i])):
            if OUTFITS[i][j] is not None:
                if type(OUTFITS[i][j]) == int:
                    if OUTFITS[i][j] >= 1000 and j != 0:  # Not a rating nor outfit id
                        # Replace with a tuple (id, name, image)
                        ID = OUTFITS[i][j]
                        CLOTHING_NAME_LINK = (ID, algorithms.getClothingWithID(ID), algorithms.getClothingImages(ID))
                        OUTFITS[i][j] = CLOTHING_NAME_LINK
                elif type(OUTFITS[i][j]) == list:  # if accessory list
                    for k in range(len(OUTFITS[i][j])):
                        if OUTFITS[i][j][k] is not None:
                            ID = OUTFITS[i][j][k]
                            CLOTHING_NAME_LINK = (ID, algorithms.getClothingWithID(ID),
                                                  algorithms.getClothingImages(ID))
                            OUTFITS[i][j][k] = CLOTHING_NAME_LINK
    return OUTFITS


@app.route("/outfits/")
def outfits():  # outfit page
    # Find images and names
    OUTFITS = algorithms.getAllOutfits()
    OUTFITS = formatOutfits(OUTFITS)
    return render_template("outfits.html", outfits=OUTFITS, original_outfit=algorithms.getAllOutfits())


def parseChosen(chosen_info):
    """
    For parsing the chosen info
    :param chosen_info: string
    :return: list
    """
    if type(chosen_info) == str:
        # remove first and last square brackets
        chosen_info = chosen_info.replace("[", "")
        chosen_info = chosen_info.replace("]", "")

        # Split
        chosen_info = chosen_info.split(", ")

        for i in range(len(chosen_info)):
            if chosen_info[i] == "None":
                chosen_info[i] = None
            # Get rid of quotations for names and comments
            if chosen_info[0] is not None:
                if chosen_info[0][0] == "'" or chosen_info[0][0] == '"':
                    chosen_info[0] = chosen_info[0][1:]
                if chosen_info[0][-1] == "'" or chosen_info[0][-1] == '"':
                    chosen_info[0] = chosen_info[0][:-1]
            if chosen_info[-2] is not None:
                if chosen_info[-2][0] == "'" or chosen_info[-2][0] == '"':
                    chosen_info[-2] = chosen_info[-2][1:]
                if chosen_info[-2][-1] == "'" or chosen_info[-2][-1] == '"':
                    chosen_info[-2] = chosen_info[-2][:-1]

        # Regroup accessory list
        ACCESSORIES = chosen_info[6:-2]

        chosen_info[6] = ACCESSORIES
        while len(chosen_info) > 9:
            chosen_info.pop(7)

    # Makes sure that the chosen clothing have a full length accessory list
    DISPLAY_CHOSEN = []
    # Duplicate
    i = 0
    for INFO in chosen_info:
        if type(INFO) == list:
            DISPLAY_CHOSEN.append([])
            for SUB_INFO in INFO:  # for the accessory list
                if SUB_INFO == "None" or SUB_INFO == "":
                    DISPLAY_CHOSEN[i].append(None)
                elif type(SUB_INFO) == str:
                    if SUB_INFO.isnumeric():
                        DISPLAY_CHOSEN[i].append(int(SUB_INFO))
                    else:
                        DISPLAY_CHOSEN[i].append(SUB_INFO)
                else:
                    DISPLAY_CHOSEN[i].append(SUB_INFO)
        elif INFO == "None" or INFO == "":
            DISPLAY_CHOSEN.append(None)
        elif type(INFO) == str:
            if INFO.isnumeric():
                DISPLAY_CHOSEN.append(int(INFO))
            else:
                DISPLAY_CHOSEN.append(INFO)
        else:
            DISPLAY_CHOSEN.append(INFO)
        i += 1

    # Fill accessory list
    while len(DISPLAY_CHOSEN[6]) < 5:
        DISPLAY_CHOSEN[6].append(None)

    return DISPLAY_CHOSEN


def parseChosenWithID(ID_and_chosen):
    """
    For parsing when there is an id as well
    :return:
    """
    # Parse
    # remove square brackets
    print("raw", ID_and_chosen)
    ID_and_chosen = ID_and_chosen.replace("[", "")
    ID_and_chosen = ID_and_chosen.replace("]", "")
    # split id and chosen
    ID_and_chosen = ID_and_chosen.split(", ")
    # find id
    ID = int(ID_and_chosen[0])
    # Get rid of first item (the id)
    ID_and_chosen.pop(0)
    # Make "None" into None
    for i in range(len(ID_and_chosen)):
        if ID_and_chosen[i] == "None":
            ID_and_chosen[i] = None
        # Get rid of quotations for names and comments
        if ID_and_chosen[0] is not None:
            if ID_and_chosen[0][0] == "'" or ID_and_chosen[0][0] == '"':
                ID_and_chosen[0] = ID_and_chosen[0][1:]
            if ID_and_chosen[0][-1] == "'" or ID_and_chosen[0][-1] == '"':
                ID_and_chosen[0] = ID_and_chosen[0][:-1]
        if ID_and_chosen[-2] is not None:
            if ID_and_chosen[-2][0] == "'" or ID_and_chosen[-2][0] == '"':
                ID_and_chosen[-2] = ID_and_chosen[-2][1:]
            if ID_and_chosen[-2][-1] == "'" or ID_and_chosen[-2][-1] == '"':
                ID_and_chosen[-2] = ID_and_chosen[-2][:-1]

    # Regroup accessory list
    ACCESSORIES = ID_and_chosen[6:-2]

    ID_and_chosen[6] = ACCESSORIES
    while len(ID_and_chosen) > 9:
        ID_and_chosen.pop(7)

    OUTFIT_CHOSEN_CLOTHES = []

    i = 0
    for INFO in ID_and_chosen:
        if type(INFO) == list:
            OUTFIT_CHOSEN_CLOTHES.append([])
            for SUB_INFO in INFO:  # for the accessory list
                if SUB_INFO == "None" or SUB_INFO == "":
                    OUTFIT_CHOSEN_CLOTHES[i].append(None)
                elif type(SUB_INFO) == str:
                    if SUB_INFO.isnumeric():
                        OUTFIT_CHOSEN_CLOTHES[i].append(int(SUB_INFO))
                    else:
                        OUTFIT_CHOSEN_CLOTHES[i].append(SUB_INFO)
                else:
                    OUTFIT_CHOSEN_CLOTHES[i].append(SUB_INFO)
        elif INFO == "[]":
            OUTFIT_CHOSEN_CLOTHES.append([])
        elif INFO == "None" or INFO == "":
            OUTFIT_CHOSEN_CLOTHES.append(None)
        elif type(INFO) == str:
            if INFO.isnumeric():
                OUTFIT_CHOSEN_CLOTHES.append(int(INFO))
            else:
                OUTFIT_CHOSEN_CLOTHES.append(INFO)
        else:
            OUTFIT_CHOSEN_CLOTHES.append(INFO)
        i += 1
    return ID, OUTFIT_CHOSEN_CLOTHES


@app.route("/addOutfits/<chosen_info>", methods=["GET", "POST"])
def addOutfits(chosen_info):  # outfit page
    # parse chosen_info
    DISPLAY_CHOSEN = parseChosen(chosen_info)

    ALERT = ""
    if request.form:
        # get the info
        OUTFIT_NAME = request.form.get("outfit name")
        TOP = request.form.get("top id")
        if TOP.isnumeric():  # Ensures typecasting
            TOP = int(TOP)
        else:
            ALERT = "Please fill in the required field: Top"
        BOTTOM = request.form.get("bottom id")
        if BOTTOM.isnumeric():  # Ensures typecasting
            BOTTOM = int(BOTTOM)
        else:
            ALERT = "Please fill in the required field: Bottom"
        SHOES = request.form.get("shoes id")
        if SHOES.isnumeric():  # Ensures typecasting
            SHOES = int(SHOES)
        else:
            ALERT = "Please fill in the required field: Shoes"

        if ALERT != "":
            return render_template("add_outfit.html", alert=ALERT, chosen=DISPLAY_CHOSEN,
                                   clothes=algorithms.getAllClothes())

        SWEATER = request.form.get("sweater id")
        if SWEATER.isnumeric():
            SWEATER = int(SWEATER)
        JACKET = request.form.get("jacket id")
        if JACKET.isnumeric():
            JACKET = int(JACKET)
        ACCESSORY_1 = request.form.get("accessory 1 id")
        if ACCESSORY_1.isnumeric():
            ACCESSORY_1 = int(ACCESSORY_1)
        ACCESSORY_2 = request.form.get("accessory 2 id")
        if ACCESSORY_2.isnumeric():
            ACCESSORY_2 = int(ACCESSORY_2)
        ACCESSORY_3 = request.form.get("accessory 3 id")
        if ACCESSORY_3.isnumeric():
            ACCESSORY_3 = int(ACCESSORY_3)
        ACCESSORY_4 = request.form.get("accessory 4 id")
        if ACCESSORY_4.isnumeric():
            ACCESSORY_4 = int(ACCESSORY_4)
        ACCESSORY_5 = request.form.get("accessory 5 id")
        if ACCESSORY_5.isnumeric():
            ACCESSORY_5 = int(ACCESSORY_5)
        COMMENT = request.form.get("comment")
        RATING = int(request.form.get("rating"))

        # Make list for accessories
        ACCESSORY_LIST = []

        if not (ACCESSORY_1 is None or ACCESSORY_1 == "" or ACCESSORY_1 == 0):
            ACCESSORY_LIST.append(ACCESSORY_1)
        if not (ACCESSORY_2 is None or ACCESSORY_2 == "" or ACCESSORY_2 == 0):
            ACCESSORY_LIST.append(ACCESSORY_2)
        if not (ACCESSORY_3 is None or ACCESSORY_3 == "" or ACCESSORY_3 == 0):
            ACCESSORY_LIST.append(ACCESSORY_3)
        if not (ACCESSORY_4 is None or ACCESSORY_4 == "" or ACCESSORY_4 == 0):
            ACCESSORY_LIST.append(ACCESSORY_4)
        if not (ACCESSORY_5 is None or ACCESSORY_5 == "" or ACCESSORY_5 == 0):
            ACCESSORY_LIST.append(ACCESSORY_5)
        ACCESSORY_LIST.sort()

        # Make accessory list length of 5
        while len(ACCESSORY_LIST) < 5:
            ACCESSORY_LIST.append(None)

        OUTFIT = [OUTFIT_NAME, TOP, BOTTOM, SHOES, SWEATER, JACKET, ACCESSORY_LIST, COMMENT, RATING]

        # Add into database
        algorithms.insertOutfit(OUTFIT)
        return redirect("/outfits/")
    return render_template("add_outfit.html", alert=ALERT, chosen=DISPLAY_CHOSEN, clothes=algorithms.getAllClothes())


@app.route("/addToItem/<ID_and_chosen>")
def addItemToOutfit(ID_and_chosen):  # add item to clothing
    ID, OUTFIT_CHOSEN_CLOTHES = parseChosenWithID(ID_and_chosen)

    # Find type of item
    ITEM_TYPE = algorithms.getExistingClothingInfo(ID)[8]
    # Add into table
    if ITEM_TYPE == "Top":
        OUTFIT_CHOSEN_CLOTHES[1] = ID
    if ITEM_TYPE == "Bottom":
        OUTFIT_CHOSEN_CLOTHES[2] = ID
    if ITEM_TYPE == "Shoes":
        OUTFIT_CHOSEN_CLOTHES[3] = ID
    if ITEM_TYPE == "Sweater":
        OUTFIT_CHOSEN_CLOTHES[4] = ID
    if ITEM_TYPE == "Jacket":
        OUTFIT_CHOSEN_CLOTHES[5] = ID
    if ITEM_TYPE == "Accessory":  # only have at most 5 accessories
        ALREADY_ADDED = False
        for ACCESSORY in OUTFIT_CHOSEN_CLOTHES[6]:
            if ID == ACCESSORY:  # can only add one of one id into the outfit
                ALREADY_ADDED = True
                break
        if not ALREADY_ADDED:
            for i in range(len(OUTFIT_CHOSEN_CLOTHES[6])):  # make nones hold accessory
                if OUTFIT_CHOSEN_CLOTHES[6][i] is None:
                    OUTFIT_CHOSEN_CLOTHES[6][i] = ID
                    break
                elif i == 4:
                    OUTFIT_CHOSEN_CLOTHES[6][4] = ID  # Will always get added
    return redirect(f"/addOutfits/{OUTFIT_CHOSEN_CLOTHES}")


@app.route("/deleteFromOutfit/<ID_and_chosen>")
def deleteItemFromOutfit(ID_and_chosen):  # add item to clothing
    ID, OUTFIT_CHOSEN_CLOTHES = parseChosenWithID(ID_and_chosen)

    # Find type of item
    ITEM_TYPE = algorithms.getExistingClothingInfo(ID)[8]
    # Add into table
    if ITEM_TYPE == "Top":
        OUTFIT_CHOSEN_CLOTHES[1] = None
    if ITEM_TYPE == "Bottom":
        OUTFIT_CHOSEN_CLOTHES[2] = None
    if ITEM_TYPE == "Shoes":
        OUTFIT_CHOSEN_CLOTHES[3] = None
    if ITEM_TYPE == "Sweater":
        OUTFIT_CHOSEN_CLOTHES[4] = None
    if ITEM_TYPE == "Jacket":
        OUTFIT_CHOSEN_CLOTHES[5] = None
    if ITEM_TYPE == "Accessory":  # only have at most 5 accessories
        for i in range(len(OUTFIT_CHOSEN_CLOTHES[6])):  # make nones hold accessory
            if OUTFIT_CHOSEN_CLOTHES[6][i] == ID:
                OUTFIT_CHOSEN_CLOTHES[6][i] = None
    return redirect(f"/addOutfits/{OUTFIT_CHOSEN_CLOTHES}")


@app.route("/delete/<ID>")
def deleteClothing(ID):  # to delete clothing
    CLOTHING_NAME = algorithms.getClothingWithID(ID)
    algorithms.deleteClothing(ID)
    print(f"Successfully deleted item #{ID}: {CLOTHING_NAME} from the database!")
    return redirect("/")


@app.route("/deleteOutfit/<ID>")
def deleteOutfit(ID):  # to delete clothing
    OUTFIT_NAME = algorithms.getOutfitWithID(ID)
    algorithms.deleteOutfit(ID)
    print(f"Successfully deleted outfit #{ID}: {OUTFIT_NAME} from the database!")
    return redirect("/outfits/")


@app.route("/editOutfit/<chosen_info>", methods=["GET", "POST"])
def editOutfit(chosen_info):  # outfit page
    # parse chosen_info
    ID, DISPLAY_CHOSEN = parseChosenWithID(chosen_info)

    ALERT = ""
    if request.form:
        # get the info
        OUTFIT_NAME = request.form.get("outfit name")
        TOP = request.form.get("top id")
        if TOP.isnumeric():  # Ensures typecasting
            TOP = int(TOP)
        else:  # alert user
            ALERT = "Please fill in the required field: Top"
        BOTTOM = request.form.get("bottom id")
        if BOTTOM.isnumeric():  # Ensures typecasting
            BOTTOM = int(BOTTOM)
        else:
            ALERT = "Please fill in the required field: Bottom"
        SHOES = request.form.get("shoes id")
        if SHOES.isnumeric():  # Ensures typecasting
            SHOES = int(SHOES)
        else:
            ALERT = "Please fill in the required field: Shoes"

        if ALERT != "":
            return render_template("edit_outfit.html", alert=ALERT, chosen=DISPLAY_CHOSEN,
                                   clothes=algorithms.getAllClothes())

        SWEATER = request.form.get("sweater id")
        if SWEATER.isnumeric():
            SWEATER = int(SWEATER)
        JACKET = request.form.get("jacket id")
        if JACKET.isnumeric():
            JACKET = int(JACKET)
        ACCESSORY_1 = request.form.get("accessory 1 id")
        if ACCESSORY_1.isnumeric():
            ACCESSORY_1 = int(ACCESSORY_1)
        ACCESSORY_2 = request.form.get("accessory 2 id")
        if ACCESSORY_2.isnumeric():
            ACCESSORY_2 = int(ACCESSORY_2)
        ACCESSORY_3 = request.form.get("accessory 3 id")
        if ACCESSORY_3.isnumeric():
            ACCESSORY_3 = int(ACCESSORY_3)
        ACCESSORY_4 = request.form.get("accessory 4 id")
        if ACCESSORY_4.isnumeric():
            ACCESSORY_4 = int(ACCESSORY_4)
        ACCESSORY_5 = request.form.get("accessory 5 id")
        if ACCESSORY_5.isnumeric():
            ACCESSORY_5 = int(ACCESSORY_5)
        COMMENT = request.form.get("comment")
        RATING = int(request.form.get("rating"))

        # Make list for accessories
        ACCESSORY_LIST = []

        if not (ACCESSORY_1 is None or ACCESSORY_1 == "" or ACCESSORY_1 == 0):
            ACCESSORY_LIST.append(ACCESSORY_1)
        if not (ACCESSORY_2 is None or ACCESSORY_2 == "" or ACCESSORY_2 == 0):
            ACCESSORY_LIST.append(ACCESSORY_2)
        if not (ACCESSORY_3 is None or ACCESSORY_3 == "" or ACCESSORY_3 == 0):
            ACCESSORY_LIST.append(ACCESSORY_3)
        if not (ACCESSORY_4 is None or ACCESSORY_4 == "" or ACCESSORY_4 == 0):
            ACCESSORY_LIST.append(ACCESSORY_4)
        if not (ACCESSORY_5 is None or ACCESSORY_5 == "" or ACCESSORY_5 == 0):
            ACCESSORY_LIST.append(ACCESSORY_5)
        ACCESSORY_LIST.sort()

        # Make Accessory List length of 5
        while len(ACCESSORY_LIST) < 5:
            ACCESSORY_LIST.append(None)

        OUTFIT = [OUTFIT_NAME, TOP, BOTTOM, SHOES, SWEATER, JACKET, ACCESSORY_LIST, COMMENT, RATING]
        print(OUTFIT)
        # Add into database
        algorithms.editOutfit(ID, OUTFIT)
        return redirect("/outfits/")
    return render_template("edit_outfit.html", alert=ALERT, chosen=DISPLAY_CHOSEN, clothes=algorithms.getAllClothes(),
                           outfit_id=ID)


@app.route("/addToEditItem/<ID_and_chosen>")
def addItemToEditOutfit(ID_and_chosen):  # add item to clothing
    # Find the outfit ID
    ID_and_chosen = ID_and_chosen.split(", ")
    OUTFIT_ID = ID_and_chosen[0]
    OUTFIT_ID = OUTFIT_ID[1:]
    OUTFIT_ID = int(OUTFIT_ID)

    # format ID_and_chosen
    ID_and_chosen.pop(0)
    ID_and_chosen = ", ".join(ID_and_chosen)
    ID_and_chosen = f"[{ID_and_chosen}"

    ID, OUTFIT_CHOSEN_CLOTHES = parseChosenWithID(ID_and_chosen)

    # Find type of item
    ITEM_TYPE = algorithms.getExistingClothingInfo(ID)[8]
    # Add into table
    if ITEM_TYPE == "Top":
        OUTFIT_CHOSEN_CLOTHES[1] = ID
    if ITEM_TYPE == "Bottom":
        OUTFIT_CHOSEN_CLOTHES[2] = ID
    if ITEM_TYPE == "Shoes":
        OUTFIT_CHOSEN_CLOTHES[3] = ID
    if ITEM_TYPE == "Sweater":
        OUTFIT_CHOSEN_CLOTHES[4] = ID
    if ITEM_TYPE == "Jacket":
        OUTFIT_CHOSEN_CLOTHES[5] = ID
    if ITEM_TYPE == "Accessory":  # only have at most 5 accessories
        ALREADY_ADDED = False
        for ACCESSORY in OUTFIT_CHOSEN_CLOTHES[6]:
            if ID == ACCESSORY:  # can only add one of one id into the outfit
                ALREADY_ADDED = True
                break
        if not ALREADY_ADDED:
            for i in range(len(OUTFIT_CHOSEN_CLOTHES[6])):  # make nones hold accessory
                if OUTFIT_CHOSEN_CLOTHES[6][i] is None:
                    OUTFIT_CHOSEN_CLOTHES[6][i] = ID
                    break
                elif i == 4:
                    OUTFIT_CHOSEN_CLOTHES[6][4] = ID  # Will always get added
    return redirect(f"/editOutfit/{[OUTFIT_ID] + OUTFIT_CHOSEN_CLOTHES}")


@app.route("/generate_outfit", methods=["GET", "POST"])
def generateOutfits():
    # initialize tables
    OUTFITS = None
    ORIGINAL_OUTFITS = None
    ALERT = ""
    if request.form:
        # get the info
        FIRST_COLOR = request.form.get("first color")
        if FIRST_COLOR == "None":  # makes the none into a none type none
            FIRST_COLOR = None
        SECOND_COLOR = request.form.get("second color")
        if SECOND_COLOR == "None":
            SECOND_COLOR = None
        THIRD_COLOR = request.form.get("third color")
        if THIRD_COLOR == "None":
            THIRD_COLOR = None
        FIRST_STYLE = request.form.get("first style")
        if FIRST_STYLE == "None":
            FIRST_STYLE = None
        SECOND_STYLE = request.form.get("second style")
        if SECOND_STYLE == "None":
            SECOND_STYLE = None
        FIRST_FABRIC = request.form.get("first fabric")
        if FIRST_FABRIC == "None":
            FIRST_FABRIC = None
        SECOND_FABRIC = request.form.get("second fabric")
        if SECOND_FABRIC == "None":
            SECOND_FABRIC = None
        CLOTHING_WEATHER = request.form.get("weather")
        if CLOTHING_WEATHER == "None":
            CLOTHING_WEATHER = None

        # Generate the outfits
        GENERATING_PARAMETERS = [FIRST_COLOR, SECOND_COLOR, THIRD_COLOR, FIRST_STYLE, SECOND_STYLE, FIRST_FABRIC,
                                 SECOND_FABRIC, CLOTHING_WEATHER]
        OUTFITS = algorithms.generateOutfit(GENERATING_PARAMETERS)
        if OUTFITS is not None:
            OUTFITS=formatOutfits(OUTFITS)
        ORIGINAL_OUTFITS = algorithms.generateOutfit(GENERATING_PARAMETERS)
        # See if no outfits were generated
        if len(OUTFITS) == 0:
            ALERT = "No outfits that met the parameters were generated. Try broadening the parameters."

    # Note: original outfit is so to make the add outfit link much easier to write out
    # original_outfit is linked with outfits
    return render_template("generate_outfit.html", original_outfits=ORIGINAL_OUTFITS, outfits=OUTFITS,
                           colors=COLORS, styles=STYLES, fabrics=FABRICS, weather=WEATHER, alert=ALERT)


# For dropdowns
COLORS = ("None", "Red", "Orange", "Yellow", "Gold", "Green", "Turquoise", "Blue", "Indigo", "Violet", "Magenta",
          "Pink", "Beige", "Brown", "White", "Gray", "Silver", "Black")
STYLES = ("None", 'Basic', 'Business Casual', 'Casual', 'Cultural', 'Chic', 'Cosplay', 'Cute', 'Formal', 'Girly',
          'Goth', 'Loser', 'Old-Fashioned', 'Party', 'Preppy', 'Professional', 'Punk', 'Sportswear', 'Street wear')
FABRICS = ("None", 'Canvas', 'Chenille', 'Chiffon', 'Cotton', 'Crepe', 'Denim', 'Lace', 'Leather', 'Linen', 'Linen',
           'Nylon', 'Polyester', 'Satin', 'Silk', 'Spandex', 'Velvet', 'Wool')
WEATHER = ("None", "Hot", "Warm", "Neutral", "Cool", "Cold")
CLOTHING_TYPES = ("None", "Top", "Bottom", "Shoes", "Accessory", "Sweater", "Jacket")

# MAIN PROGRAM CODE #
if __name__ == "__main__":
    # Make the database
    if FIRST_RUN:
        algorithms.setup()

    # Run app
    app.run(debug=True)
