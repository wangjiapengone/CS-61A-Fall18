"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact
from operator import sub

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def get_last_two_digits(n):
    """Get the last two digits of N > 0"""
    assert type(n) == int, 'n must be an integer'
    assert n >= 0, 'n must be non-negative'
    quo, ones = divmod(n, 10)
    tens = quo % 10
    return tens, ones


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    pig_out = False  # whether the pig out happened
    total = 0
    for _ in range(num_rolls):
        curr = dice()
        total += curr
        if curr == 1:  # pig out
            pig_out = True
    return 1 if pig_out else total
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    tens, ones = get_last_two_digits(score)
    return max(2 * tens - ones, 1)
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls > 0:
        return roll_dice(num_rolls, dice=dice)
    else:
        return free_bacon(opponent_score)
    # END PROBLEM 3


def is_swap(player_score, opponent_score):
    """
    Return whether the current player's score has the same absolute
    difference between its last two digits as the opponent's score.
    """
    # BEGIN PROBLEM 4
    diff_player = sub(*get_last_two_digits(player_score))
    diff_opponent = sub(*get_last_two_digits(opponent_score))
    return abs(diff_player) == abs(diff_opponent)
    # END PROBLEM 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def each_turn(strategy, player_score, opponent_score, dice, goal):
    """Simulate each turn of the gane."""
    num_rolls = strategy(player_score, opponent_score)
    player_score += take_turn(num_rolls, opponent_score, dice)
    if is_swap(player_score, opponent_score):
        player_score, opponent_score = opponent_score, player_score
    return player_score, opponent_score


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    while score0 < goal and score1 < goal:
        if player == 0:
            score0, score1 = each_turn(strategy0, score0, score1, dice, goal)
        else:
            score1, score0 = each_turn(strategy1, score1, score0, dice, goal)
        player = other(player)
        # END PROBLEM 5
        # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)
        # BEGIN PROBLEM 6
        say = say(score0, score1)
        # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores

def announce_lead_changes(previous_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != previous_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say

def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 17) # Player 0 gets 7 points, then Swine Swap applies
    Player 0 now has 6 and Player 1 now has 17
    Player 1 takes the lead by 11
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, previous_high=0, previous_score=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 11)
    11 point(s)! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 11)
    >>> f4 = f3(13, 20) # Player 1 gets 2 points, then Swine Swap applies
    >>> f5 = f4(20, 35) # Player 0 gets 22 points, then Swine Swap applies
    15 point(s)! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 47) # Player 1 gets 12 points; not enough for a new high
    >>> f7 = f6(21, 47)
    >>> f8 = f7(21, 77)
    30 point(s)! That's the biggest gain yet for Player 1
    >>> f9 = f8(77, 22) # Swap!
    >>> f10 = f9(33, 77) # Swap!
    55 point(s)! That's the biggest gain yet for Player 1
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    def say(score0, score1):
        current_score = score1 if who else score0
        gain = current_score - previous_score
        if gain > previous_high:
            print('{} point(s)! That\'s the biggest gain yet for Player {}'.format(gain, who))
        return announce_highest(who, max(gain, previous_high), current_score)
    return say
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average value of FN when called.
    N 次调用 fn. 每次计算 fn 的值，再求平均

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    def average(*args):
        total = sum(fn(*args) for _ in range(num_samples))
        return total / num_samples
    return average
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    max_score = 0
    optimal_num = 0
    aver_func = make_averaged(roll_dice, num_samples)
    for num_rolls in range(1, 11):
        aver_score = aver_func(num_rolls, dice)
        if aver_score > max_score:
            max_score = aver_score
            optimal_num = num_rolls
    return optimal_num
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if True:  # Change to True to test always_roll(8)
        # print('always_roll(8) win rate:', average_win_rate(always_roll(8)))
        print('always_roll(6) win rate:', average_win_rate(always_roll(6), baseline=always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    return 0 if free_bacon(opponent_score) >= margin else num_rolls  # Replace this statement
    # END PROBLEM 10


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points and does not trigger a
    non-beneficial swap. Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    expected_score = score + free_bacon(opponent_score)
    if is_swap(expected_score, opponent_score):  # trigger a swap
        if expected_score < opponent_score:  # beneficial swap
            return 0
        else:
            return num_rolls
    else:  # no swap
        return bacon_strategy(score, opponent_score, margin, num_rolls)
    # END PROBLEM 11


from my_final_strategy import max_prob_roll


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    每次掷出n个六面骰子的期望点数为（掷10,000次的平均值）：
    1 3.50
    2 5.86
    3 7.36
    4 8.22
    5 8.63
    6 8.70
    7 8.55
    8 8.21
    9 7.78
    10 7.30
    则掷6个的期望最大

    策略：
    1. 用 swap_strategy 作为 baseline
    2. 尝试掷 0-3 个骰子能否大概率结束比赛（当 num_rolls=4 时，总点数为 1 的概率大于 50%）
    3. 当和对方有一定分差时，尝试制造 swap （但从结果看对胜率的提升有限）
    
    final_strategy win rate: 0.6699
    """
    # BEGIN PROBLEM 12
    num_rolls = 6  # 因为6个的期望最大
    margin = 8
    baseline_num = swap_strategy(score, opponent_score, margin, num_rolls)  # win rate: 0.648
    check_win = win_by_num(score, opponent_score, GOAL_SCORE)
    for num in range(4):  # check whether win the game or not by rolling 0, 1, 2, 3
        if check_win(num):
            return num
    if baseline_num != 0 and score + margin < opponent_score:  # 如果己方和对方分数差距比较大时，可以尝试制造 swap
        expected_score = find_closest_match(score, opponent_score)
        return max_prob_roll(expected_score - score) if expected_score < opponent_score else baseline_num
    else:
        return baseline_num
    # END PROBLEM 12


def find_closest_match(score, opponent_score):
    """找到最小的大于score，且 abs(score个十位差) == abs(opponent_score个十位差) 的数字"""
    stop = False
    while not stop:
        score += 1
        if is_swap(score, opponent_score):
            stop = True
    return score


def win_by_num(score, opponent_score, goal):
    """Whether rolling NUM dice can win the game"""
    expectations = {
            1: 3.50, 
            2: 5.86, 
            3: 7.36, 
            4: 8.22, 
            5: 8.63, 
            6: 8.70, 
            7: 8.55, 
            8: 8.21, 
            9: 7.78, 
            10: 7.30, 
        }  # 掷 NUM 个骰子得到点数的期望值
    def win(num):
        if num == 0:
            expected_score = score + free_bacon(opponent_score)
            if expected_score >= goal and \
                not (is_swap(expected_score, opponent_score) and expected_score >= opponent_score):
                return True
        else:
            expected_score = expectations[num]
            return score + expected_score >= goal 
    return win


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()