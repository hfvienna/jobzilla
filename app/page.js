// app/page.js

'use client'

import { useState, useEffect } from 'react';
import axios from 'axios';
import './globals.css';
import 'daisyui/dist/full.css';
import Link from 'next/link';




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
      <p>Lets add some Daisy styling!</p>
      <div className="btn-group">
        <button className="btn">Button 1</button>
        <button className="btn btn-outline">Button 2</button>
      </div>
      <Link href="/ranking">Go to Ranking</Link>
    </div>
  </div>
);
}