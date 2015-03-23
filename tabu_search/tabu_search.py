'''
Created on Jun 17, 2011
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
import math
import random


# Function which calculates the euclidean distance between two points
def euclideanDistance(v1, v2):
    # use Zip to iterate over the two vectors
    sum = 0.0
    for coord1, coord2 in zip(v1, v2):
        sum += pow((coord1 - coord2), 2)

    return math.sqrt(sum)


# Function that evaluates the total length of a path
def tourCost(perm):
    # Here tour cost refers to the sum of the euclidean distance between
    # consecutive points starting from first element
    totalDistance = 0.0
    size = len(perm)
    for index in range(size):
        # select the consecutive point for calculating the segment length
        if index == size - 1:
            # This is because in order to complete the 'tour' we need to reach
            # the starting point
            point2 = perm[0]
        else:  # select the next point
            point2 = perm[index + 1]

        totalDistance += euclideanDistance(perm[index], point2)

    return totalDistance


def stochasticTwoOptWithEdges(perm):
    result = perm[:]  # make a copy
    size = len(result)
    # select indices of two random points in the tour
    p1, p2 = random.randrange(0, size), random.randrange(0, size)
    # do this so as not to overshoot tour boundaries
    exclude = set([p1])
    if p1 == 0:
        exclude.add(size - 1)
    else:
        exclude.add(p1 - 1)

    if p1 == size - 1:
        exclude.add(0)
    else:
        exclude.add(p1 + 1)

    while p2 in exclude:
        p2 = random.randrange(0, size)

    # to ensure we always have p1<p2
    if p2 < p1:
        p1, p2 = p2, p1

    # now reverse the tour segment between p1 and p2
    result[p1:p2] = reversed(result[p1:p2])

    return result, [[perm[p1 - 1], perm[p1]], [perm[p2 - 1], perm[p2]]]


# Function that creates a random permutation from an initial permutation by
# shuffling the elements in to a random order
def constructInitialSolution(initPerm):
    # Randomize the initial permutation
    permutation = initPerm[:]  # make a copy of the initial permutation
    size = len(permutation)
    for index in range(size):
        # shuffle the values of the initial permutation randomly
        # get a random index and exchange values
        shuffleIndex = random.randrange(index, size)
        permutation[shuffleIndex], permutation[index] = permutation[index],permutation[shuffleIndex]

    return permutation


'''

TABU SEARCH PART

'''

# Function that returns a best candidate, sorting by cost
def locateBestCandidate(candidates):
    candidates.sort(key=lambda(c): c["candidate"]["cost"])
    best, edges = candidates[0]["candidate"], candidates[0]["edges"]
    return best, edges


def isTabu(perm, tabuList):
    result = False
    size = len(perm)
    for index, edge in enumerate(perm):
        if index == size - 1:
            edge2 = perm[0]
        else:
            edge2 = perm[index + 1]
        if [edge, edge2] in tabuList:
            result = True
            break

    return result


def generateCandidates(best, tabuList, points):
    permutation, edges, result = None, None, {}
    while permutation is None or isTabu(best["permutation"], tabuList):
        permutation, edges = stochasticTwoOptWithEdges(best["permutation"])
    candidate = {}
    candidate["permutation"] = permutation
    candidate["cost"] = tourCost(candidate["permutation"])
    result["candidate"] = candidate
    result["edges"] = edges
    return result


def search(points, maxIterations, maxTabu, maxCandidates):
    # construct a random tour
    best = {}
    best["permutation"] = constructInitialSolution(points)
    best["cost"] = tourCost(best["permutation"])
    tabuList = []
    print "Let's start"
    while maxIterations > 0:
        # Generate candidates using stocahstic 2-opt near current
        # best candidate
        # Use Tabu list to not revisit previous rewired edges
        candidates = []
        for index in range(0, maxCandidates):
            candidates.append(generateCandidates(best, tabuList, points))
        # Locate the best candidate
        print "Locating the best candidate"
        # sort the list of candidates by cost
        # since it is an  involved sort, we write a function for getting
        # the least cost candidate
        bestCandidate, bestCandidateEdges = locateBestCandidate(candidates)
        print "Best candidate: {0}\nBest candidateEdges: {1}".format(
            bestCandidate,
            bestCandidateEdges)
        # compare with current best and update if necessary
        if bestCandidate["cost"] < best["cost"]:
            # set current to the best, so that we can continue iteration
            best = bestCandidate
            # update tabu list
            for edge in bestCandidateEdges:
                if len(tabuList) < maxTabu:
                    tabuList.append(edge)

        maxIterations -= 1

    return best

if __name__ == '__main__':
    # Problem Configuration
    # Use Berlin52 instance of TSPLIB
    # Algorithm Configuration
    maxIterations = 100
    maxTabuCount = 15
    maxCandidates = 50

    # Problem Configuration
    berlin52 = [[565,575],[25,185],[345,750],[945,685],[845,655],
                [880,660],[25,230],[525,1000],[580,1175],[650,1130],[1605,620],
                [1220,580],[1465,200],[1530,5],[845,680],[725,370],[145,665],
                [415,635],[510,875],[560,365],[300,465],[520,585],[480,415],
                [835,625],[975,580],[1215,245],[1320,315],[1250,400],[660,180],
                [410,250],[420,555],[575,665],[1150,1160],[700,580],[685,595],
                [685,610],[770,610],[795,645],[720,635],[760,650],[475,960],
                [95,260],[875,920],[700,500],[555,815],[830,485],[1170,65],
                [830,610],[605,625],[595,360],[1340,725],[1740,245]]

    # Execute the algorithm
    result = search(berlin52, maxIterations, maxTabuCount, maxCandidates)

    print "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print "FINAL RESULT\n"
    print result
