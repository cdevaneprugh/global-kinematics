import numpy as np
from math import sin, cos, atan, atan2, degrees, radians, sqrt
from shared_utils import get_drag_force_const, get_gravity

###################################################################################################################

def ECEF_to_ENU(ECEF0, GCS0, ECEF):
    
    ECEF = ECEF - ECEF0
    lat, lon, h = GCS0
    
    rotation = [[ -sin(lon), cos(lon), 0],
                [-sin(lat)*cos(lon), -sin(lat)*sin(lon), cos(lat)],
                [ cos(lat)*cos(lon),  cos(lat)*sin(lon), sin(lat)]]
    
    ENU = [0,0,h] # h scales enu to have ground at zero
    
    for i in range(len(rotation)):
        for j in range(len(ECEF)):
            ENU[i] += rotation[i][j] * ECEF[j]
    
    return ENU
    
###################################################################################################################
    
def ENU_to_ECEF(ENU, GCS):
    
    lat, lon, h = GCS
    
    rotation = [[-sin(lon), -sin(lat)*cos(lon), cos(lat)*cos(lon)],
                [ cos(lon), -sin(lat)*sin(lon), cos(lat)*sin(lon)],
                [ 0, cos(lat), sin(lat)]]
    
    ECEF = [0,0,0] 
    
    for i in range(len(rotation)):
        for j in range(len(ENU)):
            ECEF[i] += rotation[i][j] * ENU[j]
            
    return ECEF
    
###################################################################################################################
    
def GCS_to_ECEF(GCS):
    
    lat, lon, h = GCS
    
    X = (6375e3+h) * cos(lat) * cos(lon)
    Y = (6375e3+h) * cos(lat) * sin(lon)
    Z = (6375e3+h) * sin(lat)
    
    return [X,Y,Z]

###################################################################################################################

def ECEF_to_GCS(ECEF):
    
    X, Y, Z = ECEF
    p = sqrt(X**2 + Y**2)
    
    lon = atan2(Y, X)
    lat = atan(Z / p)
    h = p / cos(lat) - 6375e3
    
    return [lat, lon ,h]

###################################################################################################################

def global_solution(gcs0, ecef0, v0, A, m, Cd, dt, omega):
    
    ############################################################################################
    
    def f(R):
        
        # ECEF components
        X, Y, Z, VX, VY, VZ = R
        
        # V magnitude
        V = np.sqrt( VX**2 + VY**2 + VZ**2 )
        
        # drag force and gravity
        C = get_drag_force_const(h, A, Cd)
        g = get_gravity(h)
        
        # velocity ode
        dR_dt = [VX, VY, VZ]
        
        # acceleration ode
        dVX_dt = -g*cos(lat)*cos(lon) - C/m*V*VX + 2*omega*VY
        dVY_dt = -g*cos(lat)*sin(lon) - C/m*V*VY - 2*omega*VX
        dVZ_dt = -g*sin(lat) - C/m*V*VZ
        
        dV_dt = [dVX_dt, dVY_dt, dVZ_dt]
        
        return np.asarray(dR_dt + dV_dt)
    
    ############################################################################################
    
    # set up ode initial conditions
    
    # GCS0 to ECEF0
    X0, Y0, Z0 = ecef0
    
    # convert ENU velocities to ECEF
    VX0, VY0, VZ0 = v0
    
    # package initial array
    R = np.array( [X0, Y0, Z0, VX0, VY0, VZ0] )
    
    ############################################################################################
    
    ECEF_soln = []
    GCS_soln = []
    times = []
    
    t = 0
    lat, lon, h = gcs0
    
    ############################################################################################
    
    while h >= 0:
        
        # create a copy of R instead of appending a pointer to the soln lists
        # python is stupid, you have to do this
        soln = R[:3].copy()
        
        # append data
        times.append(t) # time
        ECEF_soln.append(soln) # ECEF coordinates

        GCS = ECEF_to_GCS(soln) # convert to GCS
        GCS_soln.append(GCS)     # GCS coordinates
    
        # RK 4th order
        k1 = dt*f(R)
        k2 = dt*f(R + 0.5*k1)
        k3 = dt*f(R + 0.5*k2)
        k4 = dt*f(R + k3)
        R += (k1 + 2.*k2 + 2.*k3 + k4) / 6.
        
        # update loop variables
        t += dt
        lat, lon, h = GCS # in radians and meters
    
    ############################################################################################
    
    # convert gcs to degrees
    for i in range( len(GCS_soln) ):
        for j in range(2):
            GCS_soln[i][j] = degrees(GCS_soln[i][j])
    
    # convert ECEF results to ENU
    ENU_soln = []
    for i in range(len(ECEF_soln)):
        ENU_soln.append(ECEF_to_ENU(ecef0, gcs0, ECEF_soln[i]))
    
    # solns from tuples to lists
    ECEF_soln = np.asarray(ECEF_soln).T
    GCS_soln = np.asarray(GCS_soln).T
    ENU_soln = np.asarray(ENU_soln).T

    return ECEF_soln, GCS_soln, ENU_soln, times