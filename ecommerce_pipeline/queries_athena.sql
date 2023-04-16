--Queries on Athena

--Customers with most seles
    SELECT c.name, SUM(o.total) as total_sales
    FROM processed_orders o 
    JOIN processed_customers c ON o.customer_id = c.id
    GROUP BY c.name
    ORDER BY total_sales DESC;

--Categories with most sales
    SELECT p.category, SUM(o.total) as total_sales
    FROM processed_orders o 
    JOIN processed_products p ON o.product_id = p.id
    GROUP BY p.category
    ORDER BY total_sales DESC;

--Quantity of orders per customer
    SELECT c.name, COUNT(o.id) as total_orders
    FROM processed_orders o 
    JOIN processed_customers c ON o.customer_id = c.id
    GROUP BY c.name
    ORDER BY total_orders DESC;

--spending average per order
    SELECT c.name, AVG(o.total) as avg_order_total
    FROM processed_orders o 
    JOIN processed_customers c ON o.customer_id = c.id
    GROUP BY c.name
    ORDER BY avg_order_total DESC;

--Total quantity of products sold per category
    SELECT p.category, SUM(o.quantity) as total_quantity
    FROM processed_orders o 
    JOIN processed_products p ON o.product_id = p.id
    GROUP BY p.category
    ORDER BY total_quantity DESC;