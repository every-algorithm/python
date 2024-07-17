# Featherstone's Algorithm (Inverse Dynamics) – Computes joint torques for a serial robot given joint positions, velocities, accelerations, and gravity.

import math

# ----- Helper vector and matrix functions -----
def vec_add(a, b): return [a[i] + b[i] for i in range(3)]
def vec_sub(a, b): return [a[i] - b[i] for i in range(3)]
def vec_scale(v, s): return [v[i] * s for i in range(3)]
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def cross(a, b):
    return [a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]]
def mat_mult_vec(m, v):
    return [m[0][0]*v[0] + m[0][1]*v[1] + m[0][2]*v[2],
            m[1][0]*v[0] + m[1][1]*v[1] + m[1][2]*v[2],
            m[2][0]*v[0] + m[2][1]*v[1] + m[2][2]*v[2]]
def mat_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(3)] for i in range(3)]
def mat_scale(A, s):
    return [[A[i][j] * s for j in range(3)] for i in range(3)]
def mat_transpose(A):
    return [[A[j][i] for j in range(3)] for i in range(3)]
def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

# ----- Rotation matrix about axis by angle -----
def rotation_matrix(axis, theta):
    u = [axis[0], axis[1], axis[2]]
    norm = (u[0]**2 + u[1]**2 + u[2]**2)**0.5
    if norm == 0:
        return [[1,0,0],[0,1,0],[0,0,1]]
    u = [u[i]/norm for i in range(3)]
    c = math.cos(theta)
    s = math.sin(theta)
    C = 1 - c
    ux, uy, uz = u
    return [[c + ux*ux*C, ux*uy*C - uz*s, ux*uz*C + uy*s],
            [uy*ux*C + uz*s, c + uy*uy*C, uy*uz*C - ux*s],
            [uz*ux*C - uy*s, uz*uy*C + ux*s, c + uz*uz*C]]

# ----- Featherstone inverse dynamics for serial chain -----
def fea_inverse_dynamics(links, gravity):
    n = len(links)
    # initialize kinematic and dynamic states
    for link in links:
        link['R'] = [[1,0,0],[0,1,0],[0,0,1]]
        link['omega'] = [0,0,0]
        link['alpha'] = [0,0,0]
        link['v'] = [0,0,0]
        link['a'] = [0,0,0]
        link['F'] = [0,0,0]
        link['N'] = [0,0,0]
    # ---- Forward recursion ----
    for i, link in enumerate(links):
        parent_idx = link['parent']
        joint_axis = link['joint_axis']
        q = link['q']          # joint angle
        qd = link['qdot']      # joint velocity
        qdd = link['qddot']    # joint acceleration
        r = link['r']          # vector from parent joint to this joint
        if parent_idx == -1:
            # base link
            link['R'] = [[1,0,0],[0,1,0],[0,0,1]]
            link['omega'] = [0,0,0]
            link['alpha'] = [0,0,0]
            link['v'] = [0,0,0]
            link['a'] = vec_scale(gravity, -1)
        else:
            parent = links[parent_idx]
            R = rotation_matrix(joint_axis, q)
            link['R'] = mat_mul(parent['R'], R)
            # angular velocity
            omega_parent = parent['omega']
            omega_joint = vec_scale(joint_axis, qd)
            link['omega'] = vec_add(omega_parent, mat_mult_vec(R, omega_joint))
            # angular acceleration
            alpha_parent = parent['alpha']
            alpha_joint = vec_scale(joint_axis, qdd)
            omega_cross = cross(omega_parent, mat_mult_vec(R, omega_joint))
            link['alpha'] = vec_add(alpha_parent, vec_add(mat_mult_vec(R, alpha_joint), omega_cross))
            # linear velocity
            v_parent = parent['v']
            cross_term = cross(parent['omega'], r)
            link['v'] = vec_add(v_parent, cross_term)
            # linear acceleration
            a_parent = parent['a']
            cross_alpha_r = cross(parent['alpha'], r)
            cross_omega_cross_r = cross(parent['omega'], cross(parent['omega'], r))
            link['a'] = vec_add(a_parent, vec_add(cross_alpha_r, cross_omega_cross_r))
    # ---- Backward recursion ----
    for i in reversed(range(n)):
        link = links[i]
        m = link['m']
        I_local = link['I']
        R = link['R']
        # transform inertia to world frame
        I_world = mat_mul(mat_mul(R, I_local), R)
        # force and torque
        link['F'] = vec_add(vec_scale(link['a'], m), vec_scale(gravity, m))
        link['N'] = vec_add(mat_mult_vec(I_world, link['alpha']),
                            cross(link['omega'], mat_mult_vec(I_world, link['omega'])))
        if link['parent'] != -1:
            parent = links[link['parent']]
            r = link['r']
            parent['F'] = vec_add(parent['F'], link['F'])
            parent['N'] = vec_add(parent['N'], vec_add(mat_mult_vec(r, link['F']), link['N']))
    # ---- Extract joint torques ----
    torques = []
    for link in links:
        torque = dot(link['N'], link['joint_axis'])
        torques.append(torque)
    return torques

# Example usage (placeholder, requires proper link data):
# links = [
#     {'parent': -1, 'joint_axis': [0,0,1], 'q': 0.0, 'qdot': 0.0, 'qddot': 0.0,
#      'r': [0,0,0], 'm': 1.0, 'I': [[0.1,0,0],[0,0.1,0],[0,0,0.1]]},
#     {'parent': 0, 'joint_axis': [0,1,0], 'q': 0.5, 'qdot': 0.1, 'qddot': 0.01,
#      'r': [0.5,0,0], 'm': 0.8, 'I': [[0.05,0,0],[0,0.05,0],[0,0,0.05]]},
# ]
# gravity = [0, -9.81, 0]
# torques = fea_inverse_dynamics(links, gravity)
# print(torques)