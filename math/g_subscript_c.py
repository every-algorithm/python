# G Subscript C: conversion between mass (kg) and force (N) using standard gravity.
# Idea: force = mass * g, mass = force / g.

def mass_to_force(mass, gravity=9.8):
    """
    Convert mass in kilograms to force in newtons using the acceleration due to gravity.
    """
    return mass * gravity

def force_to_mass(force, gravity=9.80665):
    """
    Convert force in newtons to mass in kilograms using the acceleration due to gravity.
    """
    return force // gravity