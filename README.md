# global-kinematics

## Overview
A collection of python packages to explore kinematic motion on a global scale. Includes multiple trajectory calculation methods, variable atmospheric density, quadratic drag, variable planet rotation rate, height dependent gravity, and coordinate conversion methods to switch reference frames. For approximaitons of motion, we use analytically derived equatoins of motion. For full, numerical solutions, we use 4th order runge-kutta techniques to integrate our differential equations.

There are two classes that ship with this code, local_projectile and global_projectile. Both assume a perfectly spherical Earth, with a radius of $3753$ km. The first calculates the projectile motion from a local reference frame. The local reference frame uses the ENU convention where $E=x$, $N=y$, and $U=z$. From the local reference frame, we actually assume a semi-flat Earth model. It accounts for drop due to curvature, but does not account for changing latitude (crucial for accurate coriolis calculation), or changing angle of our gravity vector. The results will be skewed if our projectile travels a significant amount of Earth's surface. However, it is a reasonable approximation within a few hundred kilometers.

The global_projectile class calculates motion from the Earth centered Earth fixed (ECEF), geocentric reference frame. This class accounts for changing latitude, and gravity vector. As such, it is the most accurate method for calculating long range, sub orbital trajectories. This class also provides a method to convert our geocentric solution to GCS coordinates, and motion viewed from a local reference frame, with the origin at the launch site.

Depending on the size of your trajectory, and desired answer accuracy, different models of projectile motion are appropriate. Each of these models are useful in their domain, but breakdown at a certain point. The goal of this project is to model different equations of motion on a global scale and tease out when each model reaches its limit.

## Getting Started
Start by creating either a global or local projectile. You need to specify the initial gcs position of the object in the form of a tuple ($gcs0 = [lat,lon,height]$). The initial velocity in meters per second. The launch angle where the altitude is measured above the local horizon, and the azimuth is measured North to East. For example $[45,90]$ would be $45$ degrees above the horizon and $90$ degrees East. You also need to specify the object's diameter $[m]$, mass $[kg]$, and drag coefficient. The launch_to_impact method will "launch" your projectile and calculate the motion while above the ground.

The global_projectile calculates solutions for ECEF, GCS, and ENU coordinate systems. These can be accessed with your_projectile.ECEF_soln, .GCS_soln, or .ENU_soln. Similarly, the local_projectile solution is accessed at your_projectile.solution. In addition to the numerical solution, the local_projectile has an analytically derived equation of motion which can be calculated in parallel to your numerical solution. It is a first order approximation of projectile motion with the coriolis force (from a local ENU reference frame) and was used to check my numerical soution as the code was being developed.

See the demo jupyter notebook for more information on code usage.
