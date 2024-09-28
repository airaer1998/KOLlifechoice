def build_bst(arr):
    tree = {}
    comparisons = set()

    def insert(val):
        if not tree:
            tree[val] = {'left': None, 'right': None}
            return

        current = tree
        while True:
            node_key = list(current.keys())[0]
            if val < node_key:
                comparisons.add((val, node_key))
                if current[node_key]['left'] is None:
                    current[node_key]['left'] = {val: {'left': None, 'right': None}}
                    break
                current = current[node_key]['left']
            else:
                comparisons.add((node_key, val))
                if current[node_key]['right'] is None:
                    current[node_key]['right'] = {val: {'left': None, 'right': None}}
                    break
                current = current[node_key]['right']

    for item in arr:
        insert(item)
        print(f"Inserted {item}. Current BST: {tree}")
        print(f"Comparisons so far: {comparisons}\n")

    return comparisons

def quicksort(arr):
    comparisons = set()

    def partition(low, high):
        pivot = arr[low]
        i = low + 1
        for j in range(low + 1, high + 1):
            comparisons.add((arr[j], pivot))
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[low], arr[i - 1] = arr[i - 1], arr[low]
        return i - 1

    def quick_sort(low, high):
        if low < high:
            pi = partition(low, high)
            print(f"Partitioned around {arr[pi]}. Current array: {arr}")
            print(f"Comparisons so far: {comparisons}\n")
            quick_sort(low, pi - 1)
            quick_sort(pi + 1, high)

    quick_sort(0, len(arr) - 1)
    return comparisons

# Test the theorem
A = ['g', 'c', 'a', 'n', 'i', 'r', 'e']

print("Building Binary Search Tree:")
S = build_bst(A.copy())

print("\nRunning QuickSort:")
Q = quicksort(A.copy())

print("\nComparison of S and Q:")
print(f"S: {S}")
print(f"Q: {Q}")
print(f"S == Q: {S == Q}")
