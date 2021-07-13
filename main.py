from tkinter import filedialog
import pandas as pd
import cv2


# Global Variables
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
clicked = False
r = g = b = xpos = ypos = 0

path = filedialog.askopenfilename()

cv2.namedWindow('Color Names', cv2.WINDOW_FREERATIO) # Second img
img1 = cv2.imread("images/black.jpg", cv2.INTER_AREA)

if len(path) > 0:
    cv2.namedWindow("Color Detection App", cv2.WINDOW_FREERATIO)  # Main img
    img = cv2.imread(path, cv2.INTER_AREA)
    cv2.imshow("Color Detection App", img)

# Detect Color
def recognize_color(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i, "R"])) + abs(G- int(csv.loc[i, "G"])) + abs(B- int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Mouse Movement Function
def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Opening the image on the screen
cv2.setMouseCallback("Color Detection App", mouse_click)
# Looping the program until you Press ESC
while (1):
    cv2.imshow("Color Detection App", img)
    cv2.imshow("Color Names", img1)
    if (clicked):

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills that color entire rectangle
        cv2.rectangle(img1, (0, 0), (800, 480), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = recognize_color(r, g, b) + "[" + "R=" + str(r) + " G=" + str(g) + " B=" + str(b) +"]"

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img1, text, (9, 240), 2, 1.1, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if (r + g + b >= 600):
            cv2.putText(img1, text, (9, 240), 2, 1.1, (0, 0, 0), 2, cv2.LINE_AA)

        # Stopping clicking
        clicked = False

# Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
