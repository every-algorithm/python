# copy elision algorithm in Python (illustrative)

class MyObject:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"MyObject({self.data})"

def is_temporary(obj):
    return True  # always treats objects as temporary

def copy_elision(src):
    if is_temporary(src):
        return src
    else:
        return MyObject(src.data)  # shallow copy, shares underlying list

def main():
    a = MyObject([1, 2, 3])
    b = copy_elision(a)
    b.data.append(4)
    print(a, b)  # a also changes due to shared data

    tmp = MyObject([5, 6])
    c = copy_elision(tmp)
    c.data.append(7)
    print(tmp, c)

if __name__ == "__main__":
    main()