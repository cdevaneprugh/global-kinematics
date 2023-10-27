import numpy as np

############################################################################################

# calculate velocity components using alt/az convention
def get_velocity_components(v, alt_az):
    
    # angles = [altitude, azimuth]
    alt, az = np.radians(alt_az)
    
    # find angles
    vx = v * np.sin(az) * np.cos(alt)
    vy = v * np.cos(az) * np.cos(alt)
    vz = v * np.sin(alt)
    
    return [vx, vy, vz]

############################################################################################

# height is height above ground
# need to account for drop due to curvature (probably not in flat approx though)
def get_air_density(height):
    return 1.225 * np.exp(-height/8500)

############################################################################################

# calculate the constant for the drag force at a specific altitude
# C = 1/2 * air_density * drag_coefficient * cross_sectional_area
# it's everything in the drag equation except the velocity

def get_drag_force_const(height, A, Cd = 0.47):
    rho = 1.225 * np.exp(-height/8500)
    return 0.5 * rho * Cd * A

############################################################################################

# force of gravity from height
def get_gravity(height):
    return 6.6743e-11 * 5.9722e24 / (6375e3 + height)**2

############################################################################################

# gcs coord export for simplekml
# should be in [lon, lat, h]
def export_gcs_coord(gcs_soln):
    
    gcs_export = []
    for i in range( len(gcs_soln[0]) ):
        gcs_export.append([gcs_soln[1][i], gcs_soln[0][i], gcs_soln[2][i]])
    
    return gcs_export