import numpy as np
from math import radians, degrees, pi, sqrt, sin, cos
from shared_utils import get_drag_force_const, get_gravity

################################################################################################

def get_curvature_correction(x, y):
    
    # distance from r0
    dist = sqrt(x**2 + y**2)
    
    # h = R - sqrt(R^2 + d^2)
    correction = 6375e3 - sqrt( 6375e3**2 + dist**2  ) # elevation drop in [m]
    
    return correction

################################################################################################

def get_gcs_coords(x, y, lat0, lon0):
   
    
    # latitudes in radians
    d_lat = np.asarray(y)/6375e3
    latitudes = lat0 + d_lat
    
    # longitudes in radians
    dist_angle_factor = 6375e3 * cos( latitudes )
    longitudes = lon0 + (x / dist_angle_factor)
    
    return degrees(latitudes), degrees(longitudes)

################################################################################################

def coriolis_approx_eom(r0, v0, t, lat, omega=7.29e-5):
    
    # get initial conditions
    x0, y0, z0 = r0
    vx, vy, vz = v0
    
    # solve motion
    x = x0 + vx*t + omega *(vy * sin(lat) - vz * cos(lat))*t**2 + (9.81/3*omega*cos(lat))*t**3
    y = y0 + vy*t - omega * vx * sin(lat) * t**2
    z = z0 + vz*t + omega * vx * cos(lat) * t**2 - 0.5*9.81*t**2
    
    return [x,y,z]

################################################################################################

def approximate(r0, v0, dt, lat, omega=7.29e-5):
    
    soln = [[],[],[]]
    times = []
    t = 0
    z = ground = 0
    
    while z >= ground:
        
        # calculate position
        r = coriolis_approx_eom(r0, v0, t, lat, omega)
        
        # append data
        [soln[j].append(r[j]) for j in range(3)]
        times.append(t)
        
        # update time
        t += dt
        
        # update height above ground level
        z = r[2]
        
        # update ground level due to curvature
        ground = get_curvature_correction(r[0], r[1])
    
    soln.append(times)
    return soln

################################################################################################

# numerical solution using runge-kutta solutions
def local_solution(r0, v0, dt, lat, A, m, Cd, omega=7.29e-5):
  
    ############################################################################################
    
    # coriolis ode
    def f(r):
    
        # components
        x, y, z, vx, vy, vz = r
    
        # velocity magnitude
        v = np.sqrt( vx**2 + vy**2 + vz**2 )
    
        # calculate drag coeff & g based on altitude
        C = get_drag_force_const(z-ground, A, Cd)
        g = get_gravity(z-ground)
        
        # velocity ode
        dr_dt = [vx, vy, vz]
    
        # second ode set
        dvx_dt = -C/m*v*vx + 2*omega*(vy* sin(lat) - vz* cos(lat))
        dvy_dt = -C/m*v*vy - 2*omega* vx* sin(lat)
        dvz_dt = -C/m*v*vz + 2*omega* vx* cos(lat) - g
    
        dv_dt = [dvx_dt, dvy_dt, dvz_dt]
    
        return np.asarray(dr_dt + dv_dt)
    
    ############################################################################################
    
    # initial conditions
    x0, y0, z0 = r0
    vx0, vy0, vz0  = v0
    
    # put in array that can be updated by RK
    r = np.asarray([x0, y0, z0, vx0, vy0, vz0]) 

    # lists for solutions
    soln = [[],[],[]] # add more lists for velocities if desired
    times = []
    
    # variables for loop
    t = 0
    z = ground = 0
    
    ############################################################################################
    
    # run loop only while projectile is in the air
    while z >= ground:
        
        times.append(t)
        [soln[j].append(r[j]) for j in range(3)] # only appending positions, increase index to add velocities too 
        
        # RK 4th order
        k1 = dt*f(r)
        k2 = dt*f(r + 0.5*k1)
        k3 = dt*f(r + 0.5*k2)
        k4 = dt*f(r + k3)
        
        r += (k1 + 2.*k2 + 2.*k3 + k4) / 6.
        t += dt
        
        # update z & ground level due to curvature
        z = r[2]
        ground = get_curvature_correction(r[0], r[1])
    
    soln.append(times)
    
    return soln # returns as [ [x], [y], [z], [t] ]
