# automatic assist routine

## Part 2, everything was *way* too complicated

Ok, so here's the deal. I'm an idiot and overcomplicated it.
The real trick is to make the simplest line following implementation ever.
It's like what, a generic beginner project?
We can do that.
But what does it involve?

It actually seems to be quite simple, and involves almost no math.
The bulk of the logic is that we should just be able to take the line, see where the average of the leftmost and the rightmost point is to get the "center of it", and then determine how much power to give to each side proportionately using that information.
For example, if the line's center is on the left then provide more power to the right, and vice versa.

It should be relatively foolproof and requite little tuning to make work.
To be completely honest, it could be done without using any pid whatsoever.
Definitely worth looking into in terms of implementing.

## Original planning

- drive forwards until line is detected
- display something onto smartdashboard if line is found
- get line vector
  - slope
  - y intercept in frame (note that the bottom left of the frame if left side of the robot closest)
- find center of line in camera fov
- calculate change in distance and rotation
- go forwards for distance and then turn degrees
- yeet at the wall

## change in distance (inches)

$$y= \frac {7.5(39m+b)} {-51} + 14.5$$

magic numbers are $\frac {7.5} {51}$, the ratio between inches and camera pixels, $39$, the center x of the camera, $14.5$, the distance in inches between the top of the camera ($x=0$) and the center of rotation.
$m$ is the slope of the vector and $b$ is the projected y-intercept with the camera where $y=0$.

## Change in rotation (degrees)

$$\Theta = \arctan(-m)$$

$$r\degree = \left\{
    \begin{array}{ll}
        90\degree-\Theta & \quad \Theta < 90\degree \\
        -90\degree+\Theta & \quad \Theta > 90\degree \\
        0 & \quad \Theta = 90\degree
    \end{array}
\right.
$$