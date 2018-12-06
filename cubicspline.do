//import uswages dataset
import delimited uswages.csv

//install bspline backage
ssc install bspline

//list first 4 rows of the dataset
list in 1/4


//begin by visualizing the data in the form of a scatterplot
twoway (scatter wage exper), ytitle(Wage) xtitle(Experience) legend(off) note("Fig 1. Relationship between experience and wage")title("Wage vs Exper") name(Scatter)

//remove outliers where wage is greater than 4000
drop if wage > 4000

//scatter without outliers
twoway (scatter wage exper), ytitle(Wage) xtitle(Experience) legend(off) note("Fig 2. Relationship between experience and wage (remove outlier)")title("Wage vs Exper") name(Scatter2)

//Linear regression of experience regressed onto wage
regress wage exper
predict linear_wage_exper
twoway (scatter wage exper)(line linear_wage_exper exper, sort), ytitle(Wage) xtitle(Experience) legend(off) note("Fig 3. Relationship between experience and wage: using simple linear regression") title("Linear") name(Linear)

//Polynomial regression of experience regressed onto wage (Quadratic fit, degree = 2)
regress wage c.exper##c.exper
predict quad_wage_exper
twoway (scatter wage exper)(line quad_wage_exper exper, sort), ytitle(Wage) xtitle(Experience) legend(off) note("Fig 4. Relationship between experience and wage: using polynomial regression") title("Polynomial: Degree 2") name(Degree2)

//Polynomial regression of experience regressed onto wage (Polynomial, degree = 4)
regress wage c.exper##c.exper##c.exper##c.exper
predict degfour_wage_exper
twoway (scatter wage exper)(line degfour_wage_exper exper, sort), ytitle(Wage) xtitle(Experience) legend(off) note("Fig 5. Relationship between experience and wage: using polynomial regression") title("Polynomial: Degree 4") name(Degree4)

//Cubic Spline regression using bspline package with knots at 8,15,27 (these are the quartiles)
bspline, xvar(exper) knots(8,15,27) gen(cubic_wage_exper_spline) power(3)
regress wage cubic_wage_exper_spline*
predict cubic_wage_exper_spline
twoway (scatter wage exper)(line cubic_wage_exper_spline exper, sort), ytitle(Wage) xtitle(Experience) legend(off) note("Fig 6. Relationship between experience and wage: using cubic regression. Knots at (8,15,27)") title("Cubic: Knots at Quartiles") name(Cubic)

//Try to reproduce cubic spline regression results from scratch using basis functions
gen exper2 = exper^2
gen exper3 = exper^3
gen k8 = cond(exper > 8, (exper - 8)^3, 0)
gen k15 = cond(exper > 15, (exper - 15)^3, 0)
gen k27 = cond(exper > 27, (exper - 27)^3, 0)
regress wage exper exper2 exper3 k8 k15 k27
predict cubic_wage_exper

//compare regression results using bspline package with those obtained from scrach
sum cubic_wage_exper cubic_wage_exper_spline

//Cubic Spline regression using bspline with knots now evenly spaced at 15,30,40 
bspline, xvar(exper) knots(15,30,40) gen(cubic_wage_exper_spline_even) power(3)
regress wage cubic_wage_exper_spline_even*
predict cubic_wage_exper_spline_even
twoway (scatter wage exper)(line cubic_wage_exper_spline_even exper, sort), ytitle(Wage) xtitle(Experience) legend(off) note("Fig 7. Relationship between experience and wage: using cubic regression. Knots at (15,30,40)") title("Cubic: Evenly Spaced Knots") name(Cubic2)

//Create a plot of all the fits: linear, polynomial, cubic
twoway (scatter wage exper)(line linear_wage_exper quad_wage_exper cubic_wage_exper_spline exper, sort), ytitle(Wage) xtitle(Experience) legend(label(1 "Observed") label(2 "Linear Regression") label(3 "Polynomial Regression") label(4 "Cubic Regrssion")) note("Fig 8. Relationship between experience and wage") title("Linear vs Quadratic vs Cubic") name(All)
