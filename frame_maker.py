import random

def split(rect, vertical):
	area = rect["w"]*rect["h"]
	if (area < min_area):
		return [rect]
	elif (vertical):
		w_new = random.randint(int(0.3*rect["w"]), int(0.7*rect["w"]))
		rect1 = {"x": rect["x"], "y": rect["y"], "w": w_new, "h": rect["h"]}
		rectangles1 = split(rect1, not vertical)
		rect2 = {"x": rect["x"] + w_new, "y": rect["y"], "w": rect["w"] - w_new, "h": rect["h"]}
		rectangles2 = split(rect2, not vertical)
	else:
		h_new = random.randint(int(0.3*rect["h"]), int(0.7*rect["h"]))
		rect1 = {"x": rect["x"], "y": rect["y"], "w": rect["w"], "h": h_new}
		rectangles1 = split(rect1, not vertical)
		rect2 = {"x": rect["x"], "y": rect["y"] + h_new, "w": rect["w"], "h": rect["h"] - h_new}
		rectangles2 = split(rect2, not vertical)

	rectangles1.extend(rectangles2)
	rectangles1.append(rect)
	return rectangles1



width = 2700
height = 1800
min_area = 50000

rect = {"x": 0, "y": 0, "w": width, "h": height}
rectangles = split(rect, True)