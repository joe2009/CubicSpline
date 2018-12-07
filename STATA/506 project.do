
import delimited uswages.csv
ssc install bspline

list in 1/4


//scatter without fit
twoway (scatter wage exper), legend(off) note("Fig 1. Relationship between experience and wage")title("Wage vs Exper") name(Scatter)

//remove outliers
drop if wage > 4000

//scatter without outliers
twoway (scatter wage exper), legend(off) note("Fig 2. Relationship between experience and wage (remove outlier)")title("Wage vs Exper") name(Scatter2)

//Linear fit
bspline, xvar(exper) gen(linear_wage_exper) power(1)
regress wage linear_wage_exper*
predict linear_wage_exper
twoway (scatter wage exper)(line linear_wage_exper exper, sort), legend(off) note("Fig 3. Relationship between experience and wage: using simple linear regression") title("Linear") name(Linear)

//Quadratic fit
bspline, xvar(exper) gen(quad_wage_exper) power(2)
regress wage quad_wage_exper*
predict quad_wage_exper
twoway (scatter wage exper)(line quad_wage_exper exper, sort), legend(off) note("Fig 4. Relationship between experience and wage: using polynomial regression") title("Quadratic") name(Quadratic)


//Cubic Spline
bspline, xvar(exper) knots(0,20,40,58) gen(cubic_wage_exper) power(3)
regress wage cubic_wage_exper*
predict cubic_wage_exper
twoway (scatter wage exper)(line cubic_wage_exper exper, sort), legend(off) note("Fig 5. Relationship between experience and wage: using cubic regression. Knots at (0,20,40,58)") title("Cubic") name(Cubic)

//All fits
twoway (scatter wage exper)(line linear_wage_exper quad_wage_exper cubic_wage_exper exper, sort), legend(label(1 "Observed") label(2 "Linear Regression") label(3 "Polynomial Regression") label(4 "Cubic Regrssion")) note("Fig 6. Relationship between experience and wage") title("Linear vs Quadratic vs Cubic") name(All)
