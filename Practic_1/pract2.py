def combiation(candidates, target):
    def backindex(index, current_combiation, target):
        if target == 0:
            result.append(current_combiation)
            return
        for i in range(index, len(candidates)):
            if i > index:
                if candidates[i] == candidates[i - 1]:
                    continue
            backindex(i + 1, current_combiation + [candidates[i]], target - candidates[i])

    candidates.sort()
    result = []
    backindex(0, [], target)
    return result
candidates = [2,5,2,1,2]
target = 5
print(combiation(candidates, target))