
import cv2
import pytesseract



def read_puzzle(img):
    pytesseract.pytesseract.tesseract_cmd = (r"C:\Program Files\Tesseract-OCR\tesseract.exe")

    if img is None:
        print("Failed to load image")
        return None

    width, height = 400, 400

    resized_img = cv2.resize(img, (width, height))


    gray = cv2.cvtColor(
        resized_img,
        cv2.COLOR_BGR2GRAY
    )

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    largest_square = None
    max_area = 0

    for cnt in contours:

        area = cv2.contourArea(cnt)

        # ignore tiny contours
        if area < 1000:
            continue

        peri = cv2.arcLength(cnt, True)

        approx = cv2.approxPolyDP(
            cnt,
            0.02 * peri,
            True
        )

        if len(approx) == 4 and area > max_area:
            largest_square = approx
            max_area = area

    if largest_square is None:
        print("No Sudoku grid found")
        return None

    cv2.drawContours(
        resized_img,
        [largest_square],
        -1,
        (0, 255, 0),
        3
    )

    # =========================
    # SPLIT INTO 9x9 CELLS
    # =========================

    x, y, w, h = cv2.boundingRect(largest_square)

    cell_width = w // 9
    cell_height = h // 9

    margin = 4

    board = [[0 for _ in range(9)] for _ in range(9)]

    config = r'--psm 10 -c tessedit_char_whitelist=123456789'

    for row in range(9):

        for col in range(9):

            cell_x = x + col * cell_width
            cell_y = y + row * cell_height

            cv2.rectangle(
                resized_img,
                (cell_x, cell_y),
                (cell_x + cell_width, cell_y + cell_height),
                (0, 255, 0),
                1
            )

            cell = thresh[
                cell_y + margin: cell_y + cell_height - margin,
                cell_x + margin: cell_x + cell_width - margin
            ]

            non_zero = cv2.countNonZero(cell)

            # =========================
            # EMPTY CELL CHECK
            # =========================

            if non_zero > 100:

                cell = cv2.GaussianBlur(
                    cell,
                    (5, 5),
                    0
                )

                enlarged = cv2.resize(
                    cell,
                    None,
                    fx=4,
                    fy=4
                )

                text = pytesseract.image_to_string(
                    enlarged,
                    config=config
                ).strip()

                if text.isdigit():

                    digit = int(text)

                    if 1 <= digit <= 9:
                        board[row][col] = digit

                #print(f"Cell ({row},{col}) = {board[row][col]}")

            #else:
                #print(f"Cell ({row},{col}) = 0")

    cv2.imshow("Sudoku Grid", resized_img)
    cv2.imshow("Threshold", thresh)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return board
