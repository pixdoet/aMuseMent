"""
clean.py - removes files from ./saves directory
"""

import time
import shutil


def wipe_all():
    userAffirmation = input(
        "Are you sure you want to remove ALL files from ./saves? [yes/no]: "
    )

    affirmationSafety = userAffirmation.lower()

    if affirmationSafety == "yes":
        print("WARNING: REMOVING ALL FILES FROM THE SAVES DIRECTORY!")
        print(
            "If you decide to not do so, you have five seconds to press Control-C to cancel."
        )
        i = 0
        for i in range(5, 0, -1):
            print(i)
            time.sleep(1)
        shutil.rmtree("./saves")
        print("All files from ./saves removed!")

    elif affirmationSafety == "no":
        print("Operation cancelled")

    else:
        print("Invalid input! [yes/no]")
