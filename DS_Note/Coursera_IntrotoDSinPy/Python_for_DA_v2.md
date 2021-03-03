# Ch2

## introspection

Var, Function + "?" -> show info.

Function + "??" -> show source code

## Command

%run # run other py script in jupyter notebook

%load # import py script in jupyter notebook

%timeit # Measure execute time

    a = np.random.randn(100, 100)
    %timeit np.dot(a, a)
    
    # 57.3 µs ± 1.91 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    
%debug? # "?" to check command info

%quickref, %magic # show commands

%matplotlib inline # integrate w/ matplotlib, setup matplotlib

## list

list() : constructor creating a new list

    a = [1,2,3]
    b = a
    c = list(a)
    
    a is b # true
    a is not c # true
    a == c # true
    
## Changeable / Unchangeable

Changeable: Most class

    a_list = ['foo', 2, [4, 5]]
    b_list = a_list
    b_list[2] = (3, 4)
    # a_list = ['foo', 2, [3, 4]]
    
Unchangeable: string, turple

    a = 'this is a string'
    b = a.replace('string', 'longer string')
    # a = 'this is a string'; b = 'this is a longer string'

## Ternary Op

    value = true-expr if condition else false-expr

    'Non-negative' if x >= 0 else 'Negative'
    
    if x >=0:
        value = 'Non-negative'
    else:
        value = 'Negative'
       
# Ch3



# Ch4

# Ch5

# Ch7