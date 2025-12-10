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

SUBCROPS = {
    "s1": (383, 353, 851, 422),
    "s2": (383, 429, 851, 498),
    "s3": (383, 505, 851, 574),
    "s4": (383, 581, 851, 650),
    "s5": (383, 657, 851, 726),
    "s6": (383, 733, 851, 802),
    "s7": (383, 809, 851, 878),
    "s8": (383, 885, 851, 954)
}

def take_screenshot_scaled_gray():
    img = ImageGrab.grab(bbox=(0, 0, SRC_W, SRC_H))
    img = img.resize((TARGET_W, TARGET_H), ImageGrab.Image.LANCZOS)
    img = img.convert("L")
    return np.array(img)

def crop_image(img):
    x1, y1, x2, y2 = CROP
    return img[y1:y2, x1:x2]

def crop_sub(img, coords):
    x1, y1, x2, y2 = coords
    return img[y1:y2, x1:x2]

def mse(imgA, imgB):
    return np.mean((imgA.astype("float") - imgB.astype("float")) ** 2)

def find_best_match(cropped, folder):
    best_file = None
    best_score = float("inf")

    for file in os.listdir(folder):
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        path = os.path.join(folder, file)
        template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            continue

        template = cv2.resize(template, (cropped.shape[1], cropped.shape[0]))
        score = mse(cropped, template)

        print(f"[INFO] {file} MSE: {score:.2f}")

        if score < best_score:
            best_score = score
            best_file = file

    return best_file, best_score


def main():
    print("F8 = screenshot + automatikus összehasonlítás")

    while True:
        keyboard.wait(HOTKEY)
        print("\n[KÉSZÜL A KÉP] Screenshot...")

        screenshot = take_screenshot_scaled_gray()
        cropped_main = crop_image(screenshot)

        # 1) Pelda fő kiválasztása
        print("\n[1] Fő kategória keresése (peldaX.png)...")
        best, score = find_best_match(cropped_main, FOLDER)

        if not best:
            print("Nem találtam hasonló pelda képet.")
            continue

        print(f"\n=== FŐ TALÁLAT ===\nLegjobban hasonlít: {best}")

        # például best = "pelda1.png" → pelda1 mappa
        folder_name = os.path.splitext(best)[0]  # pelda1
        subfolder = os.path.join(FOLDER, folder_name)

        if not os.path.isdir(subfolder):
            print(f"HIBA: {subfolder} mappa nem létezik!")
            continue

        print(f"\n[2] Belépés mappába: {subfolder}")

        # 2) S1 → S8 összehasonlítás
        for s_key, coords in SUBCROPS.items():
            print(f"\n--- {s_key} vizsgálata ---")

            sub_crop = crop_sub(screenshot, coords)
            best_s, score_s = find_best_match(sub_crop, subfolder)

            if best_s:
                print(f"{s_key} legjobb egyezése: {best_s} (MSE: {score_s:.2f})")
            else:
                print(f"{s_key}: nincs találat.")

if __name__ == "__main__":
    main()
