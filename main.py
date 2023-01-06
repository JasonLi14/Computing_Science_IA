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
            print(CLOTHING_INFORMATION)
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

    EXISTING_INFORMATION = algorithms.formatClothingInput(algorithms.getExistingClothingInfo(ID))  # find existing information
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
            print(CLOTHING_INFORMATION)
            CLOTHING_INFORMATION = algorithms.formatClothingInput(CLOTHING_INFORMATION)

            # Insert into table
            algorithms.editClothing(ID, CLOTHING_INFORMATION)
            print("Help")
            print(f"Successfully edited item #{ID}: {CLOTHING_NAME} in the database!")
            return redirect("/")
    return render_template("edit.html", existing_info = EXISTING_INFORMATION, colors=COLORS, styles=STYLES,
                           fabrics=FABRICS, weather=WEATHER, clothing_types=CLOTHING_TYPES, alert=ALERT)


@app.route("/outfits/")
def outfits():  # outfit page
    global OUTFIT_CHOSEN_CLOTHES
    ALERT = ""
    if request.form:
        # get the info
        OUTFIT_NAME = request.form.get("outfit name")
        TOP = request.form.get("top id")
        BOTTOM = request.form.get("bottom")

    return render_template("outfits.html", alert=ALERT, chosen=OUTFIT_CHOSEN_CLOTHES)


@app.route("/delete/<ID>")
def deleteClothing(ID):  # to delete clothing
    CLOTHING_NAME = algorithms.getClothingWithID(ID)
    algorithms.deleteClothing(ID)
    print(f"Successfully deleted item #{ID}: {CLOTHING_NAME} from the database!")
    return redirect("/")


# For dropdowns
COLORS = ("None", "Red", "Orange", "Yellow", "Gold", "Green", "Turquoise", "Blue", "Indigo", "Violet", "Magenta",
          "Pink", "Beige", "Brown", "White", "Gray", "Silver", "Black")
STYLES = ("None", 'Basic', 'Business Casual', 'Casual', 'Chic', 'Cosplay', 'Cute', 'Ethnic', 'Formal', 'Girly', 'Goth', 'Loser',
          'Old-Fashioned', 'Party', 'Preppy', 'Professional', 'Punk', 'Sportswear', 'Streetwear')
FABRICS = ("None", 'Canvas', 'Chenille', 'Chiffon', 'Cotton', 'Crepe', 'Denim', 'Lace', 'Leather', 'Linen', 'Linen',
           'Nylon', 'Polyester', 'Satin', 'Silk', 'Spandex', 'Velvet', 'Wool')
WEATHER = ("None", "Hot", "Warm", "Neutral", "Cool", "Cold")
CLOTHING_TYPES = ("None", "Top", "Bottom", "Shoes", "Accessory", "Sweater", "Jacket")

# For outfit creation
OUTFIT_CHOSEN_CLOTHES = []

# MAIN PROGRAM CODE #
if __name__ == "__main__":
    # Make the database
    if FIRST_RUN:
        algorithms.setup()

    # Run app
    app.run(debug=True)
