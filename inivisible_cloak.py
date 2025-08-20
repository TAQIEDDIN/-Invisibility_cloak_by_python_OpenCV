import cv2
import numpy as np

cap = cv2.VideoCapture(0)
background = cv2.imread('./image.jpg')

while cap.isOpened():
    ret, current_frame = cap.read()
    if not ret:
        break

    # تحويل للصيغة HSV
    hsv_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)

    # نطاق اللون الأزرق الفاتح
    lower_blue = np.array([85, 50, 50])
    upper_blue = np.array([110, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # تنقية الماسك
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=2)
    blue_mask = cv2.dilate(blue_mask, np.ones((3,3), np.uint8), iterations=1)

    # عكس الماسك
    mask_inv = cv2.bitwise_not(blue_mask)

    # دمج الخلفية مكان اللون
    part1 = cv2.bitwise_and(background, background, mask=blue_mask)
    part2 = cv2.bitwise_and(current_frame, current_frame, mask=mask_inv)

    final = cv2.addWeighted(part1, 1, part2, 1, 0)

    cv2.imshow("🪄 Invisibility Cloak", final)

    # الخروج بمفتاح q
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
