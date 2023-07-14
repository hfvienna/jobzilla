'use client'
// pages/index.js

import { useState, useEffect } from 'react';
import axios from 'axios';
import './globals.css';
import 'daisyui/dist/full.css';



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
  <div className="card bg-base-200 shadow-xl">
    <div className="card-body">
      <h2 className="card-title">Hello DaisyUI!</h2> 
      <p>Let's add some Daisy styling!</p>

      <div className="btn-group">
        <button className="btn">Button 1</button>
        <button className="btn btn-outline">Button 2</button>
      </div>
    </div>
  </div>
);
}