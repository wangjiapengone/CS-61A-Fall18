"""
Implementing helper functions of my final strategy
解决的问题：如果我想掷出S，那么掷几个骰子最可能实现呢？
"""
from collections import defaultdict


def compute_count_of_s(S):
    """计算掷出总数为S > 1的可能有多少种"""
    num_rolls = list(range(1, 11))  # 骰子掷出的个数为 1-10
    result = [0] * len(num_rolls)
    for roll in num_rolls:
        result[roll - 1] = helper(roll, S)
    return result


def helper(n, S):
    """掷出n个骰子，总点数为S的排列数"""
    if not 2 * n <= S <= 6 * n:  # 因为 pig out, 每个骰子的点数必须至少为 2
        return 0
    if n == 1:
        return 1
    result = 0
    for i in range(2, 7):
        result += helper(n - 1, S - i)
    return result


def max_prob_roll(s):
    """给出想掷出的总点数S，返回最可能的掷点策略（数目）"""
    if s == 1:
        return 10
    else:
        counts = compute_count_of_s(s)
        return counts.index(max(counts)) + 1


if __name__ == '__main__':
    print(1, 10)  # 容易得知： 掷10个骰子最容易得到1
    for s in range(2, 30):
        counts = compute_count_of_s(s)
        print(s, counts.index(max(counts)) + 1)  # 想掷点数; 最可能掷骰子策略
    for s in range(1, 30):
        print(max_prob_roll(s))
