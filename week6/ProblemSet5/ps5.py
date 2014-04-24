# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."
    from pprint import pprint
    with open(mapFilename) as f:
        map = WeightedDigraph()
        nodes = set([])
        for line in f.readlines():
            src, dest, total, outdoor = line.split()
            try:
                srcNode = Node(src)
                map.addNode(srcNode)
            except ValueError:
                pass
            try:
                destNode = Node(dest)
                map.addNode(destNode)
            except ValueError:
                pass
            edge = WeightedEdge(srcNode, destNode, total, outdoor)
            map.addEdge(edge)
            #print src,dest,total,outdoor
            #pprint(map.edges)
            #raw_input("Press Enter to continue...")
        f.close()
    return map

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    def printPath(path):
        result = ''
        for i in range(len(path)):
            result = result + str(path[i])
            if i != len(path) - 1:
                result = result + '->'
        return result

    def pathDist(graph,path):
        totalDist = 0.0
        outdoorDist = 0.0
        for i in range(len(path) - 1):
            srcEdges = graph.edges[path[i]]
            pathFound = False
            for d in srcEdges:
                if d[0] == path[i+1]:
                    pathFound = True
                    totalDist += d[1][0]
                    outdoorDist += d[1][1]
            if not pathFound:
                return 0.0, 0.0
        return totalDist, outdoorDist

    def DFS(graph, start, end, path, shortest):
        path = path + [start]
        pd1, pd2 = pathDist(graph,path)
        if pd1 > 0.0:
            print "Current DFS path:",printPath(path), "Dist:",pathDist(graph,path)
        if start == end:
            return path
        for node in graph.childrenOf(start):
            if node not in path: # avoid cycles
                if shortest == None: # or pathTotalDist < sTotalDist:
                    newPath = DFS(graph, node, end, path, shortest)
                    if newPath != None:
                        pathTotalDist, pathOutsideDist = pathDist(graph,path)
                        sTotalDist = None
                        if shortest != None:
                            sTotalDist, sOutsideDist = pathDist(graph,shortest)
                        print "current path dist",pathTotalDist, "shortest path dist",sTotalDist
                        shortest = newPath
        return shortest
    

    totalDist = 0.0
    outdoorDist = 0.0
    path = []
    
    dfs = DFS(digraph,Node(start),Node(end), [], None)
    totalDist, outdoorDist = pathDist(digraph, dfs)
    print "dfs, totaldist, outdoordist", dfs, totalDist,outdoorDist
    if totalDist > maxTotalDist:
        raise ValueError("total distance exceeded")
    if outdoorDist > maxDistOutdoors:
        raise ValueError("outdoor distance exceeded")
    strdfs = [str(d) for d in dfs]
    return strdfs

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    pass


# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':

# Pb 1 tests
    '''
    g = WeightedDigraph()
    na = Node('a')
    nb = Node('b')
    nc = Node('c')
    g.addNode(na)
    g.addNode(nb)
    g.addNode(nc)
    e1 = WeightedEdge(na, nb, 15, 10)
    print e1
    print e1.getTotalDistance()
    print e1.getOutdoorDistance()
    e2 = WeightedEdge(na,nc,14,6)
    e3 = WeightedEdge(nb,nc,3,1)
    print e2
    print e3
    g.addEdge(e1)
    g.addEdge(e2)
    g.addEdge(e3)
    print g
    print g.childrenOf(e1)

    # Pb 1 test 5
    nh = Node('h')
    nj = Node('j')
    nk = Node('k')
    nm = Node('m')
    ng = Node('g')
    g = WeightedDigraph()
    g.addNode(nh)
    g.addNode(nj)
    g.addNode(nk)
    g.addNode(nm)
    g.addNode(ng)
    randomEdge = WeightedEdge(nm, nh, 66, 44)
    g.addEdge(randomEdge)
    randomEdge = WeightedEdge(nm, nh, 37, 37)
    g.addEdge(randomEdge)
    randomEdge = WeightedEdge(nh, nm, 23, 11)
    g.addEdge(randomEdge)
    randomEdge = WeightedEdge(nh, nk, 83, 20)
    g.addEdge(randomEdge)
    randomEdge = WeightedEdge(nh, nk, 31, 24)
    g.addEdge(randomEdge)
    randomEdge = WeightedEdge(nm, nk, 13, 5)
    g.addEdge(randomEdge)
    randomEdge = WeightedEdge(nh, nm, 17, 15)
    g.addEdge(randomEdge)
    randomEdge = WeightedEdge(nm, nh, 68, 27)
    g.addEdge(randomEdge)
    print g.childrenOf(nh), "should be [m,k,k,m]"
    print g.childrenOf(nj), "should be []"
    from pprint import pprint
    pprint (g.edges)

    #     Test cases
    from pprint import pprint
    mitMap = load_map("mit_map.txt")
    print isinstance(mitMap, Digraph)
    print isinstance(mitMap, WeightedDigraph)
    print 'nodes', mitMap.nodes
    #pprint (mitMap.edges)
    print mitMap.edges


    LARGE_DIST = 1000000
    from pprint import pprint
    mitMap = load_map("mit_map.txt")
    pprint (mitMap.edges)

    #     Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)

    #     dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print bruteForceSearch(mitMap, '57', '68', LARGE_DIST, LARGE_DIST)

    #     print "DFS: ", dfsPath1
    #print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)
    '''
    n1 = Node('1')
    n2 = Node('2')
    n3 = Node('3')
    n4 = Node('4')
    map2 = WeightedDigraph()
    map2.addNode(n1)
    map2.addNode(n2)
    map2.addNode(n3)
    map2.addNode(n4)
    map2.addEdge(WeightedEdge(n1,n2,10,5))
    map2.addEdge(WeightedEdge(n1,n4,15,1))
    map2.addEdge(WeightedEdge(n2,n3,8,5))
    map2.addEdge(WeightedEdge(n4,n3,8,5))
    print bruteForceSearch(map2,'1','3',18,18), "should be [1,2,3]"

    from pprint import pprint
    pprint (map2.edges)


#     Test case 2
#     print "---------------"
#     print "Test case 2:"
#     print "Find the shortest-path from Building 32 to 56 without going outdoors"
#     expectedPath2 = ['32', '36', '26', '16', '56']
#     brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
#     dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
#     print "Expected: ", expectedPath2
#     print "Brute-force: ", brutePath2
#     print "DFS: ", dfsPath2
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
#     print "---------------"
#     print "Test case 3:"
#     print "Find the shortest-path from Building 2 to 9"
#     expectedPath3 = ['2', '3', '7', '9']
#     brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath3
#     print "Brute-force: ", brutePath3
#     print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
#     print "---------------"
#     print "Test case 4:"
#     print "Find the shortest-path from Building 2 to 9 without going outdoors"
#     expectedPath4 = ['2', '4', '10', '13', '9']
#     brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
#     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
#     print "Expected: ", expectedPath4
#     print "Brute-force: ", brutePath4
#     print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
#     print "---------------"
#     print "Test case 5:"
#     print "Find the shortest-path from Building 1 to 32"
#     expectedPath5 = ['1', '4', '12', '32']
#     brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath5
#     print "Brute-force: ", brutePath5
#     print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
#     print "---------------"
#     print "Test case 6:"
#     print "Find the shortest-path from Building 1 to 32 without going outdoors"
#     expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
#     brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
#     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
#     print "Expected: ", expectedPath6
#     print "Brute-force: ", brutePath6
#     print "DFS: ", dfsPath6
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
#     print "---------------"
#     print "Test case 7:"
#     print "Find the shortest-path from Building 8 to 50 without going outdoors"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
#     print "---------------"
#     print "Test case 8:"
#     print "Find the shortest-path from Building 10 to 32 without walking"
#     print "more than 100 meters in total"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr
