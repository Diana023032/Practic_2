nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
new_nums = set(nums)
for num in new_nums:
    # подсчитываем,сколько раз число встречается в списке и проверяем, встречается ли оно более одного раза
    if nums.count(num) > 1:
        print("true")
        break
    else:
        print("false")
