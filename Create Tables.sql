CREATE TABLE Country (
	"Country Code" NVARCHAR(20) NOT NULL PRIMARY KEY
	,"Country Name" NVARCHAR(100) NULL
	);

CREATE TABLE Customers (
	"Customer No" NVARCHAR(50) NOT NULL PRIMARY KEY
	,"Customer Name" NVARCHAR(300) NULL
	,"Country Code" NVARCHAR(20) NULL
	,"Currency Code" NVARCHAR(20) NULL
	,"Email" NVARCHAR(200) NULL
	,"Type of Supply" NVARCHAR(100) NULL
	,"Salesperson" NVARCHAR(100) NULL
	);

CREATE TABLE Sales (
	"Date Key" NVARCHAR(50) NOT NULL
	,"Posting Date" DATE NULL
	,"Customer No" NVARCHAR(50) NOT NULL
	,"Document No" NVARCHAR(50) NOT NULL
	,"Order No" NVARCHAR(50) NULL
	,"Salesperson" NVARCHAR(100) NULL
	,"Country Code" NVARCHAR(50) NULL
	,"Entity" NVARCHAR(50) NOT NULL
	,"Sales Type" NVARCHAR(50) NULL
	,"Brand Code" NVARCHAR(50) NULL
	,"Item No" NVARCHAR(50) NOT NULL
	,"Quantity" FLOAT(53) NULL
	,"GBP Sales" FLOAT(53) NULL
	,"GBP Margin" FLOAT(53) NULL
	,"EUR Sales" FLOAT(53) NULL
	,"EUR Margin" FLOAT(53) NULL
	,"USD Sales" FLOAT(53) NULL
	,"USD Margin" FLOAT(53) NULL
	-- ,PRIMARY KEY (
	-- 	"Date Key"
	-- 	,"Customer No"
	-- 	,"Document No"
	-- 	,"Entity"
	-- 	,"Item No"
	-- 	)
	);

CREATE TABLE Items (
	"Item No" NVARCHAR(50) NOT NULL PRIMARY KEY
	,"Vendor Reference" NVARCHAR(50) NULL
	,"Description" NVARCHAR(50) NULL
	,"Description 2" NVARCHAR(50) NULL
	,"Colours" NVARCHAR(50) NULL
	,"Size 1" NVARCHAR(50) NULL
	,"Size 1 Unit" NVARCHAR(50) NULL
	,"Season" NVARCHAR(20) NULL
	,"Category" NVARCHAR(50) NULL
	,"Product Group" NVARCHAR(50) NULL
	,"EAN Barcode" NVARCHAR(50) NULL
	,"Tariff No" NVARCHAR(50) NULL
	,"Style Ref" NVARCHAR(300) NULL
	,"GBP Trade" DECIMAL(18, 4) NULL
	,"GBP SRP" DECIMAL(18, 4) NULL
	,"EUR Trade" DECIMAL(18, 4) NULL
	,"EUR SRP" DECIMAL(18, 4) NULL
	,"USD Trade" DECIMAL(18, 4) NULL
	,"USD SRP" DECIMAL(18, 4) NULL
	,"Vendor No" NVARCHAR(50) NULL
	,"COO" NVARCHAR(20) NULL
	,"Image URL" NVARCHAR(300) NULL
	,"Blocked" NVARCHAR(20) NULL
	,"Pref Sale" NVARCHAR(20) NULL
	,"Bread & Butter" NVARCHAR(20) NULL
	);

CREATE TABLE Date (
	"Date Key" NVARCHAR(50) NOT NULL PRIMARY KEY
	,"Date" DATE NOT NULL
	,"Year" INTEGER NOT NULL
	,"Financial Year" NVARCHAR(20) NOT NULL
	,"Quarter" NVARCHAR(20) NOT NULL
	,"Financial Quarter" NVARCHAR(20) NOT NULL
	,"Month No" INTEGER NOT NULL
	,"Financial Month No" INTEGER NOT NULL
	,"Month Name" NVARCHAR(50) NOT NULL
	,"ISO Week No" INTEGER NOT NULL
	,"Day of Week No" INTEGER NOT NULL
	,"Day of Month No" INTEGER NOT NULL
	,"Day of Year No" INTEGER NOT NULL
	,"Day Name" NVARCHAR(30) NOT NULL
	);

CREATE TABLE Brand (
	"Brand Code" NVARCHAR(10) NOT NULL PRIMARY KEY
	,"Brand Name" NVARCHAR(100) NULL
	,"Buying Category" NVARCHAR(100) NULL
	,"Status" NVARCHAR(100) NULL
	);

CREATE TABLE Purchases (
	"ETA Date" DATE NULL
	,"PO No" NVARCHAR(50) NOT NULL
	,"Vendor No" NVARCHAR(50) NOT NULL
	,"Vendor Name" NVARCHAR(300) NULL
	,"Entity" NVARCHAR(50) NOT NULL
	,"Item No" NVARCHAR(50) NULL
	,"Currency" NVARCHAR(10) NULL
	,"Value" FLOAT(53) NULL
	,"Outstanding Value" FLOAT(53) NULL
	,"Quantity" FLOAT(53) NULL
	,"Qty Received" FLOAT(53) NULL
	,"Outstanding Qty" FLOAT(53) NULL
	,"Reserved Qty" FLOAT(53) NULL
	,"PO Freestock Qty" FLOAT(53) NULL
	-- ,PRIMARY KEY (
	-- 	"PO NO"
	-- 	,"Vendor No"
	-- 	,"Entity"
	-- 	)
	);

CREATE TABLE Orderbook (
	"Sales Order" NVARCHAR(50) NOT NULL
	,"Entity" NVARCHAR(50) NOT NULL
	,"Order Date" DATE NULL
	,"Location Code" NVARCHAR(100) NOT NULL
	,"Shipment Date" DATE NULL
	,"Shiner Ref" NVARCHAR(50) NULL
	,"Order Type" NVARCHAR(30) NULL
	,"Reporting Date" DATE NULL
	,"Status" NVARCHAR(50) NULL
	,"Customer No" NVARCHAR(50) NOT NULL
	,"Item No" NVARCHAR(50) NOT NULL
	,"Quantity" FLOAT(53) NULL
	,"Outstanding Qty" FLOAT(53) NULL
	,"Currency" NVARCHAR(10) NULL
	,"Value" FLOAT(53) NULL
	,"Outstanding Value" FLOAT(53) NULL
	-- PRIMARY KEY (
	-- 	"Sales Order"
	-- 	,"Entity"
	-- 	,"Location Code"
	-- 	,"Customer No"
	-- 	,"Item No"
	-- 	)
	);

CREATE TABLE Inventory (
	"Item No" NVARCHAR(50) NOT NULL
	,"Entity" NVARCHAR(50) NOT NULL
	,"Free Stock" FLOAT NULL
	,"Inventory" FLOAT NULL
	);