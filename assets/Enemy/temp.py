from PIL import Image
import numpy as np


dic = {"Attack": 6, "Die": 4, "Hurt": 2, "Stand": 4, "Walk": 6}

# for n, state in enumerate(["Attack", "Die", "Hurt", "Stand", "Walk"]):
# 	image = Image.open(f"./Right/{state}/{state}.jpg")
# 	w, h = image.size

# 	num = dic[state]
# 	for i in range(num-1, -1, -1):
# 		im = image.crop([w-((i+1)*(w/6)), 0, w-(i*(w/6)), h])
# 		im.save(f"./Right/{state}/{state}{i}.jpg")

image = Image.open(f"./Right/Attack/Attack4.png")
w, h = image.size

loadList = []
load = image.load()
for j in range(h):
	l = []
	for i in range(w):
		l.append(load[i, j])
		if load[i, j] == (255, 255, 255, 255):
			l[-1] = (0, 0, 0, 0)
	loadList.append(l)

print(loadList[0][0])

arr = np.array(loadList, dtype=np.uint8)
im = Image.fromarray(arr)
im.show()
