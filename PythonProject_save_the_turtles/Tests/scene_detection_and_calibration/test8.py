import cv2
import numpy as np

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def auto_detect_edges(image_path):
    image = cv2.imread(image_path)
    orig = image.copy()

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    lower_white = np.array([0, 0, 212])
    upper_white = np.array([131, 255, 255])

    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    mask_combined = cv2.bitwise_or(mask_red, mask_white)

    kernel = np.ones((5,5), np.uint8)
    mask_closed = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    masked_gray = cv2.bitwise_and(gray, gray, mask=mask_closed)

    blurred = cv2.GaussianBlur(masked_gray, (5, 5), 0)

    edged = cv2.Canny(blurred, 30, 150)

    cv2.imshow("Edges", edged)
    cv2.waitKey(0)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for i, contour in enumerate(contours):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)

    if screenCnt is not None and len(screenCnt) == 4:
        single_contour_img = orig.copy()
        cv2.drawContours(single_contour_img, [screenCnt], -1, (0, 255, 0), 3)

        for i, point in enumerate(screenCnt):
            x, y = point.ravel()
            cv2.circle(single_contour_img, (x, y), 7, (255, 0, 0), -1)
            cv2.putText(single_contour_img, f"{i+1}", (x - 25, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

        text = f"Contour {i+1}: 4 points"
        cv2.putText(single_contour_img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        cv2.imshow(f"Contour {i+1}", single_contour_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if detected == 1:
        return screenCnt.reshape(4, 2)
    else:
        return None

contour_points = auto_detect_edges('floor2.png')

if contour_points is not None:
    orig = cv2.imread('floor.png')
    
    warped = four_point_transform(orig, contour_points)

    cv2.imshow("Original", orig)
    cv2.imshow("Warped", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No suitable contour found")
