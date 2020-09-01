from django.test import TestCase
import sys
import os
import re

# Create your tests here.
import sys
import math
def addStrings(num1, num2):
    # write code here
    len1 = len(num1)
    len2 = len(num2)
    num = []
    str_num = ''
    if num1[len1-1]=='\n' or num1[len1-1]=='\r\n':
        l1 = len1 - 2
    if num2[len2-1]=='\n' or num2[len2-1]=='\r\n':
        l2 = len2 - 2

    c = 0
    while l1 >= 0 and l2 >= 0:
        t = int(num1[l1]) + int(num2[l2]) + c
        s = int(t % 10)
        c = int(t / 10)
        num.append(s)
        l1 -= 1
        l2 -= 1
    print(l1,l2)
    while l1 >= 0 and c > 0:
        t = int(num1[l1]) + c
        s = int(t % 10)
        c = int(t / 10)
        num.append(s)
        l1 -= 1
    while l2 >= 0 and c > 0:
        t = int(num2[l2]) + c
        s = t % 10
        c = t / 10
        num.append(s)
        l2 -= 1
    if l1 >= 0:
        str_num = num1[0:l1 + 1]
    if l2 >= 0:
        str_num = num2[0:l2 + 1]
    l3 = len(num)
    i = l3 - 1
    while i >= 0:
        str_num += str(num[i])
        i -= 1
    return str_num

def maxSubArray(nums):
    # write code here
    sums = 0
    i = 0
    while i < len(nums):
        if nums[i] < 0:
            i += 1
        else:
            break
    mark = 1
    tempt = 0
    newnums = sorted(nums)
    if i == len(nums):
        return newnums[len[nums] - 1]

    while i < len(nums):
        if nums[i] >= 0 and mark > 0:
            sums += nums[i]
        else:
            tempt += nums[i]
            mark = 0
            if tempt > 0:
                mark = 1
                sums += tempt
        i += 1
    return sums




# 请完成下面这个函数，实现题目要求的功能
# 当然，你也可以不按照下面这个模板来作答，完全按照自己的想法来 ^-^
# ******************************开始写代码******************************


def divingBoard(a, b, k):
    arr = []
    for i in range(0, k + 1):
        j = k - i
        sums = a * i + b * j
        if sums in arr:
            continue
        else:
            arr.append(sums)
    print(arr)
    return arr


# ******************************结束写代码******************************


def getNum(codes):
    s = '0010'
    index = codes.find(s)
    num = 0;
    while index >= 0:
        num += 1
        if codes[index + 4] == '0':
            index = codes.find(s, index + 3)
        elif codes[index + 4] == '1':
            index = codes.find(s, index + 4)
        else:
            index = codes.find(s, index + 4)
    return num



def func(arr):
    left = []
    right = []
    left.append(0)
    left.append(1)
    right.append(0)
    right.append(1)
    for j in range(2,len(arr)):
        k=j-1
        l = j-2
        le = 0
        while l>=0:
            if arr[k]<=arr[l]:
                break
            l-=1
        if l < 0:
            le = 1
        else:
            le = left[l+1]+1
        left.append(le)
    ls = len(arr)
    j=ls-3
    while j >=0:
        k=j+1
        l = j+2
        re = 0
        while l<ls:
            if arr[k]<=arr[l]:
                break
            l +=1
        if l ==ls:
            re = 1
        else:
            re=right[ls-l]+1
        right.append(re)
        j-=1
    return left,right

def allOrderOfString(s):
    all_list = [[s[0]]]
    l=0
    l2=1
    for i in range(1,len(s)):
        for j in range(l,l2):
            item = all_list[j]
            for index in range(len(item)):
                t = list(item)
                t.insert(index,s[i])
                all_list.append(t)
            t = item
            t.append(s[i])
            all_list.append(t)
        l=l2
        l2=len(all_list)
    return all_list


if __name__ == "__main__":
    # n = int(input())
    # arr = list(map(int, input().split(' ')))
    # print(len(arr))
    # left, right = func(arr)
    # print(left,right)
    # l = len(arr)
    # for i in range(l):
    #     print(left[i] + right[l-i-1] + 1, end=' ')
    print(allOrderOfString('abh'))
    print(allOrderOfString('abhdcgo'))
