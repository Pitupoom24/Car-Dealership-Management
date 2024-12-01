"use client"; // Ensure it's a Client Component

import { useState, useEffect } from "react";

export default function LoginPage() {

  const [employeeID, setEmployeeID] = useState(""); // State for employee ID
  const [password, setPassword] = useState(""); // State for password
  const [errorMessage, setErrorMessage] = useState(""); // State for any error messages
  const [isLoggedIn, setIsLoggedIn] = useState(false); // State to track login status
  const [verifiedEmployeeID, setVerifiedEmployeeID] = useState(null)

    useEffect(() => {
    setIsLoggedIn(false);
  }, []);



  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    const url = `http://127.0.0.1:8000/api/users/login/?employeeid=${employeeID}&password=${password}`;

    try {
      const response = await fetch(url, {
        method: "GET",
      });

      if (response.ok) {
        const data = await response.json();



        if (data.is_valid === 1) {



        sessionStorage.setItem('current_employee_id', data.employeeid);
        sessionStorage.setItem('is_currently_logged_in', true);
        window.location.href = '/';



             

   


        } else {
          setErrorMessage("Invalid credentials, please try again.");
        }



      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Login failed.");
      }
    } catch (error) {
      setErrorMessage("An error occurred. Please try again.");
      console.error("Error during login:", error);
    }
  };


  return (
    <div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm">
        <img
          className="mx-auto h-10 w-auto"
          src="https://tailwindui.com/plus/img/logos/mark.svg?color=indigo&shade=600"
          alt="Your Company"
        />
        <h2 className="mt-10 text-center text-2xl font-bold tracking-tight text-gray-900">
          Sign in to your account
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form className="space-y-6" onSubmit={handleSubmit}>
          <div>
            <label
              htmlFor="employee_id"
              className="block text-sm font-medium text-gray-900"
            >
              Employee ID
            </label>
            <div className="mt-2">
              <input
                type="text"
                name="employee_id"
                id="employee_id"
                value={employeeID}
                onChange={(e) => setEmployeeID(e.target.value)} // Update employee ID state
                autoComplete="employee_id"
                required
                className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm"
              />
            </div>
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-900"
            >
              Password
            </label>
            <div className="mt-2">
              <input
                type="password"
                name="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)} // Update password state
                autoComplete="current-password"
                required
                className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm"
              />
            </div>
          </div>

          {errorMessage && (
            <div className="text-red-600 text-sm mt-2">{errorMessage}</div>
          )}

          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Sign in
            </button>
          </div>
        </form>

        <p className="mt-10 text-center text-sm text-gray-500">
          New to this website?{" "}
          <a
            href="#"
            className="font-semibold text-indigo-600 hover:text-indigo-500"
          >
            Sign up
          </a>
        </p>
      </div>
    </div>
  );
}
