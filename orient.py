'''
orient.py
Created: Monday, 17th October 2022 10:25:40 am
Matthew Riche
Last Modified: Monday, 17th October 2022 10:25:45 am
Modified By: Matthew Riche
'''

from maya.api.OpenMaya import MVector, MMatrix
import maya.cmds as cmds

from . import vectors as vc

def get_average_xform(nodes):
    """Find a point vector that is the average of all given components or transforms.

    Args:
        nodes (iterable): iterable of str names of nodes in a maya scene.

    Raises:
        ValueError: If a node passed inside the iterable has not defined transform data.

    Returns:
        MVector: point vector at the average location of all given nodes.
    """    

    x_values = []
    y_values = []
    z_values = []

    # Sanitize against position-less node.
    for node in nodes:
        try:
            position = MVector(cmds.xform(node, q=True, t=True, ws=True))
        except ValueError:
            raise ValueError("Provided node {} doesn't have transform to average.".format(node))

        x_values.append(position.x)
        y_values.append(position.y)
        z_values.append(position.z)

    x_avg = sum(x_values) / len(x_values)
    y_avg = sum(y_values) / len(y_values)
    z_avg = sum(z_values) / len(z_values)

    return MVector(x_avg, y_avg, z_avg)


def aim_at(subject, target, up_vector=(0.0, 0.0, 1.0), aim_axis=0, up_axis=2):

    # Sanitize node arguments:
    for node in [subject, target]:
        if(cmds.objectType(node) not in ['transform', 'joint']):
            raise TypeError ("Can only run on nodes with transform data.  {} does not have "
                "transform data.".format(node))

    fix_determinant = False

    subject_pos = vc._sanitize_vector(cmds.xform(subject, q=True, t=True, ws=True))
    target_pos = vc._sanitize_vector(cmds.xform(target, q=True, t=True, ws=True))

    aim_vec = target_pos - subject_pos
    aim_vec.normalize()

    up_vec_recalc = MVector(up_vector)
    up_vec_recalc.normalize()

    last_vec = vc.cross_prod(up_vec_recalc, aim_vec)
    last_vec.normalize()

    # Check if combination of aim and up axis will result in negative determinants:
    nd_combos = [(0,1), (1,2), (2,0)]
    if((aim_axis, up_axis) in nd_combos):
        fix_determinant = True

    up_vec_recalc = vc.cross_prod(up_vector, last_vec)
    up_vec_recalc.normalize()

    





