#!/usr/bin/env python

# sensei
# Andrew Pennebaker
# 3 March 2012

import SimpleCV
import random
import sys
import os
import time

ENGLISH = {
    "kao": "face",
    "me": "eyes",
    "hana": "nose"
}


def main():
    camera = SimpleCV.Camera()

    d = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep

    haar_hand = d + "haar-hand.xml"

    lessons = [
        "kao",  # face
        "me",   # eyes
        "hana"  # nose
    ]

    lesson = random.choice(lessons)

    haar = d + "haar-" + ENGLISH[lesson] + ".xml"

    image = camera.getImage()
    w, h = image.size()

    kao_pos = [w - 100, 100]
    me_pos = [w - 100, h / 2]
    hana_pos = [w - 100, h - 100]
    result_pos = [100, h - 100]
    next_lesson_pos = [100, 100]

    default_color = SimpleCV.Color.GREEN
    select_color = SimpleCV.Color.BLUE
    result_color = SimpleCV.Color.RED
    next_lesson_color = SimpleCV.Color.GREEN

    while True:
        image = camera.getImage()
        image = image.flipHorizontal()

        features = image.findHaarFeatures(haar)

        hands = image.findHaarFeatures(haar_hand)

        colors = {
            "kao": default_color,
            "me": default_color,
            "hana": default_color,
            "nextlesson": next_lesson_color
        }

        result = ""

        try:
            features.draw(default_color)
            hand = hands[0]
            hand.draw(select_color)

            if hand.distanceFrom((kao_pos[0], kao_pos[1])) < 100:
                colors["kao"] = select_color
                if lesson == "kao":
                    result = "hai"
                else:
                    result = "ie"
            elif hand.distanceFrom((me_pos[0], me_pos[1])) < 100:
                colors["me"] = select_color
                if lesson == "me":
                    result = "hai"
                else:
                    result = "ie"
            elif hand.distanceFrom((hana_pos[0], hana_pos[1])) < 100:
                colors["hana"] = select_color
                if lesson == "hana":
                    result = "hai"
                else:
                    result = "ie"
            elif hand.distanceFrom(
                (next_lesson_pos[0], next_lesson_pos[1])
            ) < 100:
                colors["nextlesson"] = select_color
                lesson = random.choice(lessons)
                haar = d + "haar-" + ENGLISH[lesson] + ".xml"
        except:
            pass
        finally:
            image.drawText(
                "kao",
                kao_pos[0],
                kao_pos[1],
                colors["kao"],
                40
            )
            image.drawText(
                "me",
                me_pos[0],
                me_pos[1],
                colors["me"],
                40
            )
            image.drawText(
                "hana",
                hana_pos[0],
                hana_pos[1],
                colors["hana"],
                40
            )

            if result != "":
                image.drawText(
                    result,
                    result_pos[0],
                    result_pos[1],
                    result_color,
                    40
                )
                image.drawText(
                    ">",
                    next_lesson_pos[0],
                    next_lesson_pos[1],
                    colors["nextlesson"],
                    40
                )

                image.show()

                time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
