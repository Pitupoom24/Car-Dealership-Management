"use client"; // Ensure it's a Client Component

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

export default function DetailsPage() {
  const searchParams = useSearchParams();



  const warrantyid = searchParams.get("warrantyid");

  // State for storing the car details

  const [warrantyDetail, setwarrantyDetail] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  
  const fetchWarrantyDetail = async () => {
    setLoading(true);
    const apiURL_details = `http://127.0.0.1:8000/api/warranties/retrieve_by_warrantyid/?warrantyid=${warrantyid}`;

    try {
      const response = await fetch(apiURL_details);
      if (!response.ok) {
        return; // no details
      }
      const data = await response.json();
      
      

      setwarrantyDetail(data); // Store the fetched data
    } catch (err) {
      setError(err.message); // Handle errors
    } finally {
      setLoading(false); // Set loading to false after fetching
    }
  };




  useEffect(() => {
    fetchWarrantyDetail();
   
  }, [warrantyid]); // Re-run the effect if any parameter changes

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1 className="text-5xl font-bold text-center bg-gradient-to-r from-blue-800 to-purple-400 bg-clip-text text-transparent my-6">
        Warranty Details
      </h1>
      <div className="space-y-6">
        {warrantyDetail.length > 0 ? (
          warrantyDetail.map((car) => (
            <div
              key={car.warrantyid}
              className="mx-28 bg-gradient-to-r from-purple-200 to-purple-400 p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300"

            >
              <p className="text-xl font-semibold">
              Warranty ID:{" "}
                <span className="font-normal">{car.warrantyid}</span>
              </p>
              <p className="text-xl font-semibold">
                start date:{" "}
                <span className="font-normal">{car.enddate}</span>
              </p>
              <p className="text-xl font-semibold">
              end detail:{" "}
                <span className="font-normal">{car.coveragedetail}</span>
              </p>
              
            </div>
          ))
        ) : (
          <div className="mx-28 bg-gradient-to-r from-purple-200 to-purple-400 p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
            <p className="text-center">No details available.</p>
          </div>
        )}
      </div>

      <h1 className="text-5xl font-bold text-center bg-gradient-to-r from-green-800 to-green-400 bg-clip-text text-transparent mt-20 mb-6">
       
      </h1>
      
    </div>
  );
}
