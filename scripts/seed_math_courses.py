import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app.database import get_db

def seed_courses():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Seed Course
        cursor.execute('''
            INSERT OR REPLACE INTO courses (id, title, section, description)
            VALUES (?, ?, ?, ?)
        ''', ('course-math-mastery', 'Digital SAT Math Mastery', 'Math', 'Master every domain and skill tested on the Digital SAT Math section with the Desmos calculator.'))
        
        modules = [
            {
                "topic": "Algebra",
                "subtopic": "Linear Equations",
                "title": "Mastering Linear Equations",
                "content": r"""# Linear Equations: Mastery Guide

## Overview
Linear equations form the backbone of the Digital SAT Math section. They test your ability to model real-world scenarios, solve for variables, and understand the relationship between variables at a constant rate of change. Mastering linear equations is crucial because they appear frequently and serve as a foundation for more complex topics like systems of equations and functions.

## Core Concepts
- **Slope-Intercept Form:** $y = mx + b$, where $m$ is the slope and $b$ is the y-intercept.
- **Point-Slope Form:** $y - y_1 = m(x - x_1)$, where $(x_1, y_1)$ is a point on the line and $m$ is the slope.
- **Standard Form:** $Ax + By = C$, where $A, B$, and $C$ are constants.
- **Slope Formula:** $m = \frac{y_2 - y_1}{x_2 - x_1}$.
- **Parallel vs. Perpendicular:** Parallel lines have the same slope ($m_1 = m_2$). Perpendicular lines have negative reciprocal slopes ($m_1 \cdot m_2 = -1$).

## Desmos Tips
- **Solving Equations:** To solve a complex linear equation, type the left side into Desmos as $y = \text{left side}$ and the right side as $y = \text{right side}$. Click the intersection point to find the x-value of the solution.
- **Finding Intercepts:** Enter the equation in any form and click on the axes to instantly find the x and y-intercepts.
- **Sliders:** If an equation involves an unknown constant (like $y = 3x + c$), add a slider for $c$ to visualize how changing the constant affects the line's position.

## Worked Examples

**Example 1:**
If $3(x - 4) + 2x = 5x + 7 - x$, what is the value of $x$?
*Algebraic Solution:*
Distribute and combine like terms:
$3x - 12 + 2x = 4x + 7$
$5x - 12 = 4x + 7$
Subtract $4x$ from both sides: $x - 12 = 7$
Add $12$: $x = 19$.
*Desmos Shortcut:* Graph $y = 3(x - 4) + 2x$ and $y = 5x + 7 - x$. Find the intersection point. The x-coordinate is 19.

**Example 2:**
A line passes through $(2, 5)$ and $(-4, -7)$. What is its equation in $y = mx + b$ form?
*Algebraic Solution:*
Find slope: $m = \frac{-7 - 5}{-4 - 2} = \frac{-12}{-6} = 2$.
Use point-slope form: $y - 5 = 2(x - 2) \implies y = 2x - 4 + 5 \implies y = 2x + 1$.
*Desmos Shortcut:* Add a table in Desmos with the points $(2,5)$ and $(-4,-7)$. Type $y_1 \sim mx_1 + b$ below it to instantly get $m=2$ and $b=1$.

**Example 3:**
For what value of $k$ does the system $y = 3x + 5$ and $y = kx - 2$ have no solution?
*Algebraic Solution:*
Lines with no solution must be parallel (same slope) and have different y-intercepts. The slope of the first line is $3$. So, $k$ must equal $3$.
*Desmos Shortcut:* Graph $y = 3x + 5$ and $y = kx - 2$ (add slider for $k$). Slide $k$ until the lines never intersect (are perfectly parallel), which happens at $k = 3$.

## Common Traps
- **Sign Errors when Distributing:** Forgetting to distribute a negative sign to the second term inside a parenthesis (e.g., $-(x - 3)$ becoming $-x - 3$ instead of $-x + 3$). Always double-check your signs.
- **Switching x and y in the Slope Formula:** Calculating slope as change in x over change in y. Remember "rise over run": $\frac{\Delta y}{\Delta x}$.
- **Misinterpreting the y-intercept in Word Problems:** The y-intercept represents the initial value (when $x=0$), not the final total or the rate of change.

## Quick Drills

1. What is the value of $x$ in the equation $4(x - 2) = 2x + 8$?
2. What is the slope of the line $3x - 4y = 12$?
3. If a line is parallel to $y = -2x + 4$ and passes through $(0, 5)$, what is its equation?
4. A gym charges a $\$50$ sign-up fee plus $\$25$ per month. What linear equation models the total cost $C$ for $m$ months?
5. Solve for $t$: $\frac{t+3}{2} = \frac{2t-1}{3}$

**Answers:**
1. $x = 8$
2. Slope = $\frac{3}{4}$ (Rewrite as $y = \frac{3}{4}x - 3$)
3. $y = -2x + 5$
4. $C = 25m + 50$
5. $t = 11$
"""
            },
            {
                "topic": "Advanced Math",
                "subtopic": "Equivalent Expressions",
                "title": "Simplifying Equivalent Expressions",
                "content": r"""# Equivalent Expressions

## Overview
Questions on equivalent expressions test your algebraic manipulation skills, specifically polynomial arithmetic, factoring, and rational expressions. The SAT frequently asks you to find an expression that is mathematically identical to a given, usually complicated, algebraic expression.

## Core Concepts
- **Combining Like Terms:** Only terms with the exact same variables and exponents can be added or subtracted.
- **Distributive Property:** $a(b + c) = ab + ac$.
- **FOIL (First, Outer, Inner, Last):** $(a+b)(c+d) = ac + ad + bc + bd$.
- **Difference of Squares:** $a^2 - b^2 = (a-b)(a+b)$.
- **Perfect Square Trinomials:** $(a \pm b)^2 = a^2 \pm 2ab + b^2$.
- **Polynomial Division/Rewriting Rational Expressions:** $\frac{A(x)}{B(x)} = Q(x) + \frac{R(x)}{B(x)}$.

## Desmos Tips
- **The "Test a Number" Visual Strategy:** Graph the original expression as $y = \text{original expression}$. Graph the answer choices one by one. The correct choice will perfectly overlap the original graph.
- **Checking Equivalence:** If an expression has multiple variables (like $x$ and $y$), set $y$ to a specific constant (e.g., $y=2$) and graph the expressions as functions of $x$ to check for overlaps.

## Worked Examples

**Example 1:**
Which expression is equivalent to $(3x^2 - 4x + 1) - (x^2 + 2x - 5)$?
*Algebraic Solution:*
Distribute the negative sign: $3x^2 - 4x + 1 - x^2 - 2x + 5$.
Combine like terms: $(3x^2 - x^2) + (-4x - 2x) + (1 + 5) = 2x^2 - 6x + 6$.
*Desmos Shortcut:* Graph $y = (3x^2 - 4x + 1) - (x^2 + 2x - 5)$ and $y = 2x^2 - 6x + 6$. They will be the exact same parabola.

**Example 2:**
Rewrite the expression $\frac{x^2 + 5x + 6}{x + 2}$.
*Algebraic Solution:*
Factor the numerator: $x^2 + 5x + 6 = (x + 2)(x + 3)$.
Cancel out the common factor: $\frac{(x + 2)(x + 3)}{x + 2} = x + 3$ (for $x \neq -2$).
*Desmos Shortcut:* Graph $y = \frac{x^2 + 5x + 6}{x + 2}$. Notice it forms a straight line identical to $y = x + 3$ (except for a hole at $x = -2$).

**Example 3:**
Which expression is equivalent to $(2x - 3y)^2$?
*Algebraic Solution:*
Use the perfect square formula $(a-b)^2 = a^2 - 2ab + b^2$.
$(2x)^2 - 2(2x)(3y) + (3y)^2 = 4x^2 - 12xy + 9y^2$.
*Desmos Shortcut:* Since there are two variables, substitute a value for $y$, say $y=1$. Graph $y = (2x - 3(1))^2$ and $y = 4x^2 - 12x(1) + 9(1)^2$. They will perfectly overlap.

## Common Traps
- **Fake Distribution of Powers:** Thinking $(x + y)^2 = x^2 + y^2$. Remember the middle term! It must be $x^2 + 2xy + y^2$.
- **Negative Sign Drop:** When subtracting polynomials, forgetting to distribute the subtraction to every term in the second polynomial.
- **Canceling Terms Unlawfully in Fractions:** Simplifying $\frac{x^2 + 4}{x}$ to $x + 4$. You cannot cancel parts of an addition/subtraction. It is $\frac{x^2}{x} + \frac{4}{x} = x + \frac{4}{x}$.

## Quick Drills

1. Simplify: $3(x^2 - 2x) - 2(x^2 + 4x - 1)$.
2. Factor: $16x^2 - 25$.
3. Which expression is equivalent to $(x+4)(x-5)$?
4. Simplify: $\frac{4x^3 - 8x^2}{4x^2}$.
5. Which expression is equivalent to $x^2 + 10x + 25$?

**Answers:**
1. $x^2 - 14x + 2$
2. $(4x - 5)(4x + 5)$
3. $x^2 - x - 20$
4. $x - 2$
5. $(x + 5)^2$
"""
            },
            {
                "topic": "Advanced Math",
                "subtopic": "Exponents",
                "title": "Mastering Exponents and Radicals",
                "content": r"""# Exponents and Radicals

## Overview
Questions involving exponents and radicals test your understanding of exponent laws, fractional exponents, and exponential growth/decay models. These rules govern how powers combine and interact, essential for simplifying complex algebraic expressions and solving exponential equations.

## Core Concepts
- **Product Rule:** $x^a \cdot x^b = x^{a+b}$
- **Quotient Rule:** $\frac{x^a}{x^b} = x^{a-b}$
- **Power of a Power:** $(x^a)^b = x^{a \cdot b}$
- **Negative Exponents:** $x^{-a} = \frac{1}{x^a}$
- **Zero Exponent:** $x^0 = 1$ (for $x \neq 0$)
- **Fractional Exponents (Radicals):** $x^{\frac{m}{n}} = \sqrt[n]{x^m} = (\sqrt[n]{x})^m$

## Desmos Tips
- **Evaluating Complex Radicals/Powers:** If a question asks for the numeric equivalent of a complex expression like $8^{\frac{2}{3}}$, simply type it into Desmos to get $4$.
- **Finding Equivalent Expressions:** Graph the original expression and the answer choices to see which graph matches exactly. Be careful to restrict the domain to $x > 0$ when dealing with fractional exponents to avoid confusing errors with negative roots.
- **Solving Exponential Equations:** Graph both sides (e.g., $y = 2^{x+1}$ and $y = 16$) and find the intersection point.

## Worked Examples

**Example 1:**
If $3^{2x-1} = 27$, what is the value of $x$?
*Algebraic Solution:*
Rewrite 27 with a base of 3: $27 = 3^3$.
Set the exponents equal: $2x - 1 = 3$.
$2x = 4 \implies x = 2$.
*Desmos Shortcut:* Graph $y = 3^{2x-1}$ and $y = 27$. Click the intersection point to see the x-coordinate is 2.

**Example 2:**
Which expression is equivalent to $\sqrt[3]{x^6 y^9}$?
*Algebraic Solution:*
Rewrite using fractional exponents: $(x^6 y^9)^{\frac{1}{3}}$.
Multiply exponents: $x^{6 \cdot \frac{1}{3}} y^{9 \cdot \frac{1}{3}} = x^2 y^3$.
*Desmos Shortcut:* Substitute a value for $y$ (e.g., $y=2$). Graph $y = \sqrt[3]{x^6 (2)^9}$ and $y = x^2 (2)^3$. They match exactly.

**Example 3:**
Simplify $\frac{x^3 \cdot x^5}{(x^2)^4}$.
*Algebraic Solution:*
Apply product rule on top: $x^{3+5} = x^8$.
Apply power rule on bottom: $x^{2 \cdot 4} = x^8$.
Divide: $\frac{x^8}{x^8} = x^{8-8} = x^0 = 1$.
*Desmos Shortcut:* Graph $y = \frac{x^3 \cdot x^5}{(x^2)^4}$. The result is a horizontal line at $y=1$.

## Common Traps
- **Adding Bases:** Thinking $2^3 + 2^4 = 2^7$. You can only add exponents when *multiplying* terms with the same base ($2^3 \cdot 2^4 = 2^7$).
- **Mishandling Negative Exponents:** Treating $x^{-2}$ as $-x^2$. Remember, negative exponents mean taking the reciprocal, $\frac{1}{x^2}$.
- **Power of a Power vs Product:** Confusing $(x^2)^3$, which is $x^6$, with $x^2 \cdot x^3$, which is $x^5$.

## Quick Drills

1. Simplify $x^4 \cdot x^7$.
2. What is the value of $16^{\frac{3}{4}}$?
3. Simplify $\frac{y^9}{y^3}$.
4. Express $\sqrt{x^5}$ using a fractional exponent.
5. Solve for $x$: $5^{x+2} = 125$.

**Answers:**
1. $x^{11}$
2. $8$
3. $y^6$
4. $x^{\frac{5}{2}}$
5. $x = 1$
"""
            },
            {
                "topic": "Advanced Math",
                "subtopic": "Quadratic Equations",
                "title": "Cracking Quadratic Equations",
                "content": r"""# Quadratic Equations

## Overview
Quadratics appear everywhere in the Advanced Math section. You must be comfortable switching between different forms of quadratic equations, finding the roots (x-intercepts), finding the vertex (minimum/maximum), and using the discriminant to determine the number of solutions.

## Core Concepts
- **Standard Form:** $y = ax^2 + bx + c$. The y-intercept is $c$.
- **Factored Form:** $y = a(x - r_1)(x - r_2)$. The roots (x-intercepts) are $r_1$ and $r_2$.
- **Vertex Form:** $y = a(x - h)^2 + k$. The vertex is $(h, k)$.
- **Quadratic Formula:** $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.
- **Discriminant:** $\Delta = b^2 - 4ac$.
  - If $\Delta > 0$: Two real solutions.
  - If $\Delta = 0$: One real solution.
  - If $\Delta < 0$: No real solutions.
- **Sum and Product of Roots:** For $ax^2 + bx + c = 0$, Sum = $\frac{-b}{a}$ and Product = $\frac{c}{a}$.

## Desmos Tips
- **Finding Roots and Vertex:** Just type the quadratic equation (e.g., $y = x^2 - 5x + 6$). Click on the parabola to immediately reveal the x-intercepts (roots), the y-intercept, and the vertex (minimum or maximum point).
- **Matching Forms:** If asked which equation represents the same parabola, graph the original and the answer choices to see which one overlaps perfectly.
- **Solving Systems:** When solving a system with a quadratic and a linear equation, graph both and tap the intersections.

## Worked Examples

**Example 1:**
What are the solutions to $x^2 - 7x + 10 = 0$?
*Algebraic Solution:*
Factor the quadratic: $(x - 2)(x - 5) = 0$.
Set each factor to zero: $x - 2 = 0 \implies x = 2$; $x - 5 = 0 \implies x = 5$.
*Desmos Shortcut:* Graph $y = x^2 - 7x + 10$. Look at where the graph crosses the x-axis. The points are $(2, 0)$ and $(5, 0)$.

**Example 2:**
What is the minimum value of the function $f(x) = 2x^2 - 8x + 3$?
*Algebraic Solution:*
Find the x-coordinate of the vertex: $x = \frac{-b}{2a} = \frac{-(-8)}{2(2)} = \frac{8}{4} = 2$.
Substitute $x = 2$ back into the function: $f(2) = 2(2)^2 - 8(2) + 3 = 8 - 16 + 3 = -5$. The minimum value is $-5$.
*Desmos Shortcut:* Graph the function. Click on the lowest point of the parabola. The coordinates are $(2, -5)$. The minimum value is the y-coordinate, $-5$.

**Example 3:**
For what values of $k$ does the equation $x^2 + kx + 9 = 0$ have exactly one real solution?
*Algebraic Solution:*
For exactly one solution, the discriminant must be zero: $b^2 - 4ac = 0$.
$k^2 - 4(1)(9) = 0 \implies k^2 - 36 = 0 \implies k^2 = 36 \implies k = 6 \text{ or } -6$.
*Desmos Shortcut:* Graph $y = x^2 + kx + 9$ and add a slider for $k$. Slide $k$ until the parabola just touches the x-axis at exactly one point. You will see this happens when $k=6$ and $k=-6$.

## Common Traps
- **Confusing Roots and Factors:** If roots are $2$ and $-3$, the factors are $(x - 2)$ and $(x + 3)$, not $(x + 2)$ and $(x - 3)$. Always reverse the sign.
- **Missing the $\pm$ in Square Roots:** When solving $x^2 = 16$, the answer is $x = \pm 4$, not just $4$.
- **Misinterpreting Vertex questions:** When a question asks for the maximum height, it wants the y-value of the vertex. When it asks *when* the maximum height occurs, it wants the x-value.

## Quick Drills

1. Find the roots of $x^2 + 6x + 8 = 0$.
2. What is the vertex of the parabola $y = (x - 3)^2 + 4$?
3. Does $2x^2 - 3x + 5 = 0$ have real solutions? (Use discriminant)
4. What is the sum of the solutions to $3x^2 - 12x + 7 = 0$?
5. Rewrite $y = x^2 - 4x + 3$ in factored form.

**Answers:**
1. $x = -2, x = -4$
2. $(3, 4)$
3. No ($b^2 - 4ac = 9 - 40 = -31 < 0$)
4. Sum = $\frac{-b}{a} = \frac{-(-12)}{3} = 4$
5. $y = (x - 1)(x - 3)$
"""
            },
            {
                "topic": "Geometry and Trigonometry",
                "subtopic": "Lines, Angles, and Triangles",
                "title": "Geometry Foundations: Lines, Angles & Triangles",
                "content": r"""# Lines, Angles, and Triangles

## Overview
Geometry on the DSAT heavily emphasizes relationships between lines, angles, and the fundamental properties of triangles. Knowing angle theorems and triangle congruence/similarity shortcuts is crucial for these visually driven problems.

## Core Concepts
- **Supplementary Angles:** Angles that add up to $180^\circ$ (a straight line).
- **Complementary Angles:** Angles that add up to $90^\circ$.
- **Vertical Angles:** Opposite angles at an intersection are equal.
- **Parallel Lines cut by a Transversal:** Corresponding, Alternate Interior, and Alternate Exterior angles are equal. Consecutive interior angles are supplementary.
- **Triangle Sum Theorem:** The interior angles of any triangle add up to $180^\circ$.
- **Exterior Angle Theorem:** An exterior angle of a triangle equals the sum of the two opposite interior angles.
- **Similar Triangles:** Triangles with the exact same angles. Their corresponding side lengths are proportional.
- **Pythagorean Theorem:** $a^2 + b^2 = c^2$ (for right triangles only).
- **Special Right Triangles:**
  - $45^\circ-45^\circ-90^\circ$: sides are $x, x, x\sqrt{2}$.
  - $30^\circ-60^\circ-90^\circ$: sides are $x, x\sqrt{3}, 2x$.

## Desmos Tips
- **Solving Proportions:** For similar triangles, set up the proportion $\frac{a}{b} = \frac{c}{x}$ as an equation in Desmos and it will instantly give you the missing length.
- **Pythagorean Calculations:** Type $\sqrt{c^2 - a^2}$ directly into the calculator to quickly find the missing leg of a right triangle.

## Worked Examples

**Example 1:**
In a triangle, two angles measure $40^\circ$ and $75^\circ$. What is the measure of the third angle?
*Algebraic Solution:*
The sum is $180^\circ$. Third angle = $180 - (40 + 75) = 180 - 115 = 65^\circ$.
*Desmos Shortcut:* Type $180 - (40 + 75)$ directly into an expression line.

**Example 2:**
Two parallel lines are intersected by a transversal. If one interior angle is $(2x + 10)^\circ$ and the consecutive interior angle is $(3x - 30)^\circ$, find $x$.
*Algebraic Solution:*
Consecutive interior angles add up to $180^\circ$.
$(2x + 10) + (3x - 30) = 180$
$5x - 20 = 180$
$5x = 200 \implies x = 40$.
*Desmos Shortcut:* Type $(2x + 10) + (3x - 30) = 180$ into Desmos. Look at the vertical line graph at $x = 40$.

**Example 3:**
A right triangle has a hypotenuse of $13$ and a leg of $5$. What is the length of the other leg?
*Algebraic Solution:*
Use the Pythagorean Theorem: $a^2 + b^2 = c^2$.
$5^2 + b^2 = 13^2 \implies 25 + b^2 = 169 \implies b^2 = 144 \implies b = 12$.
*Desmos Shortcut:* Type $\sqrt{13^2 - 5^2}$ to immediately get $12$.

## Common Traps
- **Assuming Diagrams are to Scale:** Unless stated otherwise, never guess an angle measure or side length just by looking at how big it appears in the drawing.
- **Mixing up Special Right Triangle Ratios:** In a 30-60-90 triangle, the hypotenuse is twice the short leg ($2x$), NOT the long leg. The long leg is $x\sqrt{3}$.
- **Confusing Congruent and Proportional:** Similar triangles have proportional sides, not necessarily equal sides. Don't assume lengths are equal just because angles are.

## Quick Drills

1. Angles $A$ and $B$ are supplementary. If $A = 110^\circ$, what is $B$?
2. In a right triangle, the legs are $6$ and $8$. What is the hypotenuse?
3. An isosceles right triangle has a leg of $7$. What is the hypotenuse?
4. Two angles of a triangle are $50^\circ$ and $60^\circ$. What is the exterior angle adjacent to the third angle?
5. Triangles ABC and DEF are similar. If AB=4, BC=6, and DE=12, what is EF?

**Answers:**
1. $70^\circ$
2. $10$
3. $7\sqrt{2}$
4. $110^\circ$ (Because $50+60 = 110$, or $180 - (180 - 110)$)
5. $18$ (Scale factor is $3$)
"""
            },
            {
                "topic": "Geometry and Trigonometry",
                "subtopic": "Circles",
                "title": "Conquering Circles",
                "content": r"""# Circles

## Overview
Circle questions on the SAT evaluate your knowledge of the equation of a circle in the coordinate plane, as well as geometric properties involving area, circumference, arcs, and sectors.

## Core Concepts
- **Equation of a Circle:** $(x - h)^2 + (y - k)^2 = r^2$, where $(h, k)$ is the center and $r$ is the radius.
- **Completing the Square:** Often required to convert a general polynomial circle equation into standard form to find the center and radius.
- **Area of a Circle:** $A = \pi r^2$.
- **Circumference of a Circle:** $C = 2\pi r$ or $C = \pi d$.
- **Arc Length:** $s = \frac{\theta}{360} \cdot 2\pi r$ (where $\theta$ is in degrees).
- **Sector Area:** $\text{Area} = \frac{\theta}{360} \cdot \pi r^2$.
- **Radians vs. Degrees:** To convert degrees to radians, multiply by $\frac{\pi}{180}$. To convert radians to degrees, multiply by $\frac{180}{\pi}$. The full circle is $2\pi$ radians.

## Desmos Tips
- **Visualizing the Equation:** Graph an equation like $x^2 + y^2 - 4x + 6y = 12$ directly in Desmos. It will draw the circle. You can easily spot the center visually by clicking on the leftmost, rightmost, top, and bottom extremities to find the midpoint.
- **Finding the Radius:** Once the circle is graphed, subtract the x-coordinate of the center from the rightmost edge's x-coordinate to get the radius instantly.

## Worked Examples

**Example 1:**
What is the center and radius of the circle given by $(x + 3)^2 + (y - 5)^2 = 49$?
*Algebraic Solution:*
Compare to $(x - h)^2 + (y - k)^2 = r^2$.
Center $(h, k) = (-3, 5)$.
Radius $r = \sqrt{49} = 7$.
*Desmos Shortcut:* Graph the equation. Click the center visually, which is at $(-3, 5)$.

**Example 2:**
Find the center of the circle $x^2 + y^2 - 8x + 10y - 8 = 0$.
*Algebraic Solution:*
Complete the square for $x$ and $y$:
$(x^2 - 8x + 16) + (y^2 + 10y + 25) = 8 + 16 + 25$
$(x - 4)^2 + (y + 5)^2 = 49$.
Center is $(4, -5)$.
*Desmos Shortcut:* Type $x^2 + y^2 - 8x + 10y - 8 = 0$. Look at the circle. The center is exactly at $(4, -5)$.

**Example 3:**
A circle has a radius of $6$. What is the area of a sector with a central angle of $60^\circ$?
*Algebraic Solution:*
Area $= \frac{60}{360} \cdot \pi(6^2) = \frac{1}{6} \cdot 36\pi = 6\pi$.
*Desmos Shortcut:* Evaluate $\frac{60}{360} \cdot \pi \cdot 6^2$ to get approximately $18.849$, which matches $6\pi$.

## Common Traps
- **Forgetting to Square Root the Radius:** In the equation $(x-2)^2 + (y-3)^2 = 16$, the radius is $4$, not $16$.
- **Getting Center Signs Backwards:** The equation $(x-4)^2 + (y+2)^2$ has a center at $(+4, -2)$, not $(-4, +2)$.
- **Arc Measure vs Arc Length:** Arc measure is the degree of the angle. Arc length is a linear distance. Make sure to use the circumference formula for arc length.

## Quick Drills

1. What is the radius of the circle $(x - 1)^2 + (y + 4)^2 = 100$?
2. Find the area of a circle with a diameter of $10$.
3. What is the arc length of a semicircle with a radius of $4$?
4. Convert $\frac{\pi}{3}$ radians to degrees.
5. What is the center of the circle $x^2 - 2x + y^2 = 8$?

**Answers:**
1. $10$
2. $25\pi$
3. $4\pi$ (Half of $2\pi r$)
4. $60^\circ$
5. $(1, 0)$ (Complete the square for $x$: $(x-1)^2 - 1 + y^2 = 8 \implies (x-1)^2 + y^2 = 9$)
"""
            },
            {
                "topic": "Problem Solving and Data Analysis",
                "subtopic": "Ratios and Rates",
                "title": "Mastering Ratios, Rates, and Proportions",
                "content": r"""# Ratios and Rates

## Overview
Rates and ratios are foundational for problem solving. The SAT tests your ability to set up proportions, convert units using dimensional analysis, and analyze real-world scenarios involving speed, density, and scaling.

## Core Concepts
- **Ratio:** A comparison of two quantities (e.g., $3:4$ or $\frac{3}{4}$).
- **Proportion:** An equation stating that two ratios are equal ($\frac{a}{b} = \frac{c}{d}$). Solve by cross-multiplying: $ad = bc$.
- **Unit Rate:** A rate with a denominator of 1 (e.g., 50 miles per hour).
- **Distance Formula:** $d = r \cdot t$ (Distance = Rate $\times$ Time).
- **Unit Conversion (Dimensional Analysis):** Multiply by conversion factors as fractions so unwanted units cancel out.

## Desmos Tips
- **Solving Proportions Fast:** Type the proportion as an equation with $x$, like $\frac{3}{7} = \frac{x}{105}$. The vertical line tells you the exact answer.
- **Chained Conversions:** Type the entire string of fractions into a single Desmos expression to avoid rounding errors during intermediate steps. (e.g., $50 \cdot \frac{5280}{1} \cdot \frac{1}{60}$).

## Worked Examples

**Example 1:**
A recipe calls for $3$ cups of flour to make $8$ servings. How many cups of flour are needed for $20$ servings?
*Algebraic Solution:*
Set up a proportion: $\frac{3}{8} = \frac{x}{20}$.
Cross-multiply: $8x = 60 \implies x = \frac{60}{8} = 7.5$.
*Desmos Shortcut:* Graph $y = \frac{3}{8}x$ (where $x$ is servings and $y$ is flour) or just solve the proportion equation as given above.

**Example 2:**
A car travels at $60$ miles per hour. How many feet does it travel per second? (1 mile = 5280 feet, 1 hour = 3600 seconds).
*Algebraic Solution:*
$\frac{60 \text{ miles}}{1 \text{ hour}} \cdot \frac{5280 \text{ feet}}{1 \text{ mile}} \cdot \frac{1 \text{ hour}}{3600 \text{ seconds}}$
$= \frac{60 \cdot 5280}{3600} = \frac{316800}{3600} = 88 \text{ feet/sec}$.
*Desmos Shortcut:* Just type $\frac{60 \cdot 5280}{3600}$ into the calculator.

**Example 3:**
If the ratio of boys to girls in a class is $4:5$ and there are $36$ students in total, how many girls are there?
*Algebraic Solution:*
Total parts = $4 + 5 = 9$.
Each "part" is $36 / 9 = 4$ students.
Number of girls = $5 \cdot 4 = 20$.
*Desmos Shortcut:* Set up the equation $4x + 5x = 36$. Find $x = 4$, then calculate $5(4) = 20$.

## Common Traps
- **Part-to-Part vs Part-to-Whole:** If the ratio of boys to girls is $4:5$, the ratio of girls to the TOTAL class is $5:9$. Read carefully!
- **Inverted Proportions:** Setting up $\frac{\text{miles}}{\text{hours}} = \frac{\text{hours}}{\text{miles}}$. Always keep units strictly aligned on both sides of the equal sign.
- **Forgetting to Square Conversions for Area:** If 1 yard = 3 feet, then 1 square yard = 9 square feet ($3^2$), not 3.

## Quick Drills

1. Solve for $x$: $\frac{5}{12} = \frac{x}{60}$.
2. If $5$ apples cost $\$2.00$, what do $8$ apples cost?
3. A train travels $150$ miles in $2.5$ hours. What is its speed in miles per hour?
4. The ratio of cats to dogs is $2:7$. If there are $45$ total animals, how many dogs are there?
5. Convert $3$ square meters to square centimeters (1 m = 100 cm).

**Answers:**
1. $x = 25$
2. $\$3.20$
3. $60$ mph
4. $35$ dogs
5. $30,000$ cm$^2$
"""
            },
            {
                "topic": "Problem Solving and Data Analysis",
                "subtopic": "Percentages",
                "title": "Nailing Percentages",
                "content": r"""# Percentages

## Overview
Percentage problems on the DSAT require fluency in translating percentage growth and decay into algebraic expressions. You will encounter percent change, percent of a number, and repeated percentage changes (exponential growth/decay).

## Core Concepts
- **Percent as Decimal:** $x\% = \frac{x}{100}$. (e.g., $45\% = 0.45$).
- **Percent of a Number:** "What is $20\%$ of $50$?" $\implies 0.20 \cdot 50 = 10$.
- **Percent Increase/Multiplier:** An increase of $r\%$ means multiplying by $(1 + \frac{r}{100})$. (e.g., a $15\%$ increase is a multiplier of $1.15$).
- **Percent Decrease/Multiplier:** A decrease of $r\%$ means multiplying by $(1 - \frac{r}{100})$. (e.g., a $20\%$ discount is a multiplier of $0.80$).
- **Percent Change Formula:** $\frac{\text{New} - \text{Old}}{\text{Old}} \times 100 = \% \text{ Change}$.

## Desmos Tips
- **Quick Evaluation:** Desmos handles basic percentage math wonderfully. If you need to find price after a $35\%$ discount on a $\$40$ item, type $40 \cdot 0.65$.
- **Finding the Original Price:** If an item is $\$60$ after a $20\%$ discount, type $0.80x = 60$. The vertical line shows $x = 75$.

## Worked Examples

**Example 1:**
A shirt was originally $\$50$. It is on sale for $30\%$ off. What is the sale price?
*Algebraic Solution:*
Multiplier for $30\%$ off is $1 - 0.30 = 0.70$.
Sale price = $50 \cdot 0.70 = 35$.
*Desmos Shortcut:* Type $50 \cdot 0.70$ directly.

**Example 2:**
The population of a town increased from $4,000$ to $5,000$. What was the percent increase?
*Algebraic Solution:*
Use the percent change formula: $\frac{5000 - 4000}{4000} \times 100 = \frac{1000}{4000} \times 100 = 0.25 \times 100 = 25\%$.
*Desmos Shortcut:* Type $\frac{5000-4000}{4000} \cdot 100$.

**Example 3:**
After a $15\%$ tax is added, a laptop costs $\$920$. What was the price before tax?
*Algebraic Solution:*
Let $x$ be the original price. The multiplier for a $15\%$ increase is $1.15$.
$1.15x = 920 \implies x = \frac{920}{1.15} = 800$.
*Desmos Shortcut:* Type $1.15x = 920$. Check the x-intercept of the resulting vertical line to see $x = 800$.

## Common Traps
- **Adding Percents Sequentially:** If a price goes up $10\%$ and then down $10\%$, it is NOT back to the original price. Example: $\$100 \times 1.10 = 110$. Then $110 \times 0.90 = 99$.
- **Subtracting the Percent from the Value:** For $20\%$ off $\$50$, writing $50 - 20 = 30$. You must subtract $20\%$ OF $50$: $50 - (0.20 \times 50)$.
- **Using the New Value as the Base:** For percent change, always divide by the ORIGINAL (old) value, never the new value.

## Quick Drills

1. What is $45\%$ of $80$?
2. A $\$120$ jacket is discounted by $25\%$. What is the final price?
3. If $30\%$ of a number is $18$, what is the number?
4. A stock dropped from $\$80$ to $\$60$. What is the percent decrease?
5. An account with $\$500$ grows by $5\%$ per year. How much is in the account after 1 year?

**Answers:**
1. $36$
2. $\$90$
3. $60$ ($0.30x = 18$)
4. $25\%$
5. $\$525$ ($500 \cdot 1.05$)
"""
            }
        ]

        # Insert Modules
        for i, mod in enumerate(modules):
            cursor.execute('''
                INSERT OR REPLACE INTO course_modules (id, course_id, title, topic, subtopic, lecture_content, order_index)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (str(uuid.uuid4()), 'course-math-mastery', mod['title'], mod['topic'], mod['subtopic'], mod['content'], i))
            
        conn.commit()
        print(f"Seeded 1 course ('Digital SAT Math Mastery') and {len(modules)} modules successfully.")

if __name__ == '__main__':
    seed_courses()
