// app/page.js

'use client'

import { useState, useEffect } from 'react';
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
  <div>
      <Link href="/ranking">Go to Ranking</Link>
  </div>
);
}