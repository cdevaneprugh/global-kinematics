from math import radians, pi, sqrt
from shared_utils import get_velocity_components
from local_projectile_utils import local_solution, approximate, get_gcs_coords

# launches in the objects local reference frame
# assumes a semi flat earth model (drop due to curvature is still accounted for)

class local_projectile():
    
    def __init__(self, gcs0=[0,0,0], v0=100, alt_az=[45,90], D=0.1, m=1, Cd=0.47):
        
        # r0 in a local reference frame
        self.r0 = [0,0,gcs0[2]]
        
        # initial lat/lon in radians
        self.lat0, self.lon0 = radians(gcs0[0]), radians(gcs0[1])
        
        # velocity components using alt/az angle convention
        self.v0 = get_velocity_components(v0, alt_az)
        
        # projectile properties for calculating drag
        self.A = pi * (D/2)**2 # cross sectional area
        self.m = m                # mass
        self.Cd = Cd              # drag coefficient
        
    # given initial values, launch and see where the projectile lands
    def launch_to_impact(self, dt=0.01, omega=7.29e-5, approx=True):
        
        # numerical solution
        self.solution = local_solution(self.r0, self.v0, dt, self.lat0, self.A, self.m, self.Cd, omega)
        
        # convert to gcs
        self.gcs_soln = [[],[],[]]
        for i in range(len(self.solution[2])):
            lat, lon = get_gcs_coords(self.solution[0][i], self.solution[1][i], self.lat0, self.lon0)
            
            self.gcs_soln[0].append(lat)
            self.gcs_soln[1].append(lon)
            self.gcs_soln[2].append(self.solution[2][i])
            
        # run approximations for testing
        if approx == True:
            # vacuum
            self.vacuum_approximation = approximate(self.r0, self.v0, dt, self.lat0, omega=0)
        
            # 1st order coriolis
            self.coriolis_approximation = approximate(self.r0, self.v0, dt, self.lat0, omega)
    
    
    def flight_time(self):
        return self.solution[3][-1]
    
    def max_height(self):
        return max(self.solution[2])
    
    def distance_travelled(self):
        return sqrt( self.solution[0][-1]**2 + self.solution[1][-1]**2 )