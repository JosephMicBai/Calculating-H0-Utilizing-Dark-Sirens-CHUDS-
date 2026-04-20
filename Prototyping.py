# -*- coding: utf-8 -*-
"""
Joseph Bailor

Program for Hubble Constant Calculation using Dark Siren Method
"""

# Import Libraries
import numpy as np

# Establish Constants
c = 3e8


class Observation:
    """
    Class representing a single observation from G-Wave observatory
    """
    def __init__(self, center, r, delta_omega, luminosity_distance, redshifts):
        self.center = center
        self.r = r
        self.delta_omega = delta_omega
        self.luminosity_distance = luminosity_distance
        self.velocities = [c*(((z+1)**2-1)/((z+1)**2+1)) for z in redshifts]
        self.error_volume = spherical_volume(self.r, [0, self.delta_omega/2], [0, 2*np.pi])
        if ((luminosity_distance == 0) or (luminosity_distance != luminosity_distance)):
            raise ValueError("Invalid value for luminosity_distance")
        self.Hubbles = np.empty(len(self.velocities))
        for i in range(len(self.velocities)):
            self.Hubbles[i] = self.velocities[i]/self.luminosity_distance
    
    def check_galaxy(self, galaxy):
        ra_bounds = [(self.center[0] - self.delta_omega/2), (self.center[0] + self.delta_omega/2)]
        dec_bounds = [(self.center[1] - self.delta_omega/2), (self.center[1] + self.delta_omega/2)]
        if (((galaxy.coords[0] >= ra_bounds[0]) and (galaxy.coords[0] <= ra_bounds[1])) and ((galaxy.coords[1]) >= dec_bounds[0] and (galaxy.coords[1]) <= dec_bounds[1]) and ((galaxy.luminosity_distance >= self.r[0]) and (galaxy.luminosity_distance <= self.r[1]))):
            return True
        else:
            return False
            
class Galaxy:
    def __init__(self, coords, z, luminosity_distance):
        self.coords = coords
        self.ra = coords[0]
        self.dec = coords[1]
        self.z = z
        self.luminosity_distance = luminosity_distance
        self.velocity = c*(((z+1)**2-1)/((z+1)**2+1))
        

def spherical_volume(r, theta, phi):
    
    theta_component = -np.cos(theta[1]) + np.cos(theta[0])
    
    r_component = r[1]**3/3 - r[0]**3/3
    
    phi_component = phi[1] - phi[0]
    
    integral = theta_component*r_component*phi_component
    return integral


def compare_Observations(Observations):
    if len(Observations) < 2:
        raise ValueError("Size of Observation sequence is too small - you need at least two observations to compare them")
    
    count = 0
    # count variable used to keep track of the amount of observations in agreement with one another
    check = 0
    # check variable used to determine if no hubble constants are similar between two observations
    H_0 = float('NaN')
    # H_0 variable used to store the hubble constant common to all observations
    
    for i in range(len(Observations[0].Hubbles)):
        # For every hubble constant value H0_i in the first observation O_0 (O0_Hi)
        O0_Hi = Observations[0].Hubbles[i]
        for j in range(len(Observations)-1):
            j += 1
            # For every other observation O_j
            for m in range(len(Observations[j].Hubbles)):
                # For every hubble constant value H0_m in O_j (Oj_Hm)
                Oj_Hm = Observations[j].Hubbles[m]
                if (O0_Hi == Oj_Hm):
                    # Check to see if O0_Hi is equal to Oj_Hm. If so, set H_0 = O0_Hi and increment count to indicate a match
                    H_0 = O0_Hi
                    count += 1
                    break
            if (check == count):
                # Check to see if a match was not found. If that is the case, reset both count and check
                count = 0
                check = 0 
                break
            else:
                # If a match was found, update the check counter
                check = count
        if (count == len(Observations)-1):
            break
        
    if(count != len(Observations)-1):
        # Check to see if a match was not found for every Observation. If so, reset H_0
        H_0 = float("NaN")
        
    if (H_0 != H_0):
        print("No Hubble Constant value common to all Observations")
        
    return H_0
            
    

O1 = Observation([12, 45], [1, 2], 2, 1, [1.5, 1.2, 1.3])
O2 = Observation([18, -45], [1, 2], 2, 1, [1.7, 1.5, 1.8])

G1 = Galaxy([12.3, 44.2], 1, 1.5)

print(compare_Observations([O1, O2]))
print(O1.check_galaxy(G1))
print(O2.check_galaxy(G1))