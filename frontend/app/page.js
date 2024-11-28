"use client";
import { useState, useEffect } from "react";

export default function CarsPage() {
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCar, setSelectedCar] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [formData, setFormData] = useState({
    make: "",
    model: "",
    lower_year: "",
    higher_year: "",
    lower_numberofcylinders: "",
    higher_numberofcylinders: "",
    transmission: "",
    drivewheel: "",
    vin: "",
    color: "",
    lower_price: "",
    higher_price: "",
    lower_mileage: "",
    higher_mileage: "",
    status: "",
    locationid: "",
    lower_rating: "",
    higher_rating: "",
  });

  // Get `page` parameter from URL manually
  const [page, setPage] = useState(1);
  const limit = 10;

  const fetchCars = async () => {
    try {
      setLoading(true);

      var url = `http://127.0.0.1:8000/api/advanced_queries/?limit=${limit}&offset=${(page - 1) * limit}`;

      for (const [key, value] of Object.entries(formData)) {
        if (value !== "") {
          url += `&${key}=${value}`;
        }
      }

      const response = await fetch(url);
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

  useEffect(() => {
    fetchCars();
  }, [page, searchQuery]);


  const handleEditClick = (car) => {
    setSelectedCar(car);
    setShowModal(true);
  };

  const handleDeleteClick = async (vin) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/cars/${vin}/`, {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error("Failed to delete the car.");
      }
      setCars((prevCars) => prevCars.filter((car) => car.vin !== vin));
    } catch (err) {
      alert(err.message);
    }
  };

  const handleModalClose = () => {
    setSelectedCar(null);
    setShowModal(false);
  };

  const handleSave = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/cars/${selectedCar.vin}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(selectedCar),
        }
      );
      if (!response.ok) {
        throw new Error("Failed to update the car.");
      }
      const updatedCar = await response.json();
      setCars((prevCars) =>
        prevCars.map((car) =>
          car.vin === updatedCar.vin ? updatedCar : car
        )
      );
      handleModalClose();
    } catch (err) {
      alert(err.message);
    }
  };


  // Search Bar
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setSearchQuery(e);
    setPage(1);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;


  return (
    <div className="container mx-auto px-5 py-8 text-indigo-950">
      <h1 className="text-4xl font-bold mb-6 text-center">Dealership Management</h1>

      {/* FORM */}
      <form
      onSubmit={handleSearch}
      className="grid grid-cols-1 md:grid-cols-4 gap-4 p-6 bg-gray-100 rounded shadow-lg"
    >
      {[
        "make",
        "model",
        "transmission",
        "drivewheel",
        "vin",
        "color",
        "status",
        "locationid",
      ].map((field) => (
        <div key={field} className="flex flex-col">
          <label className="text-sm font-semibold mb-1 capitalize">{field}</label>
          <input
            type="text"
            name={field}
            value={formData[field]}
            onChange={handleChange}
            className="p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
      ))}

      {[
        { name: "lower_year", label: "Lower Year" },
        { name: "higher_year", label: "Higher Year" },
        { name: "lower_numberofcylinders", label: "Lower Cylinders" },
        { name: "higher_numberofcylinders", label: "Higher Cylinders" },
        { name: "lower_price", label: "Lower Price" },
        { name: "higher_price", label: "Higher Price" },
        { name: "lower_mileage", label: "Lower Mileage" },
        { name: "higher_mileage", label: "Higher Mileage" },
        { name: "lower_rating", label: "Lower Rating" },
        { name: "higher_rating", label: "Higher Rating" },
      ].map((field) => (
        <div key={field.name} className="flex flex-col">
          <label className="text-sm font-semibold mb-1">{field.label}</label>
          <input
            type="number"
            name={field.name}
            value={formData[field.name]}
            onChange={handleChange}
            className="p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
      ))}

      <button
        type="submit"
        className="col-span-1 md:col-span-2 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        Search
      </button>
    </form>

      {/* DISPLAYED TABLE */}
      <div className="overflow-x-auto">
        <table className="min-w-full table-auto border-collapse border border-gray-300">
          <thead>
            <tr className="bg-indigo-100">
              {/* Table Headers */}
              <th className="border border-gray-300 px-4 py-2">VIN</th>
              <th className="border border-gray-300 px-4 py-2">Make</th>
              <th className="border border-gray-300 px-4 py-2">Model</th>
              <th className="border border-gray-300 px-4 py-2">Year</th>
              <th className="border border-gray-300 px-4 py-2">Color</th>
              <th className="border border-gray-300 px-4 py-2">Price</th>
              <th className="border border-gray-300 px-4 py-2">Mileage</th>
              <th className="border border-gray-300 px-4 py-2">Status</th>
              <th className="border border-gray-300 px-4 py-2">Location ID</th>
              <th className="border border-gray-300 px-4 py-2">Last Modified By</th>
              <th className="border border-gray-300 px-4 py-2">Warranty ID</th>
              <th className="border border-gray-300 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-slate-50">
            {cars.map((car) => (
              <tr key={car.vin} className="hover:bg-indigo-50 text-center">
                {/* Table Data */}
                <td className="text-sm border border-gray-300 px-4 py-2">{car.vin}</td>
                <td className="text-sm border border-gray-300 px-4 py-2">{car.make === null ? "-" : car.make}</td>
                <td className="text-sm border border-gray-300 px-4 py-2">{car.model === null ? "-" : car.model}</td>
                <td className="text-sm border border-gray-300 px-4 py-2">{car.year === null ? "-" : car.year}</td>
                <td className="text-sm border border-gray-300 px-4 py-2">{car.color === null ? "-" : car.color}</td>
                <td className="text-sm border border-gray-300 px-4 py-2">{car.price === null ? "-" : "$" + car.price}</td>
                <td className="text-sm border border-gray-300 px-4 py-2">{car.mileage === null ? "-" : car.mileage}</td>
                <td className="text-sm border border-gray-300 px-4 py-2">{car.status === null ? "-" : car.status}</td>
                <td className="text-sm border border-gray-300 px-4 py-2">{car.locationid === null ? "-" : car.locationid}</td>
                <td className="text-sm border border-gray-300 px-4 py-2">{car.lastmodifiedby === null ? "-" : car.lastmodifiedby}</td>
                <td className="text-sm border border-gray-300 px-4 py-2">{car.warrantyid === null ? "-" : car.warrantyid}</td>
                <td className="text-sm border border-gray-300 px-4 py-2 gap-2 justify-center">
                  <button
                    onClick={() => handleEditClick(car)}
                    className="bg-blue-500 text-white px-5 py-1 rounded"
                  >
                    Edit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex justify-center mt-4">
        <button
          // href={`?page=${Math.max(1, page - 1)}`}
          onClick={()=>setPage(Math.max(1, page - 1))}
          className={`${
            page <= 1 ? "pointer-events-none opacity-50" : ""
          } text-sm px-3 py-1 mx-1 border rounded bg-indigo-200 hover:bg-gray-300`}
        >
          &#8592;
        </button>
        <span className="text-sm font-bold px-3 py-1 mx-1">{page}</span>
        <button
          // href={`?page=${page + 1}`}
          onClick={()=>setPage(page + 1)}
          className="text-sm px-3 py-1 mx-1 border rounded bg-indigo-200 hover:bg-gray-300"
        >
          &#8594;
        </button>
      </div>

      {/* Modal for Editing */}
      {showModal && selectedCar && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white py-6 px-12 rounded shadow-md">
            <h2 className="text-lg font-bold mb-4 text-center">Edit Car</h2>
            <form className="grid grid-cols-2 gap-4">
              <label className="block mb-2">
                Make:
                <input
                  type="text"
                  value={selectedCar.make}
                  onChange={(e) =>
                    setSelectedCar({
                      ...selectedCar,
                      make: e.target.value === "" ? null : e.target.value,
                    })
                  }
                  className="border px-2 py-1 w-full"
                />
              </label>
              <label className="block mb-2">
                Model:
                <input
                  type="text"
                  value={selectedCar.model}
                  onChange={(e) =>
                    setSelectedCar({
                      ...selectedCar,
                      model: e.target.value === "" ? null : e.target.value,
                    })
                  }
                  className="border px-2 py-1 w-full"
                />
              </label>
              <label className="block mb-2">
                Year:
                <input
                  type="text"
                  value={selectedCar.year}
                  onChange={(e) =>
                    setSelectedCar({
                      ...selectedCar,
                      year: e.target.value === "" ? null : e.target.value,
                    })
                  }
                  className="border px-2 py-1 w-full"
                />
              </label>
              <label className="block mb-2">
                Color:
                <input
                  type="text"
                  value={selectedCar.color}
                  onChange={(e) =>
                    setSelectedCar({
                      ...selectedCar,
                      color: e.target.value === "" ? null : e.target.value,
                    })
                  }
                  className="border px-2 py-1 w-full"
                />
              </label>
              <label className="block mb-2">
                Price:
                <input
                  type="number"
                  value={selectedCar.price}
                  onChange={(e) =>
                    setSelectedCar({
                      ...selectedCar,
                      price: e.target.value === "" ? null : e.target.value,
                    })
                  }
                  className="border px-2 py-1 w-full"
                />
              </label>
              <label className="block mb-2">
                Mileage:
                <input
                  type="number"
                  value={selectedCar.mileage}
                  onChange={(e) =>
                    setSelectedCar({
                      ...selectedCar,
                      mileage: e.target.value === "" ? null : e.target.value,
                    })
                  }
                  className="border px-2 py-1 w-full"
                />
              </label>
              <label className="block mb-2">
                Status:
                <input
                  type="text"
                  value={selectedCar.status}
                  onChange={(e) =>
                    setSelectedCar({
                      ...selectedCar,
                      status: e.target.value === "" ? null : e.target.value,
                    })
                  }
                  className="border px-2 py-1 w-full"
                />
              </label>
              <label className="block mb-2">
                Location ID:
                <input
                  type="number"
                  value={selectedCar.locationid}
                  onChange={(e) =>
                    setSelectedCar({
                      ...selectedCar,
                      locationid: e.target.value === "" ? null : e.target.value,
                    })
                  }
                  className="border px-2 py-1 w-full"
                />
              </label>
              <label className="block mb-2">
                Warranty ID:
                <input
                  type="number"
                  value={selectedCar.warrantyid}
                  onChange={(e) =>
                    setSelectedCar({
                      ...selectedCar,
                      warrantyid: e.target.value === "" ? null : e.target.value,
                    })
                  }
                  className="border px-2 py-1 w-full"
                />
              </label>
            </form>
            <div className="mt-4 flex justify-end gap-2">
              <button
                onClick={() => handleDeleteClick(car.vin)}
                className="bg-red-500 text-white px-2 py-1 rounded mr-auto"
              >
                Delete
              </button>
              <button
                onClick={handleModalClose}
                className="bg-gray-500 text-white px-3 py-1 rounded"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="bg-green-500 text-white px-3 py-1 rounded"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
