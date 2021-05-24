'''2nd Assignment - Optimization problem by Dynamic-Programming algorithm'''
'''by Pietro Zafferani'''

'''Libraries used for the assignment's completion.'''
import random
from codetiming import Timer
import scipy.optimize as optimization

'''This function creates the list containing 'n' batches and their respective prices: L = [[0,0],...,[k, p_k],...,[n,$n]].'''


def Instances(n: int) -> list:
    L = []
    for i in range(n + 1):
        # the per-unity price is drawn in a range similar to the one used for the assignment's example (4-8),
        # then multiplied for the numbers of unities in the given batch
        batch = [i, i * random.randint(4, 8)]
        L.append(batch)
    return L


'''This is the core function of the algorithm, it takes as argument the list of batches and it returns the best selling
    plan. It is based on a dynamic programming algorithm, in order to obtain the optimal solution for the n batches, it
    it computes the optimal solution for n-1 batches and so on until we reach the base case, namely when n=0 and n=1.
    This approach is effective because the problem has as sub-optimal structure, in other words the optimal solution of 
    a given instance can be found by decomposing the problem in smaller parts, the optimal solution of the smaller 
    problems are used to reconstruct the optimal solution for the initial instance.'''


def DynamicSelling(L: list) -> tuple:
    # this dictionary stores the optimal solution for each sub-instance of n elements and their associated value
    OptimalDict = {}
    # we know a priori that the optimal solutions for the 0 batch is the batch itself
    # so we can directly save them in the dictionary with their associated value
    OptimalDict[0] = [L[0]], L[0][1]

    # we iterate over each stock of batches (starting from 1) in order to find the optimal solution for each one
    for M in range(1, len(L)):
        bestPlan = []
        bestMoney = 0
        # for each stock of batches we use their optimal sub-solutions to compute the respective optimal solution
        for f in range(1, M + 1):  # we consider only the batches smaller or equal than the current one
            currentPlan = []  # instantiate an empty selling plan that will be compared to the optimal one
            OptRest = M - f  # number of optimal batch to add to hypothetical one in each round

            # check if the money associated to the hypothetical batch 'f' + the optimal solution of the remaining
            # batches is better than the previous one
            if L[f][1] + OptimalDict[OptRest][1] >= bestMoney:
                # substitute the highest amount of money with the current one
                bestMoney = L[f][1] + OptimalDict[OptRest][1]
                # substitute the optimal selling plan with the current one
                currentPlan.append(L[f])
                currentPlan += OptimalDict[OptRest][0]
                bestPlan = currentPlan

        # save in the dictionary the optimal solution for the specific 'M' batch and the respective value
        OptimalDict[M] = bestPlan, bestMoney

    # return the optimal solution of the bigger batch 'n' in the dictionary
    return OptimalDict[len(L) - 1]


'''This function takes as argument the result produced by the Dynamic programming algorithm and prints it in a more
    readable way for the user.'''


def printResults(results: tuple) -> print:
    totMoney = results[1]
    print('Best selling plan:')
    for batch in results[0]:
        if batch[0] != 0:
            print('stock of ' + str(batch[0]) + ' batches sold for ' + str(batch[1]))
    print('Total amount of money: ' + str(totMoney))


'''This function uses an external library to record the average running time of the algorithm for a given number of 
    batches. The total number of trials is 1000.'''


def Test(n: int, repetitions=1000) -> float:
    # number of trials
    for i in range(repetitions):
        # create the list of batches
        Input = Instances(n)

        # record the running time
        with Timer(name='DynamicSelling', logger=None):
            DynamicSelling(Input)

    # return the average
    return round(Timer.timers.mean('DynamicSelling'), 9)


'''This function returns an array of running times, each one of them derives from testing the algorithm on a specific
    number of batches.'''


def Time_sets(input_array: list) -> list:
    Res = list()
    # iterating over the list of input sizes
    for Input in input_array:
        # test the running time for each input size
        result = Test(Input)
        Res.append(result)
    # return the an array of running times
    return Res


'''This function uses an external library to find a mathematical curve that is able to describe the behaviour of the 
    algorithm in terms of time complexity. '''


def fit_curve(sizes: list, times: list):
    # define the mathematical function: quadratic
    def curve(x, a, b):
        return a * (x ** 2) + b

    # return the coefficients that shape the curve in order to fit the data
    # sizes represents the X-axis coordinates
    # times represents the Y-xis coordinates
    return optimization.curve_fit(curve, sizes, times)


'''This function takes the arrays of the input sizes and of their respective running times, it returns a set of pairs 
    representing the coordinates needed for plotting the algorithm's behaviour. '''


def printPairs(sizes: list, time_data: list) -> print:
    for (n, t) in zip(sizes, time_data):
        print((n, t), end=' ')


'''The following section of the file is dedicated for the interaction with the user.'''
if __name__ == '__main__':

    # Let's solve the problem's instance given on the assignment sheet

    L = [[0, 0], [1, 5], [2, 9], [3, 18], [4, 21]]

    printResults(DynamicSelling(L))