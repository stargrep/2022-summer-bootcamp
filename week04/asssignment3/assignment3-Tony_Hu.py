# Q1. Given a positive integer N. The task is to write a Python program to check if the number is prime or not.
from typing import Tuple


def is_prime(n: int) -> bool:
    count = 0
    for i in range(1,n+1):
        if n % i == 0:
            count+=1
    if count == 2:
        return True
    else:
        return False


# DO NOT ALTER BELOW.
assert is_prime(2)
assert not is_prime(15)
assert is_prime(7907)
assert not is_prime(-1)
assert not is_prime(0)


# Q2 Write a function rotate(ar[], d) that rotates arr[] of size n by d elements.
# Input ar = [1,2,3,4,5,6,7], d = 2
# Output [3,4,5,6,7,1,2]

def rotate(ar: [int], d: int) -> [int]:
    num = d % len(ar)
    return ar[num:] + ar[:num]


# DO NOT ALTER BELOW.
assert rotate([1, 2, 3, 4, 5, 6, 7], 2) == [3, 4, 5, 6, 7, 1, 2]
assert rotate([1, 2, 3], 4) == [2, 3, 1]


# Q3. Selection sort - implement a workable selection sort algorithm
# https://www.runoob.com/w3cnote/selection-sort.html 作为参考
# Input students would be a list of [student #, score], sort by score ascending order.

def selection_sort(arr: [[int]]) -> [[int]]:
    for i in range(len(arr)-1):
        for j in range(i+1,len(arr)):
            if arr[i][1] > arr[j][1]:
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
    return arr


# DO NOT ALTER BELOW.
assert selection_sort([]) == []
assert selection_sort([[1, 100], [2, 70], [3, 95], [4, 66], [5, 98]]) == [[4, 66], [2, 70], [3, 95], [5, 98], [1, 100]]


# Q4. Convert a list of Tuples into Dictionary
# tip: copy operation - copy by value, copy by reference

def convert(tup: (any), di: {any, any}) -> None:
    if len(tup) == 0 or len(tup) % 2 == 1:
        pass
    else:
        key = tup[0::2]
        val = tup[1::2]
        for i in range(len(key)):
            di[key[i]] = val[i]
        pass
    # Do NOT RETURN di, EDIT IN-PLACE

# DO NOT ALTER BELOW.
expected_dict = {}
convert((), expected_dict)
assert expected_dict == {}

convert(('key1', 'val1', 'key2', 'val2'), expected_dict)
assert expected_dict == {'key1': 'val1', 'key2': 'val2'}


# Q5. Find left-most and right-most index for a target in a sorted array with duplicated items.
# provided an example of slow version of bsearch_slow with O(n) time complexity.
# your solution should be faster than bsearch_slow

def bsearch_slow(arr: [int], target: int) -> tuple:
    left = -1
    right = -1
    for i in range(len(arr)):
        if arr[i] == target and left == -1:
            left = i
        if arr[i] > target and left != -1 and right == -1:
            right = i
        if i == len(arr) - 1:
            right = len(arr) - 1
    return left, right


def create_arr(count: int, dup: int) -> [int]:
    return [dup for i in range(count)]


# Complete this
def bsearch(arr: [int], target: int) -> tuple:
    left = 0
    right = len(arr) - 1
    while arr[left] != target:
        left += 1
    while arr[right] != target:
        right -= 1
    return left, right


assert bsearch_slow(create_arr(10000, 5), 5) == (0, 9999)
assert bsearch(create_arr(1000, 5), 5) == (0, 999)

import timeit

# slow version rnning 100 times = ? seconds
t1 = timeit.timeit(lambda: bsearch_slow(create_arr(10000, 5), 5), number=100)

# add your version and compare if faster.
t2 = timeit.timeit(lambda: bsearch(create_arr(10000, 5), 5), number=100)
print(t1-t2)


# Q6.
"""
请实现 2个python list 的 ‘cross product’ function.
要求按照Numpy 中cross product的效果: https://numpy.org/doc/stable/reference/generated/numpy.cross.html
只实现 1-d list 的情况即可.
x = [1, 2, 0]
y = [4, 5, 6]
cross(x, y)
> [12, -6, -3]
"""


def deter(A):
    if len(A[0]) == 2:
        re = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        re = 0
        for i in range(0, len(A[0])):
            re += A[0][i] * deter(remain(A, i)) * ((-1) ** i)  # 按第i列展开
    return re


def remain(A, i):
    ans = []
    for j in range(1, len(A[0])):
        temp = []
        for k in range(0, len(A[0])):
            if k == i:
                pass
            else:
                temp.append(A[j][k])
        ans.append(temp)
    return ans


def cross(x, y):
    ans = []
    for i in range(0, len(x)):
        row = [0 for i in range(0, len(x))]
        row[i] = 1
        ans.append(deter([row, x, y]))
    return ans


x = [1, 2, 0]
y = [4, 5, 6]
print(cross(x, y))

# Q7.
"""
交易传输指令经常需要验证完整性，比如以下的例子
{ 
    request : 
    { 
        order# : 1, 
        Execution_details: ['a', 'b', 'c'],
        request_time: "2020-10-10T10:00EDT"
    },
    checksum:1440,
    ...
}
可以通过很多种方式验证完整性，假设我们通过判断整个文本中的括号 比如 '{}', '[]', '()' 来判断下单是否为有效的。
比如 {{[],[]}}是有效的，然而 []{[}](是无效的。 
写一个python 程序来进行验证。
 def checkOrders(orders: [str]) -> [bool]:
 return a list of True or False.
checkOrders(["()", "(", "{}[]", "[][][]", "[{]{]"] return [True, False, True, True, False]
"""


def match(first: str, last: str) -> bool:
    check_dict = {'(': ')', '[': ']', '{': '}', ')': '(', ']': '[', '}': '{'}
    if check_dict[first] == last:
        return True
    else:
        return False


def is_full(chars: str) -> bool:
    stack = []
    for c in chars:
        if c in ['(', ')', '[', ']', '{', '}']:
            if len(stack) > 0:
                if match(stack[-1], c):
                    stack.pop()
                else:
                    stack.append(c)
            else:
                stack.append(c)
    if len(stack) > 0:
        return False
    else:
        return True


def checkOrders(orders: [str]) -> [bool]:
    ans = []
    for order in orders:
        ans.append(is_full(order))
    return ans


# test
print(checkOrders(["()", "(", "{}[]", "[][][]", "[{]{]"]))
print(is_full('''request : { order# : 1, Execution_details: ['a', 'b', 'c'], request_time: "2020-10-10T10:00EDT"}'''))


# Q8.
"""
我们在进行交易的时候通常会选择一家broker公司而不是直接与交易所交易。
假设我们有20家broker公司可以选择 (broker id is [0, 19])，通过一段时间的下单表现(完成交易的时间)，我们希望找到最慢的broker公司并且考虑与其解除合约。
我们用简单的数据结构表达broker公司和下单时间: [[broker id, 此时秒数]]
[[0, 2], [1, 5], [2, 7], [0, 16], [3, 19], [4, 25], [2, 35]]
解读: 
Broker 0 使用了2s - 0s = 2s
Broker 1 使用了5 - 2 = 3s
Broker 2 使用了7 - 5 = 2s
Broker 0 使用了16-7 = 9s
Broker 3 使用了19-16=3s
Broker 4 使用了25-19=6s
Broker 2 使用了35-25=10s
综合表现，是broker2出现了最慢的交易表现。
Def slowest(orders: [[int]]) -> int:
slowest([[0, 2], [1, 5], [2, 7], [0, 16], [3, 19], [4, 25], [2, 35]]) return 2
"""

def slowest(orders: [[int]]) -> int:
    grade = {}
    t = 0
    for i in range(len(orders)):
        if orders[i][0] not in grade.keys():
            grade[orders[i][0]] = orders[i][1] - t
        else:
            grade[orders[i][0]] += orders[i][1] - t
        t = orders[i][1]
    temp = sorted(grade.items(),key=lambda x: x[1])
    return temp[-1][0]

print(slowest([[0, 2], [1, 5], [2, 7], [0, 16], [3, 19], [4, 25], [2, 35]]))


# Q9.
"""
判断机器人是否能返回原点
一个机器人从平面(0,0)的位置出发，他可以U(向上), L(向左), R(向右), 或者D(向下)移动一个格子。
给定一个行走顺序，问是否可以回到原点。
例子
1. moves = "UD", return True.
2. moves = "LL", return False.
3. moves = "RRDD", return False.
4. moves = "LDRRLRUULR", return False.
def judgeRobotMove(moves: str) -> bool:
"""


def judgeRobotMove(moves: str) -> bool:
    x = 0
    y = 0
    for move in moves:
        if move == 'U':
            y += 1
        if move == 'D':
            y -= 1
        if move == 'L':
            x -= 1
        if move == 'R':
            x += 1
    if x == 0 and y == 0:
        return True
    else:
        return False

print(judgeRobotMove('UD'))
print(judgeRobotMove('LL'))
print(judgeRobotMove('RRDD'))
print(judgeRobotMove('LDRRLRUULR'))


# Q10.
"""
假设我们获得了一只股票的每日价格, 在这一天可以执行T+1买或卖的操作, 只能做多不能做空，每次只能持仓一股。
对于给定的价格序列，只能执行最多两次交易，写一个算法计算最高获利可以是多少。
Input: prices = [2,2,6,1,2,4,2,7]
Output: 10
解释: 6 - 2 + 7 - 1 = 10
Input: prices = [5, 3, 0]
Output: 0
解释: 没有交易。
Input: prices = [1,2,3,4,5,6,7]
Output: 6
解释: 7 - 1 = 6 因为只能持仓一股，不能再没有卖出1时购买。
"""


def trade(p: list) -> int:
    max_val = 0
    for i in range(len(p)):
        if max(p[i:]) - p[i] > max_val:
            max_val = max(p[i:]) - p[i]
    return max_val


def my_strtgy(p: list) -> int:
    ret = 0
    for i in range(len(p)):
        if trade(p[0:i]) + trade(p[i:]) > ret:
            ret = trade(p[0:i]) + trade(p[i:])
    return ret

print(my_strtgy([2, 2, 6, 1, 2, 4, 2, 7]))
print(my_strtgy([5, 3, 0]))
print(my_strtgy([1, 2, 3, 4, 5, 6, 7]))
print(my_strtgy([102220, 22200, 3200, 2412, 31, 22, 2, 2, 6, 1, 2, 4, 2, 7]))