examples = [
    {
        "input": "List the top 10 styles sold by total GBP sales for Shiner B.V in the month of October 2023.",
        "query": """
SELECT it."Description",
       it."Description 2",
       it."Colours",
       SUM(sl."GBP Sales") AS "Total GBP Sales" 
FROM Sales AS sl
LEFT JOIN Items AS it 
	ON sl."Item No" = it."Item No"
LEFT JOIN Date AS dt
	ON sl."Date Key" = dt."Date Key"
	
WHERE sl."Entity" = 'Shiner B.V'
	AND dt."Month Name" = 'October'
	AND dt."Year" = 2023
	
GROUP BY it."Description", it."Description 2", it."Colours"
ORDER BY "Total GBP Sales" DESC
LIMIT 10;
     """,
    },
    {
        "input": "How much did we invoice in February 2024 for the salesperson LOUISH",
        "query": """
SELECT SUM(sl."GBP Sales") AS "GBP Sales"
	,SUM(sl."EUR Sales") AS "EUR Sales"
	,SUM(sl."USD Sales") AS "USD Sales"
FROM Sales AS sl
LEFT JOIN Date AS dt
	ON sl."Date Key" = dt."Date Key"
WHERE dt."Month Name" = 'March'
AND dt."Year" = 2024
AND sl."Salesperson" = 'LOUISH';
        """,
    },
    {
        "input": "How much did we invoice in March 2024 by entity for the salesperson LOUISH",
        "query": """
SELECT sl."Entity"
	,SUM(sl."GBP Sales") AS "GBP Sales"
	,SUM(sl."EUR Sales") AS "EUR Sales"
	,SUM(sl."USD Sales") AS "USD Sales"
FROM Sales AS sl
LEFT JOIN Date AS dt
	ON sl."Date Key" = dt."Date Key"
WHERE dt."Month Name" = 'March'
AND dt."Year" = 2024
AND sl."Salesperson" = 'LOUISH'
GROUP BY sl."Entity"
ORDER BY CASE WHEN sl."Entity" = 'Shiner Ltd' THEN 1
			  WHEN sl."Entity" = 'Shiner B.V' THEN 2
			  WHEN sl."Entity" = 'Shiner LLC' THEN 2
			  END ASC;
        """,
    },
    {
        "input": "What was the total margin for customer CU106959 with a date range of 01/05/2023 to 31/07/2023",
        "query": """
SELECT sl."Customer No"
	,cu."Customer Name"
	,SUM(sl."GBP Margin") AS "GBP Margin"
	,SUM(sl."EUR Margin") AS "EUR Margin"
	,SUM(sl."USD Margin") AS "USD Margin"
FROM Sales AS sl
LEFT JOIN Customers AS cu
	ON sl."Customer No" = cu."Customer No"
WHERE sl."Customer No" = 'CU106959'
AND sl."Posting Date" BETWEEN '2023-05-01' AND '2023-07-31'
        """,
    },
    {
        "input": "Who were the top 10 customers by EUR Sales in France for the date range of 01/07/2023 to 31/01/2024",
        "query": """
SELECT sl."Customer No"
	,cu."Customer Name"
	,SUM(sl."EUR Sales") AS "EUR Sales"
FROM Sales AS sl
LEFT JOIN Customers AS cu
	ON sl."Customer No" = cu."Customer No"
LEFT JOIN Country AS co
	ON sl."Country Code" = co."Country Code"
WHERE co."Country Name" = 'France'
AND sl."Posting Date" BETWEEN '2023-07-01' AND '2024-01-31'
GROUP BY sl."Customer No"
	,cu."Customer Name"
ORDER BY SUM(sl."EUR Sales") DESC
LIMIT 10
        """,
    },
    {
        "input": "Which customers are up against last year for the month of February 2024",
        "query": """
WITH Last_Year AS (
    SELECT sl."Customer No"
           ,SUM(sl."GBP Sales") AS "LY GBP Sales"
    FROM Sales AS sl
    LEFT JOIN Date AS dt ON sl."Date Key" = dt."Date Key"
    WHERE dt."Month Name" = 'February' AND dt."Year" = 2023
    GROUP BY sl."Customer No"
)
,This_Year AS (
    SELECT sl."Customer No"
           ,SUM(sl."GBP Sales") AS "TY GBP Sales"
    FROM Sales AS sl
    LEFT JOIN Date AS dt ON sl."Date Key" = dt."Date Key"
    WHERE dt."Month Name" = 'February' AND dt."Year" = 2024
    GROUP BY sl."Customer No"
)
SELECT cu."Customer No"
       ,cu."Customer Name"
       ,COALESCE(ly."LY GBP Sales", 0) AS "LY GBP Sales"
       ,COALESCE(ty."TY GBP Sales", 0) AS "TY GBP Sales"
       ,COALESCE(ty."TY GBP Sales", 0) - COALESCE(ly."LY GBP Sales", 0) AS "GBP Sales Difference"
FROM Customers AS cu
LEFT JOIN Last_Year AS ly ON cu."Customer No" = ly."Customer No"
LEFT JOIN This_Year AS ty ON cu."Customer No" = ty."Customer No"
WHERE COALESCE(ty."TY GBP Sales", 0) - COALESCE(ly."LY GBP Sales", 0) > 0
ORDER BY COALESCE(ty."TY GBP Sales", 0) - COALESCE(ly."LY GBP Sales", 0) DESC;
        """,
    },
    {
        "input": "List the sales orders yet to be shipped for CU100487",
        "query": """
SELECT "Sales Order"
	,"Entity"
	,"Order Type"
	,"Status"
	,"Reporting Date"
	,"Currency"
	,SUM("Outstanding Qty") AS "Qty"
	,SUM("Outstanding Value") AS "Value"
FROM Orderbook
WHERE "Customer No" = 'CU100487'
GROUP BY "Sales Order"
	,"Entity"
	,"Order Type"
	,"Reporting Date"
	,"Currency"
ORDER BY "Reporting Date" ASC;
        """,
    },
    {
        "input": "Show me the order lines for yet to be shipped sales order ES-013063",
        "query": """
SELECT ob."Item No"
	,it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1"
	,it."Size 1 Unit"
	,ob."Currency"
	,SUM(ob."Outstanding Qty") AS "Qty"
	,SUM(ob."Outstanding Value") AS "Value"
FROM Orderbook AS ob
LEFT JOIN Items AS it
	ON ob."Item No" = it."Item No"
WHERE "Sales Order" = 'ES-013063'
GROUP BY ob."Item No"
	,it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1"
	,it."Size 1 Unit"
	,ob."Currency"
        """,
    },
    {
        "input": "give me a list of sales orders which are ready to ship for the salesperson KAISHAC",
        "query": """
SELECT ob."Sales Order"
	,ob."Customer No"
	,cu."Customer Name"
	,ob."Reporting Date"
	,ob."Status"
	,ob."Currency"
	,SUM(ob."Outstanding Qty") AS "Qty"
	,SUM(ob."Outstanding Value") AS "Value"
FROM Orderbook AS ob
LEFT JOIN Customers AS cu
	ON ob."Customer No" = cu."Customer No"
WHERE cu."Salesperson" = 'KAISHAC'
	AND ob."Status" = "Ready"
GROUP BY ob."Sales Order"
	,ob."Customer No"
	,cu."Customer Name"
	,ob."Reporting Date"
	,ob."Status"
	,ob."Currency"
ORDER BY ob."Reporting Date" ASC;
        """,
    },
    {
        "input": "Give me a list of Anti Hero decks with freestock available in Shiner Ltd",
        "query": """
SELECT iv."Item No"
	,it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1"
	,it."Size 1 Unit"
	,it."Category"
	,it."Product Group"
	,iv."Free Stock"
FROM Inventory AS iv
LEFT JOIN Items AS it
	ON iv."Item No" = it."Item No"
LEFT JOIN Brand AS br
	ON SUBSTR(iv."Item No", 1, 3) = br."Brand Code"
WHERE br."Brand Name" = 'Anti Hero'
	AND it."Product Group" = 'DECKS'
	AND iv."Entity" = 'Shiner Ltd'
	AND iv."Free Stock" > 0
ORDER BY iv."Free Stock" DESC;
        """,
    },
    {
        "input": "Give me a list of t-shirts and freestock qtys for Shiner B.V items which have screaming hand in description 2. Please return the list at sku level.",
        "query": """
SELECT iv."Item No"
	,it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1"
	,it."Size 1 Unit"
	,it."Category"
	,it."Product Group"
	,iv."Free Stock"
FROM Inventory AS iv
LEFT JOIN Items AS it
	ON iv."Item No" = it."Item No"
LEFT JOIN Brand AS br
	ON SUBSTR(iv."Item No", 1, 3) = br."Brand Code"
WHERE it."Product Group" = 'T-SHIRT'
	AND iv."Entity" = 'Shiner B.V'
	AND it."Description 2" LIKE '%screaming hand%'
	AND iv."Free Stock" > 0
        """,
    },
    {
        "input": "Give me a list of t-shirts and freestock qtys for Shiner B.V items which have screaming hand in description 2. Please return the list at style level.",
        "query": """
SELECT it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1 Unit"
	,it."Category"
	,it."Product Group"
	,SUM(iv."Free Stock") AS "Free Stock"
FROM Inventory AS iv
LEFT JOIN Items AS it
	ON iv."Item No" = it."Item No"
LEFT JOIN Brand AS br
	ON SUBSTR(iv."Item No", 1, 3) = br."Brand Code"
WHERE it."Product Group" = 'T-SHIRT'
	AND iv."Entity" = 'Shiner B.V'
	AND it."Description 2" LIKE '%screaming hand%'
	AND iv."Free Stock" > 0
GROUP BY it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1 Unit"
	,it."Category"
	,it."Product Group";
        """,
    },
    {
        "input": "Give me a list of freestock qtys for Shiner Ltd items which are fleece, have classic dot in description 2 and are size xl.",
        "query": """
SELECT iv."Item No"
	,it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1"
	,it."Size 1 Unit"
	,it."Category"
	,it."Product Group"
	,iv."Free Stock"
FROM Inventory AS iv
LEFT JOIN Items AS it
	ON iv."Item No" = it."Item No"
LEFT JOIN Brand AS br
	ON SUBSTR(iv."Item No", 1, 3) = br."Brand Code"
WHERE it."Product Group" = 'T-SHIRT'
	AND iv."Entity" = 'Shiner Ltd'
	AND it."Description 2" LIKE '%classic dot%'
	AND it."Size 1" = 'XL'
	AND iv."Free Stock" > 0
GROUP BY iv."Item No"
	,it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1"
	,it."Size 1 Unit"
	,it."Category"
	,it."Product Group"
	,iv."Free Stock";
        """,
    },
    {
        "input": "Give me a list of freestock qtys for Shiner Ltd items which are fleece, have classic dot in description 2 and are size xl.",
        "query": """
SELECT iv."Item No"
	,it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1"
	,it."Size 1 Unit"
	,it."Category"
	,it."Product Group"
	,iv."Free Stock"
FROM Inventory AS iv
LEFT JOIN Items AS it
	ON iv."Item No" = it."Item No"
LEFT JOIN Brand AS br
	ON SUBSTR(iv."Item No", 1, 3) = br."Brand Code"
WHERE it."Product Group" = 'T-SHIRT'
	AND iv."Entity" = 'Shiner Ltd'
	AND it."Description 2" LIKE '%classic dot%'
	AND it."Size 1" = 'XL'
	AND iv."Free Stock" > 0
GROUP BY iv."Item No"
	,it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1"
	,it."Size 1 Unit"
	,it."Category"
	,it."Product Group"
	,iv."Free Stock";
        """,
    },
    {
        "input": "What are the next five purchase orders arriving at Shiner Ltd that include decks which have quantities available for sale?",
        "query": """
SELECT DISTINCT po."PO No"
	,po."Vendor No"
	,po."Vendor Name"
	,po."ETA Date"
FROM Purchases AS po
LEFT JOIN Items AS it
	ON po."Item No" = it."Item No"
WHERE it."Product Group" = 'DECKS'
AND po."PO Freestock Qty" > 0
AND po."Entity" = 'Shiner Ltd'
ORDER BY po."ETA Date" ASC;
        """,
    },
    
    {
        "input": "Give me style level details for EP-004721",
        "query": """
SELECT DISTINCT po."Vendor No"
	,po."Vendor Name"
	,po."ETA Date"
	,it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1 Unit"
	,po."Currency"
	,SUM(po."Outstanding Qty") AS "Quantity"
	,SUM(po."Outstanding Value") AS "Value"
	,SUM(po."Reserved Qty") AS "Reserved Qty"
	,SUM(po."PO Freestock Qty") AS "Freestock Qty"
FROM Purchases AS po
LEFT JOIN Items AS it
	ON po."Item No" = it."Item No"
WHERE po."PO No" = 'EP-004721'
GROUP BY po."Vendor No"
	,po."Vendor Name"
	,po."ETA Date"
	,it."Description"
	,it."Description 2"
	,it."Colours"
	,it."Size 1 Unit"
	,po."Currency"
HAVING SUM(po."Outstanding Qty") > 0;
        """,
    },
]
