export default async function Home() {
    const cars = [
      {
        vin: "0040MA88PK5BBO38F",
        color: "silver",
        price: "50178.00",
        mileage: 60000,
        status: "available",
        make: "toyota",
        model: "rav 4",
        year: 2017,
        locationid: 1,
        lastmodifiedby: 1,
        warrantyid: null,
      },
      {
        vin: "0040MB99XY7ZZ1234",
        color: "black",
        price: "35000.00",
        mileage: 30000,
        status: "sold",
        make: "honda",
        model: "civic",
        year: 2020,
        locationid: 2,
        lastmodifiedby: 2,
        warrantyid: null,
      },
      // Add more car objects here...
    ];
  
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
      </div>
    );
}
