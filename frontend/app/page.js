"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

export default function CarsPage() {
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCar, setSelectedCar] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [showAddModal, setShowAddModal] = useState(false);
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
  const [createData, setCreateData] = useState({
    vin: "",
    make: "",
    model: "",
    year: "",
    color: "",
    price: "",
    mileage: "",
    status: "",
    locationid: "",
    warrantyid: "",
  });

  const [currentEmployeeID, setCurrentEmployeeID] = useState(null);
  const [isCurrentlyLoggedIn, setIsCurrentlyLoggedIn] = useState(false);

  useEffect(() => {
    setCurrentEmployeeID(sessionStorage.getItem("current_employee_id"));
    setIsCurrentlyLoggedIn(sessionStorage.getItem("is_currently_logged_in"));
  }, [
    sessionStorage.getItem("current_employee_id"),
    sessionStorage.getItem("is_currently_logged_in"),
  ]);

  // Get `page` parameter from URL manually
  const [page, setPage] = useState(1);
  const limit = 10;

  const fetchCars = async () => {
    try {
      setLoading(true);

      var url = `http://127.0.0.1:8000/api/advanced_queries/?limit=${limit}&offset=${
        (page - 1) * limit
      }`;

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

    setSelectedCar({
      ...car,
      lastmodifiedby: currentEmployeeID,
    });

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
      setShowModal(false);
    } catch (err) {
      alert(err.message);
    }
  };

  // Edit Modal
  const handleModalClose = () => {
    setSelectedCar(null);
    setShowModal(false);
  };

  // Save Button in Edit Modal
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
        prevCars.map((car) => (car.vin === updatedCar.vin ? updatedCar : car))
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

  const handleAddForm = async () => {
    if (
      createData.vin == "" ||
      createData.make == "" ||
      createData.model == "" ||
      createData.year == ""
    ) {
      alert("Please fill in all required fields: VIN, Make, Model, and Year.");
      return;
    }

    const dataToSubmit_create = {
      ...createData,
      lastmodifiedby: currentEmployeeID, // Add the employee ID
    };

    if (dataToSubmit_create.warrantyid == ""){
      dataToSubmit_create.warrantyid = null;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/api/cars/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToSubmit_create),
      });
      if (!response.ok) {
        throw new Error("Failed to create a new car.");
      }
      const createdCar = await response.json();
      setCars((prevCars) => [...prevCars, createdCar]);
      setShowAddModal(false);
      setCreateData({
        vin: "",
        make: "",
        model: "",
        year: "",
        color: "",
        price: "",
        mileage: "",
        status: "",
        locationid: "",
        warrantyid: "",
      });
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="container mx-auto px-5 py-8 text-indigo-950">
      {/* Logged in already */}
      {isCurrentlyLoggedIn && (
        <div className="flex flex-col items-end space-y-2">
          <Link
            className="px-6 py-2 text-white bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg shadow-lg transform transition hover:scale-105 hover:shadow-2xl"
            href="/login"
          >
            Log Out
          </Link>
          <h1 className="text-md font-semibold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-500">
            <span className="text-gray-600 text-sm font-normal">
              Your Employee ID:{" "}
            </span>
            {currentEmployeeID}
          </h1>
        </div>
      )}

      {/* Not Logged in yet */}
      {!isCurrentlyLoggedIn && (
        <div className="flex flex-col items-end space-y-2">
          <Link
            className="px-6 py-2 text-white bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg shadow-lg transform transition hover:scale-105 hover:shadow-2xl"
            href="/login"
          >
            Sign In
          </Link>
        </div>
      )}

      {/* Head */}
      <h1 className="text-4xl font-bold mb-6 text-center bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
        Dealership Management
      </h1>

      {/* FORM */}
      <form
        onSubmit={(e) => handleSearch(e)}
        className="grid grid-cols-1 md:grid-cols-4 gap-4 p-6 bg-gray-100 rounded shadow-lg"
      >
        {/* Input fields */}
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
            <label className="text-sm font-semibold mb-1 capitalize">
              {field}
            </label>
            <input
              type="text"
              name={field}
              value={formData[field]}
              onChange={handleChange}
              className="p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>
        ))}

        {/* Number inputs */}
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

        {/* Other buttons */}
        <div className="col-span-1 md:col-span-1 flex flex-wrap justify-evenly items-center">
          <button
            type="button" // Prevents form submission
            onClick={() => setShowAddModal(true)}
            className="text-xs bg-gradient-to-r from-blue-500 to-purple-400 text-white py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 w-[45%]"
          >
            Add New Car
          </button>

          <button
            type="button" // Prevents form submission
            className="text-xs bg-gradient-to-r from-blue-500 to-purple-400 text-white py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 w-[45%]"
          >
            Top of List
          </button>

          <button
            type="button" // Prevents form submission
            className="text-xs bg-gradient-to-r from-blue-500 to-purple-400 text-white py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 w-[45%]"
          >
            Adjust Prices
          </button>

          <button
            type="button" // Prevents form submission
            className="text-xs bg-gradient-to-r from-blue-500 to-purple-400 text-white py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 w-[45%]"
          >
            Advanced Search
          </button>
        </div>

        {/* Submit button */}
        <button
          type="submit" // This triggers the onSubmit handler
          className="col-span-1 md:col-span-1 bg-gradient-to-r from-blue-500 to-purple-400 text-white py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
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
              <th className="border border-gray-300 px-4 py-2">
                Last Modified By
              </th>
              <th className="border border-gray-300 px-4 py-2">Warranty ID</th>
              <th className="border border-gray-300 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-slate-50">
            {cars.map((car) => (
              <tr key={car.vin} className="hover:bg-indigo-50 text-center">
                {/* Table Data */}
                <td className="text-sm text-center bg-gradient-to-r from-black to-black bg-clip-text text-transparent border border-gray-300 px-4 py-2 hover:from-purple-400 hover:to-blue-600">
                  <Link
                    href={{
                      pathname: "/details",
                      query: {
                        make: car.make,
                        model: car.model,
                        year: car.year,
                      },
                    }}
                  >
                    {car.vin}
                  </Link>
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.make === null ? "-" : car.make}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.model === null ? "-" : car.model}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.year === null ? "-" : car.year}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.color === null ? "-" : car.color}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.price === null ? "-" : "$" + car.price}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.mileage === null ? "-" : car.mileage}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.status === null ? "-" : car.status}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.locationid === null ? "-" : car.locationid}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.lastmodifiedby === null ? "-" : car.lastmodifiedby}
                </td>
                <td className="text-sm border border-gray-300 px-4 py-2">
                  {car.warrantyid === null ? "-" : car.warrantyid}
                </td>
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
          onClick={() => setPage(Math.max(1, page - 1))}
          className={`${
            page <= 1 ? "pointer-events-none opacity-50" : ""
          } text-sm px-3 py-1 mx-1 border rounded bg-indigo-200 hover:bg-gray-300`}
        >
          &#8592;
        </button>
        <span className="text-sm font-bold px-3 py-1 mx-1">{page}</span>
        <button
          onClick={() => setPage(page + 1)}
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
              {[
                { label: "Make", key: "make", type: "text" },
                { label: "Model", key: "model", type: "text" },
                { label: "Year", key: "year", type: "text" },
                { label: "Color", key: "color", type: "text" },
                { label: "Price", key: "price", type: "number" },
                { label: "Mileage", key: "mileage", type: "number" },
                { label: "Status", key: "status", type: "text" },
                { label: "Location ID", key: "locationid", type: "number" },
                { label: "Warranty ID", key: "warrantyid", type: "number" },
              ].map((field) => (
                <label key={field.key} className="block mb-2">
                  {field.label}:
                  <input
                    type={field.type}
                    value={selectedCar[field.key] || ""}
                    onChange={(e) =>
                      setSelectedCar({
                        ...selectedCar,
                        [field.key]:
                          e.target.value === "" ? null : e.target.value,
                      })
                    }
                    className="border px-2 py-1 w-full"
                  />
                </label>
              ))}
            </form>
            <div className="mt-4 flex justify-end gap-2">
              <button
                onClick={() => handleDeleteClick(selectedCar.vin)}
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

      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white py-6 px-12 rounded shadow-md">
            <h2 className="text-lg font-bold mb-4 text-center">
              Create New Car
            </h2>
            <form className="grid grid-cols-2 gap-4">
              {[
                { label: "VIN", name: "vin" },
                { label: "Make", name: "make" },
                { label: "Model", name: "model" },
                { label: "Year", name: "year" },
                { label: "Color", name: "color" },
                { label: "Price", name: "price" },
                { label: "Mileage", name: "mileage" },
                { label: "Status", name: "status" },
                { label: "Location ID", name: "locationid" },
                { label: "Warranty ID", name: "warrantyid" },
              ].map((field) => (
                <label key={field.name} className="block mb-2">
                  {field.label}:
                  <input
                    type="text"
                    name={field.name}
                    value={createData[field.name]}
                    onChange={(e) =>
                      setCreateData({ ...createData, [field.name]: e.target.value })
                    }
                    className="border px-2 py-1 w-full"
                  />
                </label>
              ))}
            </form>
            <div className="mt-4 flex justify-end gap-2">
              <button
                onClick={() => setShowAddModal(false)}
                className="bg-gray-500 text-white px-3 py-1 rounded"
              >
                Cancel
              </button>
              <button
                onClick={handleAddForm}
                className="bg-green-500 text-white px-3 py-1 rounded"
              >
                Add
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
