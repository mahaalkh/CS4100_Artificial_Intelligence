- For question 1: 
	I broke the elements in the game into pallets, food, and ghost. For each of the elements, I computed the desirable values as multiple reciprocals of the value and the non-desirable values as negative multiples of the values. 

	The score is a linear combination of the above mentioned values, unless the following occurs: 

		I also considered that winning the game is very desirable and so I return +inf if the successor state leads to winning.  

		I also considered that finishing the food in the game is undesirable and so I return +inf if the successor state leads to eating all the food.  

		I also considered that losing the game is undesirable and so I return -inf if the successor state leads to losing.  

		I also considered that staying in the same position the game is undesirable and so I return -inf if the successor state leads to staying in the same position.  

------------------------------------------------

- For question 5: 
	The process was the same as question 1 except I did not considered that staying in the same position in the game because I am not given the previous position because I am only looking at the current gameState. 

- estimated time: 

               - 6 hrs for Question 2, 3, 4

               - 5 hrs for Question 5  

               - 4 hrs for Question 1
               ------------------------------
               TOTAL TIME : 15