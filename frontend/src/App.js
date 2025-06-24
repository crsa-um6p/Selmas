import logo from './logo.svg';
import './App.css';
import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import Dashboard from './Components/Dashboard';
import NavBar from './utils/NavBar';
import Footer from './utils/Footer';

// Layout component that includes NavBar and Footer
const Layout = () => {
  return (
    <div>
      <NavBar />
      <Outlet />
      <Footer />
    </div>
  );
};

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <Dashboard />,
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
