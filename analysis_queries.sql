-- a. Average loan amount for borrowers who are more than 5 days past due
SELECT AVG([Loan Amount]) as average_loan_amount
FROM borrowers
WHERE [Days Left to Pay Current EMI] <= 5;

-- b. Top 10 borrowers with the highest outstanding balance
SELECT Name, [Loan Amount] 
FROM borrowers 
ORDER BY [Loan Amount] DESC 
LIMIT 10;

-- c. List of all borrowers with good repayment history
SELECT Name 
FROM borrowers 
WHERE [Delayed Payment] = 'No';

-- d. Brief analysis with respect to loan type
SELECT [Loan Type], 
       COUNT(*) as Count, 
       AVG([Loan Amount]) as Avg_Loan_Amount,
       AVG([Interest Rate]) as Avg_Interest_Rate
FROM borrowers 
GROUP BY [Loan Type];
