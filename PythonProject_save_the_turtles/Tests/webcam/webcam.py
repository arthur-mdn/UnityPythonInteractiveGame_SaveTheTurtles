import cv2
webcam_backend = cv2.CAP_DSHOW # cv2.CAP_DSHOW pour les webcams Windows, Utilisez cv2.CAP_ANY si vous rencontrez des problèmes
webcam_index = 0 # 0 pour la première webcam, 1 pour la deuxième webcam, etc.

def display_webcam(camera_index):
    global webcam_backend

    cap = cv2.VideoCapture(camera_index, webcam_backend)

    if not cap.isOpened():
        print(f"Erreur: La webcam à l'index {camera_index} ne peut pas être ouverte.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur: Impossible de lire l'image de la webcam.")
            break

        cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

display_webcam(webcam_index)
