SELECT [Country Code]
	,[Country Name]
FROM [dCountry];

SELECT [Customer No]
	,[Name] AS 'Customer Name'
	,[Country Code]
	,[Currency Code]
	,[Email]
	,[Type of Supply]
	,[Salesperson Code] AS 'Salesperson'
FROM [dCustomer];

SELECT [Date Key]
	,[Posting Date]
	,[Customer No]
	,[Document No]
	,[Order No]
	,[Salesperson Code] AS 'Salesperson'
	,[Country Code]
	,[Entity]
	,[Sales Type]
	,LEFT([Item No], 3) AS 'Brand Code'
	,[Item No]
	,[Quantity]
	,[GBP Sales]
	,[GBP Adjusted Margin] AS 'GBP Margin'
	,[EUR Sales]
	,[EUR Adjusted Margin] AS 'EUR Margin'
	,[USD Sales]
	,[USD Adjusted Margin] AS 'USD Margin'
FROM [fSales]
WHERE [Posting Date] >= '2022-05-01';

SELECT it.[Item No]
	,it.[Vendor Reference]
	,it.[Description]
	,it.[Description 2]
	,it.[Colours]
	,it.[Size 1]
	,it.[Size 1 Unit]
	,it.[Season]
	,it.[Category Code] AS 'Category'
	,it.[Group Code] AS 'Product Group'
	,it.[EAN Barcode]
	,it.[Tariff No]
	,it.[Style Ref]
	,it.[GBP Trade]
	,it.[GBP SRP]
	,it.[EUR Trade]
	,it.[EUR SRP]
	,it.[USD Trade]
	,it.[USD SRP]
	,it.[Nav Vendor No] AS [Vendor No]
	,it.[COO]
	,(
		SELECT TOP 1 [Image URL]
		FROM [dImage]
		WHERE [Item No] = it.[Item No]
		ORDER BY CHARINDEX('_', [image URL]) ASC
		) AS 'Image URL'
	,it.[Ltd Blocked] AS [Blocked]
	,it.[On Sale] AS 'Pref Sale'
	,it.[Bread & Butter]
FROM [dItem] AS it;

SELECT [Date Key]
	,CAST([Date] AS DATE) AS 'Date'
	,[Year]
	,[Financial Year Full] AS 'Financial Year'
	,[Quarter Full] AS 'Quarter'
	,[Financial Quarter Full] AS 'Financial Quarter'
	,[Month No] AS 'Month No'
	,[Financial Month] AS 'Financial Month No'
	,[Month Name]
	,[ISO Week No] AS 'ISO Week No'
	,[Day of Week] + 1 AS 'Day of Week No'
	,[Day] AS 'Day of Month No'
	,[Day of Year] AS 'Day of Year No'
	,[Day Name]
FROM [dDate]
WHERE [Date] BETWEEN '2022-05-01' AND '2026-04-30'
ORDER BY [Date] ASC;

SELECT [Brand Code]
	,[Brand Name]
	,[Buying Category]
	,[Status]
FROM dBrand;

SELECT [ETA Date]
	,[Document No] AS 'PO No'
	,[Vendor No]
	,[Entity]
	,[Item No]
	,[Currency]
	,[Line Total] AS 'Value'
	,[Outstanding Value] AS 'Outstanding Value'
	,[Quantity]
	,[Qty Received]
	,[Outstanding Qty]
	,[Reserved Qty]
	,[PO Freestock] AS 'PO Freestock Qty'
FROM [fPurchases];

SELECT ob.[Document No] AS 'Sales Order'
	,ob.[Entity]
	,ob.[Order Date]
	,ob.[Location Code]
	,ob.[Shipment Date]
	,ob.[Shiner Ref]
	,CASE 
		WHEN SUBSTRING([Shiner Ref], 8, LEN([Shiner Ref])) LIKE 
			'[Ss][Tt][Oo][Cc][Kk]%'
			THEN 'At Once'
		WHEN cu.[Name] LIKE '%D2C%'
			THEN 'At Once'
		WHEN cu.[Name] LIKE '%Shiner%'
			THEN 'At Once'
		ELSE 'Preorder'
		END AS 'Order Type'
	,CASE 
		WHEN ob.[Customer No] IN (
				SELECT DISTINCT [Customer No]
				FROM [dCustomer]
				WHERE [Name] LIKE '%D2C%'
				)
			THEN ob.[Shipment Date]
		WHEN ob.[Shiner Ref] IS NULL
			THEN ob.[Shipment Date]
		WHEN ob.[Shiner Ref] NOT LIKE '[0-9][0-9][wW][kK][0-9][0-9]%'
			THEN ob.[Shipment Date]
		WHEN ob.[Shiner Ref] LIKE '[0-9][0-9][wW][kK][0-9][0-9]%'
			THEN CAST(DATEADD(DAY, - 1, DATEADD(DAY, (
								8 - DATEPART(WEEKDAY, DATEADD(WEEK, CAST(SUBSTRING(
												ob.[Shiner Ref], 5, 2) AS INT) - 1, 
										DATEADD(YEAR, (
												CAST(LEFT(ob.[Shiner Ref], 2) AS 
													INT) + 2000
												) - 1900, 0))) + 1
								) % 7, DATEADD(WEEK, CAST(SUBSTRING(ob.[Shiner Ref], 
										5, 2) AS INT) - 1, DATEADD(YEAR, (CAST(LEFT(ob.[Shiner Ref], 2) AS INT) + 2000
										) - 1900, 0)))) AS DATE)
		END AS 'Reporting Date'
	,CASE 
		WHEN ob.[Release Status] = 'Released'
			THEN 'Released'
		WHEN ob.[Release Status] = 'Pending Aproval'
			THEN 'Pending Approval'
		WHEN (
				SELECT COUNT(*)
				FROM [fOrderbook]
				WHERE [Item No] IS NOT NULL
					AND LEFT([Document No], 3) NOT IN ('SRO', 'USR', 'USI', 'SQ-'
						)
					AND [Outstanding Value] > 0
					AND [Document No] = ob.[Document No]
					AND [Entity] = ob.[Entity]
					AND [Location Code] = ob.[Location Code]
				) = (
				SELECT COUNT(*)
				FROM [fOrderbook]
				WHERE [Item No] IS NOT NULL
					AND LEFT([Document No], 3) NOT IN ('SRO', 'USR', 'USI', 'SQ-'
						)
					AND [Outstanding Value] > 0
					AND [Document No] = ob.[Document No]
					AND [Entity] = ob.[Entity]
					AND [Location Code] = ob.[Location Code]
					AND [SKU Status] = 'SKU Ready'
				)
			THEN 'Ready'
		WHEN (
				SELECT COUNT(*)
				FROM [fOrderbook]
				WHERE [Item No] IS NOT NULL
					AND LEFT([Document No], 3) NOT IN ('SRO', 'USR', 'USI', 'SQ-'
						)
					AND [Outstanding Value] > 0
					AND [Document No] = ob.[Document No]
					AND [Entity] = ob.[Entity]
					AND [Location Code] = ob.[Location Code]
					AND [SKU Status] = 'SKU Ready'
					AND [Order Status] = 'Not Ready'
				) > 0
			THEN 'Part Ready'
		WHEN (
				SELECT COUNT(*)
				FROM [fOrderbook]
				WHERE [Item No] IS NOT NULL
					AND LEFT([Document No], 3) NOT IN ('SRO', 'USR', 'USI', 'SQ-'
						)
					AND [Outstanding Value] > 0
					AND [Document No] = ob.[Document No]
					AND [Entity] = ob.[Entity]
					AND [Location Code] = ob.[Location Code]
				) = (
				SELECT COUNT(*)
				FROM [fOrderbook]
				WHERE [Item No] IS NOT NULL
					AND LEFT([Document No], 3) NOT IN ('SRO', 'USR', 'USI', 'SQ-'
						)
					AND [Outstanding Value] > 0
					AND [Document No] = ob.[Document No]
					AND [Entity] = ob.[Entity]
					AND [Location Code] = ob.[Location Code]
					AND [SKU Status] IN ('SKU PO Reserved', 'SKU Mixed Reservations'
						)
				)
			THEN 'Reserved'
		WHEN (
				SELECT COUNT(*)
				FROM [fOrderbook]
				WHERE [Item No] IS NOT NULL
					AND LEFT([Document No], 3) NOT IN ('SRO', 'USR', 'USI', 'SQ-'
						)
					AND [Outstanding Value] > 0
					AND [Document No] = ob.[Document No]
					AND [Entity] = ob.[Entity]
					AND [Location Code] = ob.[Location Code]
					AND [SKU Status] IN ('Not Reserved', 'SKU Not Fully Reserved'
						)
				) > 0
			THEN 'Pending'
		END AS 'Status'
	,ob.[Customer No]
	,ob.[Item No]
	,ob.[Quantity]
	,ob.[Outstanding Qty]
	,ob.[Currency]
	,ob.[Line Total] AS 'Value'
	,ob.[Outstanding Value] AS 'Outstanding Value'
FROM [fOrderbook] AS ob
LEFT JOIN [dCustomer] AS cu
	ON ob.[Customer No] = cu.[Customer No]
WHERE ob.[Item No] IS NOT NULL
	AND LEFT(ob.[Document No], 3) NOT IN ('SRO', 'USR', 'USI', 'SQ-');

SELECT [Item No]
      ,[Entity]
      ,[Free Stock]
      ,[Inventory]
FROM [dInventory];