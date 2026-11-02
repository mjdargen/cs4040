# Code atom: creating, indexing and changing lists (plain Python, no Pygame Zero).
# Quoted by: u4m1-slides.qmd, u4m1-cheatsheet.qmd

# start snippet nums_demo
# start snippet define
nums = [2, 4, 6, 8, 10, 12]
# end snippet define
nums[0]  # accesses 1st element - index 0
nums[2]  # accesses 3rd element - index 2
nums[-1]  # accesses last element
nums[1] = 8  # updates 2nd element
print(nums)  # prints the new list
# end snippet nums_demo

# start snippet fruits
fruits = ["pear", "fig", "cherry"]
fruits[1]  # fig
fruits[0] = "grape"  # ["grape", "fig", "cherry"]
len(fruits)  # 3
fruits.remove("cherry")  # ["grape", "fig"]
fruits.append("apple")  # ["grape", "fig", "apple"]
item = fruits.pop()  # ["grape", "fig"]
item = fruits.pop(0)  # ["fig"]
fruits.clear()  # []
# end snippet fruits

# start snippet pets
pets = ["cat", "dog", "fish"]
pets[1]  # dog
pets[0] = "pig"  # ["pig", "dog", "fish"]
len(pets)  # 3
pets.remove("fish")  # ["pig", "dog"]
pets.append("rat")  # ["pig", "dog", "rat"]
item = pets.pop(0)  # ["dog", "rat"]
item = pets.pop()  # ["dog"]
pets.clear()  # []
# end snippet pets
