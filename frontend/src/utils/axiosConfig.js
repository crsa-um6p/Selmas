import axios from 'axios';
// import jwt_decode from 'jwt-decode';

const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000', // Base API URL with fallback
    headers: {
        'Content-Type': 'application/json',
        // 'Access-Control-Allow-Origin': '*',
    },
});





// Add Axios interceptor for handling token refresh
axiosInstance.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true; 
            const refreshToken = localStorage.getItem('refresh');
            
            if (refreshToken) {
                try {
                    const res = await axios.post(`${process.env.REACT_APP_PLATFORM_HOST}:${process.env.REACT_APP_BACKEND_PORT}/auth/api/token/refresh/`, { refresh: refreshToken });
                    localStorage.setItem('access', res.data.access);
                    axiosInstance.defaults.headers['Authorization'] = `Bearer ${res.data.access}`;
                    originalRequest.headers['Authorization'] = `Bearer ${res.data.access}`;
                    return axiosInstance(originalRequest); 
                } catch (refreshError) {
                    localStorage.removeItem('access');
                    localStorage.removeItem('refresh');
                    window.location.href = '/'; 
                }
            } else {
                console.error('No refresh token available.');
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;
