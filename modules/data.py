# global variables
french_metropolitan_department_numbers = [str(num).zfill(2) for num in list(range(1, 96))]
print(french_metropolitan_department_numbers)
french_overseas_department_numbers = [971, 972, 973, 974, 975, 976, 977, 978, 984, 986, 987, 988, 989]
print(french_overseas_department_numbers)
french_department_numbers = french_metropolitan_department_numbers + french_overseas_department_numbers
print(french_department_numbers)
