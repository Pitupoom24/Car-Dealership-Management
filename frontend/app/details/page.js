"use client"; // Ensure it's a Client Component

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

export default function DetailsPage() {
  const searchParams = useSearchParams();

  // Access the query parameters
  const make = searchParams.get("make");
  const model = searchParams.get("model");
  const year = searchParams.get("year");

  // State for storing the car details
  const [carDetails, setCarDetails] = useState([]);
  const [carReviews, setCarReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data from the API
  const fetchCarDetails = async () => {
    setLoading(true);
    const apiURL_details = `http://127.0.0.1:8000/api/details/retrieve_by_make_model_year/?make=${make}&model=${model}&year=${year}`;
    try {
      const response = await fetch(apiURL_details);
      if (!response.ok) {
        return; // no details
      }
      const data = await response.json();

      setCarDetails(data); // Store the fetched data
    } catch (err) {
      setError(err.message); // Handle errors
    } finally {
      setLoading(false); // Set loading to false after fetching
    }
  };

  // Fetch data from the API
  const fetchCarReviews = async () => {
    setLoading(true);
    const apiURL_reviews = `http://127.0.0.1:8000/api/reviews/retrieve_by_make_model_year/?make=${make}&model=${model}&year=${year}`;
    try {
      const response = await fetch(apiURL_reviews);
      if (!response.ok) {
        return; // no reviews
      }
      const data = await response.json();

      setCarReviews(data); // Store the fetched data
    } catch (err) {
      setError(err.message); // Handle errors
    } finally {
      setLoading(false); // Set loading to false after fetching
    }
  };

  useEffect(() => {
    fetchCarDetails();
    fetchCarReviews();
  }, [make, model, year]); // Re-run the effect if any parameter changes

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!carDetails) {
    return <div>No details found for this car.</div>;
  }

  return (
    <div>
      <h1 className="text-5xl font-bold text-center text-blue-800 my-6">
        Details
      </h1>
      <div className="space-y-6">
        {carDetails.length > 0 ? (
          carDetails.map((car) => (
            <div
              key={car.id}
              className="mx-28 bg-blue-100 p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300"
            >
              <p className="text-xl font-semibold text-gray-700">
                Make:{" "}
                <span className="font-normal text-gray-500">{car.make}</span>
              </p>
              <p className="text-xl font-semibold text-gray-700">
                Model:{" "}
                <span className="font-normal text-gray-500">{car.model}</span>
              </p>
              <p className="text-xl font-semibold text-gray-700">
                Year:{" "}
                <span className="font-normal text-gray-500">{car.year}</span>
              </p>
              <p className="text-xl font-semibold text-gray-700">
                Number of Cylinders:{" "}
                <span className="font-normal text-gray-500">
                  {car.numberofcylinders}
                </span>
              </p>
              <p className="text-xl font-semibold text-gray-700">
                Transmission:{" "}
                <span className="font-normal text-gray-500">
                  {car.transmission}
                </span>
              </p>
              <p className="text-xl font-semibold text-gray-700">
                Drive Wheel:{" "}
                <span className="font-normal text-gray-500">
                  {car.drivewheel}
                </span>
              </p>
            </div>
          ))
        ) : (
          <div className="mx-28 bg-green-100 p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
            <p className="text-center">No details available.</p>
          </div>
        )}
      </div>

      <h1 className="text-5xl font-bold text-center text-green-800 mt-20 mb-6">
        Reviews
      </h1>
      <div className="space-y-6">
        {carReviews.length > 0 ? (
          carReviews.map((car) => (
            <div
              key={car.reviewid}
              className="mx-28 bg-green-100 p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300"
            >
              <p className="text-xl font-semibold text-gray-700">
                Review ID:{" "}
                <span className="font-normal text-gray-500">
                  {car.reviewid}
                </span>
              </p>
              <p className="text-xl font-semibold text-gray-700">
                Rating:{" "}
                <span className="font-normal text-gray-500">{car.rating}</span>
              </p>
              <p className="text-xl font-semibold text-gray-700">
                Comment:{" "}
                <span className="font-normal text-gray-500">{car.comment}</span>
              </p>
            </div>
          ))
        ) : (
          <div className="mx-28 bg-green-100 p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
            <p className="text-center">No reviews available.</p>
          </div>
        )}
      </div>
    </div>
  );
}
