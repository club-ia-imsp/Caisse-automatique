import cv2
import os

save_dir = os.path.join("data","image","train")

# Compter les images déjà existantes
existing_images = [
    f for f in os.listdir(save_dir)
    if f.startswith("image_") and f.endswith(".jpg")
]

count = len(existing_images)

# Caméra (externe puis interne)
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur de lecture de la caméra")
        break

    cv2.imshow("ESPACE ou 'c' pour capturer | ESC pour quitter", frame)

    k = cv2.waitKey(1)

    if k == 27:
        break

    elif k == 32 or k == ord('c'):
        count += 1
        filename = os.path.join(save_dir, f"image_{count}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Image sauvegardée : {filename}")

cap.release()
cv2.destroyAllWindows()
