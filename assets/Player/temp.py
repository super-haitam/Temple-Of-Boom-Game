from PIL import Image


dictionary = {"Stand": 5, "Walk": 8, "Shoot": 5, "Die": 8}
for directory in ["Right", "Left"]:
	for state in ["Stand", "Walk", "Shoot", "Die"]:
		img = Image.open(f"./{directory}/{state}/{state}.png")
		w, h = img.size

		numImg = dictionary[state]
		for i in range(numImg):
			im = img.crop([i*(w/numImg), 0, (i+1)*(w/numImg), h])
			im.save(f"./{directory}/{state}/{state}{i}.png")

