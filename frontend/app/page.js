"use client";
import { useState, useEffect } from "react";

export default function CarsPage({ searchParams }) {
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const page = parseInt(searchParams?.page || 1, 10); // Default to page 1
  const limit = 10;

  useEffect(() => {
    const fetchCars = async () => {
      try {
        setLoading(true);
        const response = await fetch(
          `http://127.0.0.1:8000/api/cars/?limit=${limit}&offset=${(page - 1) * limit}`
        );
        if (!response.ok) {
          throw new Error(`Failed to fetch: ${response.statusText}`);
        }
        const data = await response.json();
        setCars(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCars();
  }, [page]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="container mx-auto px-5 py-8 text-indigo-950">
      <h1 className="text-2xl font-bold mb-6 text-center">Dealership Management</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full table-auto border-collapse border border-gray-300">
          <thead>
            <tr className="bg-indigo-100">
              <th className="border border-gray-300 px-4 py-2">VIN</th>
              <th className="border border-gray-300 px-4 py-2">Make</th>
              <th className="border border-gray-300 px-4 py-2">Model</th>
              <th className="border border-gray-300 px-4 py-2">Year</th>
              <th className="border border-gray-300 px-4 py-2">Color</th>
              <th className="border border-gray-300 px-4 py-2">Price</th>
              <th className="border border-gray-300 px-4 py-2">Mileage</th>
              <th className="border border-gray-300 px-4 py-2">Location ID</th>
              <th className="border border-gray-300 px-4 py-2">Last Modified By</th>
              <th className="border border-gray-300 px-4 py-2">Warranty ID</th>
              <th className="border border-gray-300 px-4 py-2">Status</th>
            </tr>
          </thead>
          <tbody className="bg-slate-50">
            {cars.map((car) => (
              <tr key={car.vin} className="hover:bg-indigo-50">
                <td className="text-sm border border-gray-300 px-4 py-2 break-words">
                  {car.vin}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2 capitalize">
                  {car.make}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2 capitalize">
                  {car.model}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.year}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2 capitalize">
                  {car.color}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  ${car.price}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.mileage} miles
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.locationid}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.lastmodifiedby}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.warrantyid}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2 capitalize">
                  {car.status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex justify-center mt-4">
        <a
          href={`?page=${Math.max(1, page - 1)}`}
          className={`${
            page <= 1 ? "pointer-events-none opacity-50" : ""
          } text-sm px-3 py-1 mx-1 border rounded bg-indigo-200 hover:bg-gray-300`}
        >
          &#8592;
        </a>
        <span className="text-sm font-bold px-3 py-1 mx-1">{page}</span>
        <a
          href={`?page=${page + 1}`}
          className="text-sm px-3 py-1 mx-1 border rounded bg-indigo-200 hover:bg-gray-300"
        >
          &#8594;
        </a>
      </div>
    </div>
  );
}
