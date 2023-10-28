# global-kinematics

## Overview
A collection of python packages to explore kinematic motion on a global scale. Includes multiple trajectory calculation methods, variable atmospheric density, quadratic drag, variable planet rotation rate, height dependent gravity, and coordinate conversion methods to switch reference frames.

There are two classes that ship with this code, local_projectile and global_projectile. Both assume a perfectly spherical Earth, with a radius of $3753$ km. The first calculates the projectile motion from a local reference frame. The local reference frame uses the ENU convention where $E=x$, $N=y$, and $U=z$. The semi-flat Earth model does account for drop due to curvature, but does not account for changing latitude (crucial for accurate coriolis calculation), or changing angle of our gravity vector. The results will be skewed if our projectile travels a significant amount of Earth's surface. However, it is a reasonable, first order, approximation within a few hundred kilometers.

The global_projectile class calculates motion from the ECEF, geocentric reference frame. This class accounts for changing latitude, and gravity vector. As such, it is the most accurate method for calculating long range, sub orbital trajectories. This class also provides a method to convert our geocentric solution to GCS coordinates, and motion viewed from a local reference frame, with the origin at the launch site.

Depending on the size of your trajectory, and desired answer accuracy, different models of projectile motion are appropriate. Each of these models are useful in their domain, but breakdown at a certain point. The goal of this project is to model different equations of motion on a global scale and tease out when each model reaches its limit.
