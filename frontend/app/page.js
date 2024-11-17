import { useSearchParams } from "next/navigation";

export default async function CarsPage({ searchParams }) {
  const page = searchParams?.page || 1; 
  const limit = 10;

  const response = await fetch(
    `https://your-api-url/cars?limit=${limit}&offset=${(page - 1) * limit}`
  );
  const cars = await response.json();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Cars</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-200">
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
          <tbody>
            {cars.map((car) => (
              <tr key={car.vin} className="hover:bg-gray-100">
                <td className="border border-gray-300 px-4 py-2">{car.vin}</td>
                <td className="border border-gray-300 px-4 py-2">{car.make}</td>
                <td className="border border-gray-300 px-4 py-2">{car.model}</td>
                <td className="border border-gray-300 px-4 py-2">{car.year}</td>
                <td className="border border-gray-300 px-4 py-2">{car.color}</td>
                <td className="border border-gray-300 px-4 py-2">${car.price}</td>
                <td className="border border-gray-300 px-4 py-2">{car.mileage} miles</td>
                <td className="border border-gray-300 px-4 py-2">{car.locationid}</td>
                <td className="border border-gray-300 px-4 py-2">{car.lastmodifiedby}</td>
                <td className="border border-gray-300 px-4 py-2">{car.warrantyid}</td>
                <td className="border border-gray-300 px-4 py-2 capitalize">{car.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex justify-between mt-4">
        <a
          href={`?page=${Math.max(1, page - 1)}`}
          className={`${
            page <= 1 ? "pointer-events-none opacity-50" : ""
          } bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600`}
        >
          Previous
        </a>
        <a
          href={`?page=${page + 1}`}
          className="bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600"
        >
          Next
        </a>
      </div>
    </div>
  );
}
