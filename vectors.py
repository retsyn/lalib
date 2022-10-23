'''
vectors.py
Created: Friday, 14th October 2022 8:56:27 am
Matthew Riche
Last Modified: Friday, 14th October 2022 8:56:46 am
Modified By: Matthew Riche
'''

# This module leverages MVector from om2 to provide vector math that is strong against FPP errors.

from maya.api.OpenMaya import MVector
import maya.cmds as cmds
import logging as log

def cross_prod(vector1, vector2):
    """Get the cross product of two vectors.
    Args will be sanitized to precise MVectors and returned as such.

    Args:
        vector1 (iterable): Any "vector-esce" iterable.
        vector2 (iterable): Any "vector-esce" iterable.

    Returns:
        MVector: Cross product vector.
    """    

    vector1 = _sanitize_vector(vector1)
    vector2 = _sanitize_vector(vector2)

    cross_prod = vector1 ^ vector2

    return cross_prod

def dot_prod(vector1, vector2):
    """Returns the dot product or "inner product" of 2 line vectors.

    Args:
        vector1 (iterable): Line Vector
        vector2 (iterable): Second Line Vector

    Returns:
        Float: Degrees of angle between two line vectors.
    """    

    print(vector1)
    print(vector2)
    vector1 = _sanitize_vector(vector1)
    vector2 = _sanitize_vector(vector2)
    print(type(vector1))
    print(vector2)

    return (vector1 * vector2)

def best_fit_from_plane():
    pass
    # TODO
    '''
    	# Initialize plane normal
	norm = OpenMaya.MVector()
	
	# Get Point Positions
	ptList = [glTools.utils.base.getPosition(p) for p in ptList]
	
	# Calculate Plane Normal
	for i in range(len(ptList)):
		prev = OpenMaya.MVector(ptList[i-1][0],ptList[i-1][1],ptList[i-1][2])
		curr = OpenMaya.MVector(ptList[i][0],ptList[i][1],ptList[i][2])
		norm += OpenMaya.MVector((prev.z + curr.z) * (prev.y - curr.y), (prev.x + curr.x) * (prev.z - curr.z), (prev.y + curr.y) *  (prev.x - curr.x))
	
	# Normalize result
	norm.normalize()
    '''
    
def plane_normal(point_a, point_b, point_c):
    """Get a normal angle from a plane defined by three points.

    Args:
        point_a (iterable): Point A comprised by plane
        point_b (iterable): Point B comprised by plane
        point_c (iterable): Point C comprised by plane

    Returns:
        MVector: Line vector normal of the plane.
    """    

    point_a = _sanitize_vector(point_a)
    point_b = _sanitize_vector(point_b)
    point_c = _sanitize_vector(point_c)

    return ((point_c - point_a) * (point_b - point_c))

def get_line_vector(point_a, point_b, reversed=False):
    """Get a single vector represting the line vector.

    Args:
        point_a (iterable): First point on the line.
        point_b (iterable): End point on the line.
        reversed (bool, optional): To give the reversed line. Defaults to False.

    Returns:
        MVector: A line vector
    """    

    point_a = _sanitize_vector(point_a)
    point_b = _sanitize_vector(point_b)
    if(reversed):
        return point_b - point_a
    else:
        return point_a - point_b


def _sanitize_vector(vector):
    """Makes sure other types that express vectors are turns into MVectors safely before any math is
    done on them.  MVector is our protection against FPP errors.

    Args:
        vector (list, tuple, MVector): A vector expressed as anything reasonably vector-like.

    Raises:
        ValueError: If the wrong number of values is in the given iterable.
        TypeError: If a non-numerical type is in the given iterable.
        TypeError: If the vector argument isn't even iterable.

    Returns:
        MVector: Returns OpenMaya's MVector class from whatever was provided.
    """    

    # MVector itself can accept a lot of incoming data sanely, so a basic re-cast first.
    try:
        sanitized_vec = MVector(vector)
    except ValueError:
        # Raise an exception explaining why the above failed.
        if(type(vector) in [list, tuple]):
            if(len(vector) != 3):
                raise ValueError("Can't sanitize {} as a vector: number of elements is not 3."
                    .format(vector))
            else:
                for element in vector:
                    if(type(element) not in [float, int, complex]):
                        raise TypeError("Can't sanitize {}, {} not a number."
                            .format(vector, element))
                # Logically if the exception was thrown, one of the above tests should have failed.
                # But, also "logically", if they have passed somehow, it's worth casting as MVector.
                sanitized_vec = MVector(vector)
        else:
            raise TypeError("{} can't be interpreted as a vector at all.".format(vector))
    
    return sanitized_vec