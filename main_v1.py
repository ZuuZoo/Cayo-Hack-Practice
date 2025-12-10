import cv2
import numpy as np
import os
import keyboard
from PIL import ImageGrab
from datetime import datetime

# Beállítások
SRC_W = 2560
SRC_H = 1440
TARGET_W = 1920
TARGET_H = 1080

CROP = (974, 324, 1486, 972)  # X1, Y1, X2, Y2
FOLDER = "pelda"
HOTKEY = "F8"

def take_screenshot_scaled_gray():
    """2560x1440 screenshot -> lekicsinyítés 1920x1080-ra -> grayscale."""
    img = ImageGrab.grab(bbox=(0, 0, SRC_W, SRC_H))
    img = img.resize((TARGET_W, TARGET_H), ImageGrab.Image.LANCZOS)
    img = img.convert("L")
    return np.array(img)

def crop_image(img):
    x1, y1, x2, y2 = CROP
    cropped_img = img[y1:y2, x1:x2]
    return img[y1:y2, x1:x2]

def mse(imgA, imgB):
    return np.mean((imgA.astype("float") - imgB.astype("float")) ** 2)

"""def find_best_match(cropped):
    best_file = None
    best_score = float("inf")

    for file in os.listdir(FOLDER):
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        template_path = os.path.join(FOLDER, file)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

        if template is None:
            continue

        template = cv2.resize(template, (cropped.shape[1], cropped.shape[0]))
        score = mse(cropped, template)

        print(f"[INFO] {file} MSE: {score:.2f}")

        if score < best_score:
            best_score = score
            best_file = file

    return best_file, best_score"""

def find_best_match(cropped):
    orb = cv2.ORB_create(nfeatures=1000)  # sok kulcspont → stabilabb eredmény
    kp1, des1 = orb.detectAndCompute(cropped, None)

    best_file = None
    best_matches = -1

    for file in os.listdir(FOLDER):
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        template_path = os.path.join(FOLDER, file)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

        if template is None:
            continue

        # átméretezés a cropped méretére
        template = cv2.resize(template, (cropped.shape[1], cropped.shape[0]))

        kp2, des2 = orb.detectAndCompute(template, None)
        if des2 is None:
            continue

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # rendezés minőség szerint (kisebb distance = jobb)
        matches = sorted(matches, key=lambda x: x.distance)

        # jó egyezések megszámolása → minél több a jó match, annál jobb
        good = [m for m in matches if m.distance < 40]
        good_count = len(good)

        print(f"[INFO] {file} jó egyezések: {good_count}")

        if good_count > best_matches:
            best_matches = good_count
            best_file = file

    return best_file, best_matches


def main():
    print("Nyomd meg az F8-at a screenshot készítéséhez és összehasonlításhoz!")

    while True:
        keyboard.wait(HOTKEY)
        print("\n[KÉSZÜL A KÉP] Screenshot...")

        screenshot = take_screenshot_scaled_gray()
        cropped = crop_image(screenshot)

        cv2.imwrite("cropped.png", cropped)

        print("[ÖSSZEHASONLÍTÁS] Képek vizsgálata...")
        best, score = find_best_match(cropped)

        if best:
            print(f"\n=== EREDMÉNY ===\nLegjobban hasonlít: {best}\nHasonlósági érték (MSE): {score:.2f}\n")
        else:
            print("Nem találtam hasonló képet.")

if __name__ == "__main__":
    main()
