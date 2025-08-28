SELECT paymentDate, SUM(amount) AS total_amount
FROM payments
GROUP BY paymentDate
ORDER BY paymentDate DESC
LIMIT 5;
SELECT customerName, country, AVG(creditLimit) AS average_credit_limit
FROM customers
GROUP BY customerName, country;