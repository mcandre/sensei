#!/usr/bin/env python

# sensei
# Andrew Pennebaker
# 3 March 2012

import SimpleCV
import random
import sys
import os
import time

english = {
  "kao": "face",
  "me": "eyes",
  "hana": "nose"
  }

def main():
  camera = SimpleCV.Camera()

  d = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep

  haarHand = d + "haar-hand.xml"

  lessons = [
    "kao", # face
    "me", # eyes
    "hana" #nose
    ]

  lesson = random.choice(lessons)

  haar = d + "haar-" + english[lesson] + ".xml"

  image = camera.getImage()
  w, h = image.size()

  kaoPos = [w-100, 100]
  mePos = [w-100, h/2]
  hanaPos = [w-100, h-100]
  resultPos = [100, h-100]
  nextLessonPos = [100, 100]

  defaultColor = SimpleCV.Color.GREEN
  selectColor = SimpleCV.Color.BLUE
  resultColor = SimpleCV.Color.RED
  nextLessonColor = SimpleCV.Color.GREEN

  while True:
    image = camera.getImage()
    image = image.flipHorizontal()

    features = image.findHaarFeatures(haar)

    hands = image.findHaarFeatures(haarHand)

    colors = {
      "kao": defaultColor,
      "me": defaultColor,
      "hana": defaultColor,
      "nextlesson": nextLessonColor
      }

    result = ""

    try:
      features.draw(defaultColor)
      hand = hands[0]
      hand.draw(selectColor)

      if hand.distanceFrom((kaoPos[0], kaoPos[1])) < 100:
        colors["kao"] = selectColor
        if lesson == "kao":
          result = "hai"
        else:
          result = "ie"
      elif hand.distanceFrom((mePos[0], mePos[1])) < 100:
        colors["me"] = selectColor
        if lesson == "me":
          result = "hai"
        else:
          result = "ie"
      elif hand.distanceFrom((hanaPos[0], hanaPos[1])) < 100:
        colors["hana"] = selectColor
        if lesson == "hana":
          result = "hai"
        else:
          result = "ie"
      elif hand.distanceFrom((nextLessonPos[0], nextLessonPos[1])) < 100:
        colors["nextlesson"] = selectColor
        lesson = random.choice(lessons)
        haar = d + "haar-" + english[lesson] + ".xml"
    except:
      pass
    finally:
      image.drawText("kao", kaoPos[0], kaoPos[1], colors["kao"], 40)

      image.drawText("me", mePos[0], mePos[1], colors["me"], 40)

      image.drawText("hana", hanaPos[0], hanaPos[1], colors["hana"], 40)

      if result != "":
        image.drawText(result, resultPos[0], resultPos[1], resultColor, 40)

        image.drawText(">", nextLessonPos[0], nextLessonPos[1], colors["nextlesson"], 40)

        image.show()

        time.sleep(0.1)

if __name__=="__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass
