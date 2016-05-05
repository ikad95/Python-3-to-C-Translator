# This time use nested if to solve the problem

num = float(input("Enter a number: "))
if num >= 0:
	if num == 0:
		print("Zero")
	else:
		print("Positive number")
else:
	print("Negative number")