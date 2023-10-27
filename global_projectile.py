from math import radians, pi
from shared_utils import get_velocity_components
from global_projectile_utils import GCS_to_ECEF, ENU_to_ECEF, global_solution

class global_projectile():
    def __init__(self, gcs0, v0, alt_az, D, m, Cd):
        
        # initial positions
        self.gcs0 = [ radians(gcs0[0]), radians(gcs0[1]), gcs0[2] ] # lat/lon to radians
        self.ecef0 = GCS_to_ECEF(self.gcs0) # gcs to ecef
        
        # initial velocity components
        self.v0_enu = get_velocity_components(v0, alt_az) # local reference frame
        self.v0_ecef = ENU_to_ECEF(self.v0_enu, self.gcs0) # in ecef coords
        
        # projectile constants
        self.A = pi * (D/2)**2
        self.m = m
        self.Cd = Cd

    def launch_to_impact(self, dt=0.01, omega=7.29e-5):
        
        self.ecef_soln, self.gcs_soln, self.enu_soln, self.times = global_solution(self.gcs0, self.ecef0, self.v0_ecef, \
                                                                                   self.A, self.m, self.Cd, dt, omega)
    
    def flight_time(self):
        return self.times[-1]
    
    def max_height(self):
        return max(self.gcs_soln[2])