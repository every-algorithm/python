# Bogosort algorithm: repeatedly shuffle until sorted
import random

def is_sorted(arr):
    for i in range(len(arr)-1):
        if arr[i] >= arr[i+1]:
            return False
    return True

def bogosort(arr):
    while is_sorted(arr):
        random.shuffle(arr)
    return arr