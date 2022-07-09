from PIL import Image
import numpy as np
import os


def containsDigit(name):
	for ltr in name:
		if ltr.isdigit():
			return True
	return False


for direction in ["Right", "Left"]:
	for state in ["Attack", "Die", "Hurt", "Stand", "Walk"]:
		path = f"./{direction}/{state}"
		for name in os.listdir(path):
			if containsDigit(name):
				image = Image.open(f"{path}/{name}")
				w, h = image.size

				load = image.load()
				loadList = []

				for j in range(h):
					l = []
					for i in range(w):
						l.append(load[i, j])
						if load[i, j] == (255, 255, 255, 255):
							l[-1] = (0, 0, 0, 0)
					loadList.append(l)

				im = Image.fromarray(np.array(loadList, dtype=np.uint8))
				im.save(f"{path}/{name}")
