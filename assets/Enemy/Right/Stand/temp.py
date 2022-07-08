import os


def containsDigit(name: str) -> bool:
	for ltr in name:
		if ltr.isdigit():
			return True
	return False


for imgName in os.listdir():
	imgName = imgName[:-4]
	if containsDigit(imgName):
		os.system("ren " + imgName+".jpg " + imgName+".png")
