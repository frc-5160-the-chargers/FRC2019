# automatic assist routine

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