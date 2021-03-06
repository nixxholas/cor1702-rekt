# G7-T22
# BENJAMIN CHEW PIN HSIEN, NICHOLAS CHEN HAN WEI

# Q2

# Replace the content of this function with your own algorithm
# inputs: 
#   n: the number of members in your team
#   W: weight limit of each vehicle used for deliveries.
#   packages: 2D list [[packageID, reward, weight], [packageID, reward, weight], ...]
# returns:
#   2D list of package IDs to represent n sets of packages. 
#   e.g. if n = 2, this is a possible solution: [["P001", "P003"], ["P010"]]

def select_packageSets(n, W, packages):
    # Just define a fixed dictionary here.
    package_dict = get_package_dict(packages)
    unused_packages = []
    # Ensure it doesn't exist here.
    used_packages = set()

    # Split into chunks, sort them via profitability.
    # Profitability = reward/weight
    # Worst to Best
    valueMergeSort(packages)

    # We can multi-init like that
    # https://stackoverflow.com/questions/6142689/initialising-an-array-of-fixed-size-in-python
    set_threshold = [0] * n
    package_sets = []
    while len(package_sets) < n:
        package_sets.append([])

    # v1: Generic Greed
    # loop the packages first
    # while len(packages) > 0:
    #     # Obtain the current package
    #     cur_package = packages.pop()
    #     if cur_package[0] not in populated:
    #         # Obtain the least filled package set
    #         least_filled_index = get_smallest_index(set_threshold)
    #         if set_threshold[least_filled_index] + cur_package[2] <= W:
    #             package_sets[least_filled_index].append(cur_package[0])
    #             set_threshold[least_filled_index] += cur_package[2]
    #             populated.add(cur_package[0])
    #         else:
    #             # Loop every member
    #             for j in range(n):
    #                 # If the threshold inclusive of the incoming new package to add is within the weight limit,
    #                 if set_threshold[j] + cur_package[2] <= W:
    #                     package_sets[j].append(cur_package[0])
    #                     set_threshold[j] += cur_package[2]
    #                     populated.add(cur_package[0])
    #                     break

    # loop the packages first
    # push the least profitable packages first.
    package_index = 0
    while package_index < len(packages):
        # Obtain the current package
        cur_package = packages[package_index]
        if cur_package[0] not in used_packages:
            # Obtain the least filled package set
            least_filled_index = get_smallest_index(set_threshold)
            if set_threshold[least_filled_index] + cur_package[2] <= W:
                package_sets[least_filled_index].append(cur_package[0])
                set_threshold[least_filled_index] += cur_package[2]
                used_packages.add(cur_package[0])
            else:
                # Loop every member
                for j in range(n):
                    # If the threshold inclusive of the incoming new package to add is within the weight limit,
                    if set_threshold[j] + cur_package[2] <= W:
                        package_sets[j].append(cur_package[0])
                        set_threshold[j] += cur_package[2]
                        used_packages.add(cur_package[0])
                        break

        package_index += 1

    # Since they're already sorted by profitability, we can traverse and slowly scoop up
    alternator = 0  # Allows us to fairly alternate between each member.
    sub_altnerators = [0] * n  # Allow us to alternate
    while len(packages) > 0:
        package = packages.pop(0)
        # valueMergeSort(package_sets[alternator])

        # Ensure this package is not used.
        if package[0] not in used_packages:
            pushed = False

            # Iterate from the worst profitable packages first and see if they can potentially be
            # replaced for better profitability.
            for i in range(len(package_sets[alternator])):
                # Without addition, it might be possible as well.
                if set_threshold[alternator] + package[2] <= W:
                    package_sets[alternator].append(package[0])
                    used_packages.add(package[0])
                    set_threshold[alternator] += package[2]
                    pushed = True
                    break
                # If not, it might be possible for addition with deletion.
                # The least profitable package in the current set can be replaced by the current
                # package for better profitability, we get a better return.
                elif (set_threshold[alternator] - package_dict[package_sets[alternator][i]][1]) + package[2] <= W:
                    package_sets[alternator].append(package[0])
                    used_packages.add(package[0])
                    set_threshold[alternator] += (package[2] - package_dict[package_sets[alternator][i]][1])
                    used_packages.remove(package_sets[alternator][i])
                    del package_sets[alternator][i]
                    pushed = True
                    break

            if not pushed:
                unused_packages.append(package)

            # Rotate the sub-alternator
            if sub_altnerators[alternator] + 1 == len(package_sets[alternator]):
                sub_altnerators[alternator] = 0
            else:
                sub_altnerators[alternator] += 1

            # Rotate the alternator
            if alternator + 1 == len(package_sets):
                alternator = 0
            else:
                alternator += 1

    remaining_gap = W * n
    for threshold in set_threshold:
        remaining_gap -= threshold

    # Loop every sub-complete set
    for i in range(len(package_sets)):
        package_set = package_sets[i]

        for u_pack in unused_packages:
            if u_pack[2] + set_threshold[i] <= W:
                package_set.append(u_pack[0])
        # Loop every package in the set
        # for package in package_set:

    # return [[P001, P003], [P011, P007], [P004, P005, P006], [P012]]
    return package_sets


# Systematically have 2 sorted sets, one sorted according to profitability
# The other sorted according to weight
# Populate n number of members in a distributed manner.
def select_packageSets_ptw(n, W, packages):
    # Ensure it doesn't exist here.
    populated = set()

    # Split into chunks, sort them via profitability.
    # Profitability = reward/weight
    # Worst to Best
    valueMergeSort(packages)

    # We can multi-init like that
    # https://stackoverflow.com/questions/6142689/initialising-an-array-of-fixed-size-in-python
    set_threshold = [0] * n
    package_sets = []
    final_set = []
    while len(package_sets) < n:
        package_sets.append([])

    index = len(packages) - 1
    while len(package_sets) > 0:
        # Always traverse the shortest or smallest list
        curr_index = get_smallest_index(set_threshold)
        # Obtain the package with the current greatest profitability
        package = packages[index]

        # If the package in question has already been populated,
        if package[0] in populated:
            # Sort it out.
            del packages[index]
            index = (len(packages) - 1)
        # If the weight does not exceed if threshold with the current package,
        elif set_threshold[curr_index] + package[2] < W:
            set_threshold[curr_index] += package[2]
            package_sets[curr_index].append(package[0])
            populated.add(package[0])
            del packages[index]
            index -= 1
        else:
            index -= 1

        # If we're done traversing downwards
        if index == 0 and all_have_exceeded(set_threshold, package[2], W):
            # Since we're done, we can assume we're done.
            index = len(packages) - 1
            final_set.append(package_sets.pop(curr_index))

    # Weight-based sorting
    weight_sorted_packages = packages.copy()
    weightedMergeSort(weight_sorted_packages)

    # We should begin traversing through weight, going by the weight calculation.
    for i in range(len(weight_sorted_packages) - 1, 0, -1):
        # Always traverse the shortest or smallest list
        for j in range(len(set_threshold)):
            if weight_sorted_packages[i][0] not in populated and weight_sorted_packages[i][2] + set_threshold[j] < W:
                set_threshold[j] += weight_sorted_packages[i][2]
                package_sets[j].append(weight_sorted_packages[i][0])
                populated.add(weight_sorted_packages[i][0])
                packages.remove(weight_sorted_packages[i])
                del weight_sorted_packages[i]

    # ============================== END of profitability-then-weight method ============================== #


# you may insert other functions here, but all statements must be within functions
# before submitting to red, check that there are no print statements in your code. Nothing should be printed when your code runs.
def get_smallest_index(thresholds):
    index = 0
    for i in range(len(thresholds)):
        if thresholds[i] < thresholds[index]:
            index = i
    return index


def all_have_exceeded(thresholds, val, lim):
    for threshold in thresholds:
        if threshold + val < lim:
            return False
    return True


def get_package_dict(packages):
    res = {}
    for package in packages:
        res[package[0]] = package[1:]

    return res


def valueMergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements
        R = arr[mid:]  # into 2 halves

        valueMergeSort(L)  # Sort the first half
        valueMergeSort(R)  # Sort the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            # Profitability = reward/weight
            if L[i][1] / L[i][2] < R[j][1] / R[j][2]:
                # if (L[i][2] < R[j][2]) or (L[i][2] == R[j][2] and L[i][1] / L[i][2] < R[j][1] / R[j][2]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1


def weightedMergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements
        R = arr[mid:]  # into 2 halves

        valueMergeSort(L)  # Sort the first half
        valueMergeSort(R)  # Sort the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            # Profitability = reward/weight
            if L[i][2] < R[j][2]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1


def rewardMergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements
        R = arr[mid:]  # into 2 halves

        valueMergeSort(L)  # Sort the first half
        valueMergeSort(R)  # Sort the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            # Profitability = reward
            if L[i][1] < R[j][1]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1


# def package_sort(package_sets, set_thresholds):
#     sorted_package_sets = []
#     sorted_set_threshold = []
#
#     # Sort the sets according to thresholds first
#     for i in range(len(set_thresholds)):
#         if len(sorted_set_threshold) == 0:
#             sorted_set_threshold.append(set_thresholds[i])
#             sorted_package_sets.append(package_sets[i])
#         else:
#             for j in range(len(sorted_set_threshold)):
#                 if sorted_set_threshold[j] > set_thresholds[i]:
#                     sorted_set_threshold.insert(j, set_thresholds[i])
#                     sorted_package_sets.insert(j, package_sets[i])
#
#     for i in range(len(sorted_set_threshold)):
