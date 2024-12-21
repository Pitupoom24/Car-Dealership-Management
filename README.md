# **Car Dealership Management**
*Car Dealership Management* is a web-based platform developed using Next.js and Django to streamline car dealership operations, supporting over 20,000 car listings and 75,000+ reviews across multiple branches. The system leverages MySQL hosted on GCP to ensure real-time data access and updates. Key features include advanced database management with 4 triggers and 2 stored procedures, utilizing serializable transaction isolation to dynamically adjust car prices based on demand and mileage, maintaining consistency during concurrent operations. Additionally, a Vehicle Display Optimizer was created, incorporating weighted scoring algorithms based on customer preferences, vehicle features, sales trends, and inventory metrics, enhancing the accuracy of car selection for users.

## **Key Features**
1) **Search Functionality**: Enables users to search for vehicles based on various criteria such as VIN, make, model, year, price, mileage, rating, and other key specifications.
2) **Create, Update, and Delete Vehicle Entries**: Provides the ability to add, modify, or remove car listings within the system, ensuring inventory management flexibility.
3) **User Authentication**: Provides secure login functionality to authenticate users, with the userID displayed when updating or adding a vehicle, ensuring proper attribution and accountability.
4) **Vehicle Details and Reviews**: Allows users to view detailed information, reviews, and comments for each vehicle, assisting in informed decision-making.
5) **Quick Access to Top Listings**: Provides users with a fast overview of the higher rating cars in the dealership.
6) **Dynamic Price Adjustment**: Automatically adjusts vehicle prices based on demand and mileage, offering a responsive and market-sensitive pricing model.
7) **Advanced Search - Vehicle Display Optimizer**: Utilizes a weighted scoring algorithm that factors in customer preferences, vehicle features, sales trends, and inventory data to recommend the most relevant cars to users, enhancing their ability to find the ideal vehicle.

## **Installation**
### Run the Server for the Frontend (Next.js)
1) `cd frontend`
2) `npm run dev`

### Google Cloud Platform (GCP) Setup
1) `.\cloud-sql-proxy matrix-437219:us-central1:db-matrix`

### Run the Server for the Backend (Django)
1) `cd backend`
2) `python manage.py runserver`

## **Group members**
1) Pitupoom Soontornthanon
2) Matupoom Soontornthanon
3) Alondra Gonzalez
4) Praise Daniels
