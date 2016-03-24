def f1(x):
    if x == 1:
        return x
    else:
        return x*f1(x-1)
def C(n, r):
    if not r:
        return 1
    elif n == r:
        return 1
    else:
        return f1(n)/(f1(r)*f1(n-r))
def yang(i):
    for a in range(i+1):
        print (' '*(i-a))
        for b in range(a):
            print (C(a,b))
        else:print ('\n')

if __name__ == '__main__':
    yang(5)