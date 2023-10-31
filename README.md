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

# Relevant Math
## First Order Approximation
Derived in problem 9.26 in Taylor's Classical Mechanics. These equations of motion were mainly used for "sanity checks" while developing the numerical methods. They can still be used to calculate approximations in the local_projectile class. They are only valid in a local ENU reference frame. 
$$x(t)= v_{x0}t + \Omega (v_{y0}sin(\phi)-v_{z0}cos(\phi))t^2 + \frac{1}{3}\Omega g t^3 cos(\phi)$$
$$y(t) =v_{y0}t - \Omega v_{x0}sin(\phi)t^2 $$
$$z(t) =v_{y0}t + \Omega v_{x0}cos(\phi)t^2 - \frac{1}{2} g t^2 $$
Where $\Omega$ is the rotation rate of the Earth, and $\phi$ is the projectile's latitude.

## Velocity Components
We use the alt/az convention, where the altitude is the angle measured up from the local horizon. The azimuthal angle is measured counterclockwise from North.

$$ \dot x = v_0 sin(az) cos(alt) $$

$$ \dot y = v_0 cos(az) cos(alt) $$

$$ \dot z = v_0 sin(alt) $$

## Newton's Second Law
We set up Newton's second law for the forces we want to account for, then separate the ODE into it's acceleration components depending on the reference frame we are interested in.

$$m \ddot r = F_{grav} + F_{drag} + F_{cor} $$

$$ \ddot r = g - \frac{C}{m} v^2 \hat v + (2 \dot r \times \Omega )$$

### Local Reference Frame
In the case of a local reference frame $\dot r = (\dot x, \dot y, \dot z)$ and $\Omega = (0, \Omega cos(\phi), \Omega sin(\phi))$. Where, once again, $\phi$ is the latitude. This brings our acceleration components to:

$$ \ddot x = -\frac{C}{m} v v_x + 2 \Omega (v_y sin(\phi) - v_z cos(\phi) )$$  

$$ \ddot y = -\frac{C}{m} v v_y - 2 \Omega v_x sin(\phi) $$

$$ \ddot z = -\frac{C}{m} v v_z + 2 \Omega v_x cos(\phi) - g$$

### Geocentric Reference Frame
In a ECEF reference frame, $\Omega = (0,0,\Omega)$. Following through with Newton's second law gives us:

$$ \ddot x = -gcos(\phi)cos(\lambda) -\frac{C}{m}vv_x + 2\Omega v_y $$

$$ \ddot y = -gcos(\phi)sin(\lambda) -\frac{C}{m}vv_y - 2 \Omega v_x $$

$$ \ddot z = -gsin(\phi) -\frac{C}{m}vv_z $$

Where $\lambda$ is the longitude.

## Drag Force and Gravity
We calculate the drag force and gravity depending on the current height of the projectile. The gravity is easily calculated with

$$ g = \sqrt{ \frac{GM_{Earth}}{(R_{Earth} + height)^2}} $$

The drag force is calculated based on the standard drag equation:

$$ F_D = \frac{1}{2} \rho A C_d$$

Where $A$ is the cross sectional area of the object, normal to its velocity. $C_d$ is the drag coefficient of the object, and $\rho$ is the air density. We calculate the current air density based off a negative exponent fitted to the 1976 US Standard Atmosphere.

$$ \rho = 1.225 e^{-height/8500} $$

Where   $1.225$ is the atmospheric density at sea level, and $8500 m$ is the scale height of the atmosphere.

# Coordinate Conversions
### To convert from geodetic $(\phi, \lambda, heigh)$ to ECEF $(X,Y,Z)$

$$ X = (R_{Earth}+h) cos(\phi) cos(\lambda) $$

$$ Y = (R_{Earth}+h cos(\phi) sin(\lambda) $$

$$ Z = (R_{Earth}+h sin(\lambda) $$

### ECEF to Geodetic

$$ \lambda = atan2(Y,X) $$

$$ \phi = tan^{-1} ( \frac{Z}{ \sqrt{X^2 + Y^2} } ) $$

$$ h = \frac{ \sqrt{X^2 + Y^2} }{ cos(\phi) } - R_{Earth} $$

# To Do
### Known Issues
* At the equator, when the azimuthal angle=0, the trajectory makes no sense.
### Features to Add
* Use shooting method for boundary value problems.
* For suborbital trajectories, use elliptical orbit equations to determin launch angle.
