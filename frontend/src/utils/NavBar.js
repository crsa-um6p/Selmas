import React, { useState, useEffect }  from "react";
import { Disclosure } from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
// import logo from "../assets/MorSnow.ico";
import { Link } from "react-router-dom";
import axiosInstance from "./axiosConfig";



function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}



export const getUserData = async (token) => {

  try {
    const response = await axiosInstance.get(`${process.env.REACT_APP_PLATFORM_HOST}:${process.env.REACT_APP_BACKEND_PORT}/auth/user-data/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching user data:', error);
    return null;  
  }
};

export default function Navbar(props) {

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userName, setUserName] = useState("");
  const [usertype, setUsertype] = useState(null);
  const token = localStorage.getItem('access');
  

  const navigation = [
    { name: `Dashboard`, to: "/", tab:"dashboard", current: false },
    { name: `visualization`, to: "/visualisation", tab:"visualization", current: false },
    { name: `modeling`, to: "/modeling", tab:"modeling", current: false },
  ];


  // useEffect(() => {
  //   if (token) {
  //     const fetchUserData = async () => {
  //       const userData = await getUserData(token);
  //       if(userData){
  //         setUserName(userData.first_name + ' ' + userData.last_name);
  //         setIsAuthenticated(true)
  //         setUsertype(userData.user_type)
  //       }
  //     };
  //     fetchUserData();
  //   }
  // }, [token]);




  return (
    <Disclosure as="nav" className="bg-white h-[8vh] z-50">
      {({ open }) => (
        <>
          <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 h-full">
            <div className="relative flex items-center justify-between h-full ">
              <div className="absolute inset-y-0 left-0 flex items-center md:hidden ">
                {/* Mobile menu button */}
                <Disclosure.Button className="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                  <span className="sr-only">Open main menu</span>
                  {open ? (
                    <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                  ) : (
                    <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                  )}
                </Disclosure.Button>
              </div>
            </div>
          </div>

          <Disclosure.Panel className="md:hidden z-40 absolute w-full">
            <div className="bg-white space-y-1 px-2 pb-3 pt-2 ">
              <div className="flex items-center justify-center">
                {/* <img src={logo} alt="logo" className="w-10 h-10" /> */}
                <h1 className="text-2xl font-bold">Selmas</h1>
              </div>
            {navigation.map((item, index) => (
                          <Link key={index} to={item.to}>
                            <Disclosure.Button
                              className={classNames(
                                item.current ? "bg-gray-900 text-white" : "text-navtext hover:bg-gray-700 hover:text-white",
                                "block rounded-md px-3 py-2 text-base font-nunito"
                              )}
                              aria-current={item.current ? "page" : undefined}
                            >
                              {item.name}
                            </Disclosure.Button>
                          </Link>
                        ))}
              
            </div>
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  );
}


