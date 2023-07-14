'use client'
// pages/index.js

import { useState, useEffect } from 'react';
import axios from 'axios';
import './globals.css';


export default function Home() {

//  const [message, setMessage] = useState('');

//useEffect(() => {
//    async function fetchData() {
//      const response = await axios.get('http://localhost:5328/api/hello');
//      setMessage(response.data); 
//    }
//    fetchData();
//  }, []);

return (
  <div className="p-4 max-w-md mx-auto bg-indigo-200 rounded-lg shadow-md">
    <h1 className="text-lg font-medium text-gray-700">Hello Tailwindcss</h1>
  </div>
);
}