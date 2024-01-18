import cv2

def list_available_cameras(max_tests=2):
    available_cameras = []
    for i in range(max_tests):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap is None or not cap.isOpened():
            print(f"Camera at index {i} is not available.")
        else:
            print(f"Camera at index {i} is available.")
            available_cameras.append(i)
        cap.release()
    return available_cameras

# Testez les 4 premières caméras
cameras = list_available_cameras(4)
print("Available Cameras:", cameras)
