def add(a, b):
	print("__name__", __name__)
	return a + b

def sub(a, b):
	print("__name__", __name__)
	return a - b

# if __name__ == "__main__"의 의미
print("__name__", __name__)	#__name__은 __main__이다 #다른데로 호출되면 __main__이아님

if __name__ == "__main__":
	print(add(3, 4))
	print(sub(4, 2))

