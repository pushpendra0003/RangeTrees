import csv
import os
    
class Node(object):
    '''A Node in the Range Tree'''

    def __init__(self, value) -> None:
        self.value = value
        self.left = None
        self.right = None
        self.isLeaf = False
        self.assoc = None # Pointer to the Y-Tree

def LoadData(dim):

    '''
    Loads the data from a CSV file into the program
    Arguments:
        dim         : Dimensions of the data taken as input from the user.
    Returns:
        A List containing the data collected from the CSV File
    '''

    if dim == 2:

        with open("Data.csv") as csvfile: # File containing 2D Data Points
            readCSV = csv.reader(csvfile, delimiter=",")
            readCSV = list(readCSV)

            for i in range(0, len(readCSV)):
                for j in range(0, 2):
                    readCSV[i][j] = eval(readCSV[i][j])

    else:

        with open("Data1.csv") as csvfile: # File containing 1D Data Points
            readCSV = csv.reader(csvfile)
            readCSV = list(readCSV)

            for i in range(0, len(readCSV)):
                readCSV[i] = eval(readCSV[i][0])

    return readCSV

def withinRange(point, range, dim):

    '''
    Checks if the value of node is within the required range
    Arguments:
        point       : Any point in the tree
        range       : The Required Range
        dim         : Dimension of the data to be checked
    Returns :
        True if the point falls within the specified range
    '''

    if dim == 1:

        if (point >= range[0][0]  and point <= range[0][1] ) :
            return True
        
        else:
            return False
        
    elif dim == 2:
        x = point[0]
        y = point[1]

        if (x >= range[0][0]   and x <= range[0][1]  and y >= range[1][0]  and y <= range[1][1] ) :
            return True
        
        else:
            return False
        
        
def getValue (node:Node, dim, enable):

    '''
    Gets the value stored in a node in the Range Tree
    Arguments:
        node        : The node whose value is needed
        dim         : Dimension of the data
        enable      : 1 if X Coordinate is required, 0 if Y Coordinate is required
    '''
    if dim == 1:
        value = node.value

    elif dim == 2:

        if enable:
            value = node.value[0]

        else:
            value = node.value[1]

    return value

        
def FindSplitNode(root, p1 , p2, dim, enable):

    '''
    Finds the Split Node in the Range Tree i.e., whose both left and right subtrees might contain points in the required range
    Arguments:
        root        : Root of the Range Tree
        p1          : Min value of the Required Range
        p2          : Max value of the required 
        dim         : Dimension of the data (always 1 for 1D Range Tree).
        enable      : 1 if X Coordinate is required, 0 if Y Coordinate is required  
    Returns:
        The Split Node in the Ramge Tree   
    '''

    splitnode = root

    while splitnode != None:
        node = getValue(splitnode, dim, enable)

        if p1 < node:
            splitnode = splitnode.left

        elif p1 > node:
            splitnode = splitnode.right

        elif p1 <= node <= p2:
            break

    return splitnode


def SearchRangeTree1d (tree, p1, p2, dim = 1, enable = True):

    '''
    Searches a 1D Range Tree for points within a specified range.
    Arguments:
        tree        : The root node of the 1D Range Tree.
        p1          : Minimum value of the query range.
        p2          : Maximum value of the query range.
        dim         : Dimension of the data (always 1 for 1D Range Tree).
        enable      : 1 if X Coordinate is required, 0 if Y Coordinate is required

    Returns:
        A list of points within the query range.
    '''
    nodes = []
    splitnode = FindSplitNode(tree , p1, p2, dim, enable) # Finding the Split Node

    if splitnode == None:
        return nodes
    
    elif withinRange(getValue(splitnode, dim, enable) , [(p1, p2)], 1):
        nodes.append(splitnode.value)

    nodes += SearchRangeTree1d(splitnode.left, p1, p2, dim, enable) # Traversing the left Subtree
    nodes += SearchRangeTree1d(splitnode.right, p1, p2, dim, enable) # Traversing the left Subtree

    return nodes

def SearchRangeTree2d (tree, x1, x2, y1, y2, dim ):
    '''
    Searches a 2D Range Tree for points within a rectangular query range.
    Arguments:
        tree        : The root node of the 2D Range Tree.
        x1          : Minimum x-value of the query range.
        x2          : Maximum x-value of the query range.
        y1          : Minimum y-value of the query range.
        y2          : Maximum y-value of the query range.
        dim         : Dimension of the data (always 2 for 2D Range Tree).

    Returns:
        A list of points within the query range.
    '''

    results = []
    splitnode = FindSplitNode(tree, x1, x2, 2, True) # Finding the Split Node

    if (splitnode == None):
        return results
    
    if withinRange(splitnode.value, [[x1, x2], [y1, y2]], 2) :
        results.append(splitnode.value)

    vl = splitnode.left 
    while ( vl != None ):

        if withinRange(vl.value, [[x1, x2], [y1, y2]], 2):
            results.append(vl.value)

        if (x1 < vl.value[0]):
            if vl.right != None:
                results += SearchRangeTree1d(vl.right.assoc, y1, y2, dim, False)

            vl = vl.left

        else:
            vl = vl.right

    vr = splitnode.right

    while ( vr != None ):

        if withinRange(vr.value, [(x1, x2), (y1, y2)], 2):
                results.append(vr.value)

        if ( x2 > vr.value[0] ):
            if vr.left != None:
                results += SearchRangeTree1d(vr.left.assoc, y1, y2, dim, False)

            vr = vr.right

        else:
            vr = vr.left
    
    return results

def ConstructRangeTree1d(data):

    '''
    Constructs a 1D Range Tree from a sorted list of data points.
    Arguments:
        data: A sorted list of data points (numerical values).

    Returns:
        The root node of the constructed 1D Range Tree.
    '''
    
    data.sort()

    if not data:
        return None
    
    if len(data) == 1:
        node = Node(data[0])
        node.isLeaf = True

    else:
        mid_val = len(data)//2
        node = Node(data[mid_val])
        node.left = ConstructRangeTree1d(data[:mid_val])
        node.right = ConstructRangeTree1d(data[mid_val+1:])

    return node

def ConstructRangeTree2d(data, enable=True):

    '''
    Constructs a 2D Range Tree from a list of data points.
    Args:
        data: A list of data points, each point represented as a tuple (x, y).
        enable: Flag to enable building the secondary y-axis trees (optional).

    Returns:
        The root node of the constructed 2D Range Tree.
    '''
    data.sort(reverse = False, key=lambda x: x[0])

    if not data:
        return None
    
    if len(data) == 1:
        node = Node(data[0])
        node.isLeaf = True

    else:
        mid_val = len(data)//2
        node = Node(data[mid_val]) 
        node.left = ConstructRangeTree2d(data[:mid_val], enable)
        node.right = ConstructRangeTree2d(data[mid_val+1:], enable)

    if enable:
        node.assoc = ConstructRangeTree2d( sorted(data, key=lambda x: x[1]), enable=False)

    return node

dim = int(input("Dimension of the data: "))
data = LoadData(dim)

if dim == 1:
    node = ConstructRangeTree1d(data)
    mn = int(input("Give Min Value: "))
    mx = int(input("Give Max Value: "))
    ans = SearchRangeTree1d(node, mn, mx, 1, True)

else:
    node = ConstructRangeTree2d(data)
    mnx = int(input())
    mny = int(input())
    mxx = int(input())
    mxy = int(input())
    ans = SearchRangeTree2d(node, mnx, mxx, mny, mxy, dim)

print("points" , ans)