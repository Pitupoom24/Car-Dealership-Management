"use client"; // Ensure it's a Client Component

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

export default function DetailsPage() {
  const searchParams = useSearchParams();



  const employeeid = searchParams.get("employeeid");

  // State for storing the car details

  const [employeeDetail, setemployeeDetail] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  
  const fetchEmployeeDetails = async () => {
    setLoading(true);
    const apiURL_details = `http://127.0.0.1:8000/api/employees/retrieve_by_employeeid/?employeeid=${employeeid}`;

    try {
      const response = await fetch(apiURL_details);
      if (!response.ok) {
        return; // no details
      }
      const data = await response.json();
      
      

      setemployeeDetail(data); // Store the fetched data
    } catch (err) {
      setError(err.message); // Handle errors
    } finally {
      setLoading(false); // Set loading to false after fetching
    }
  };




  useEffect(() => {
    fetchEmployeeDetails();
   
  }, [employeeid]); // Re-run the effect if any parameter changes

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="  h-screen">
      <h1 className="text-5xl font-bold text-center bg-gradient-to-r from-blue-800 to-purple-400 bg-clip-text text-transparent my-6">
        Employee Details
      </h1>
      <div className="space-y-6 ">
        {employeeDetail.length > 0 ? (
          employeeDetail.map((e) => (
            <div
            key={e.employeeid}
            className="mx-28 bg-blue-200 p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300  flex flex-col"
          >
            <p className="text-xl font-semibold flex-grow mb-4 text-[#000000]">
              Employee Id:{" "}
              <span className="font-normal w-full block">{e.employeeid}</span>
            </p>
            <p className="text-xl font-semibold flex-grow mb-4">
              First Name:{" "}
              <span className="font-normal w-full block">{e.firstname}</span>
            </p>
            <p className="text-xl font-semibold flex-grow mb-4">
              Last Name:{" "}
              <span className="font-normal w-full block">{e.lastname}</span>
            </p>
            <p className="text-xl font-semibold flex-grow mb-4">
              Email:{" "}
              <span className="font-normal w-full block">{e.email}</span>
            </p>
            <p className="text-xl font-semibold flex-grow mb-4">
              Location ID:{" "}
              <span className="font-normal w-full block">{e.locationid}</span>
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
