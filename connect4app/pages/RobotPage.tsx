
import React from 'react';
import Image from 'next/image'
import Head from 'next/head'
import { Inter } from 'next/font/google'
import {useEffect, useState } from 'react';
const inter = Inter({ subsets: ['latin'] })
import { BsFillMoonStarsFill } from "react-icons/bs";
import { FaArrowLeft } from 'react-icons/fa';
import Link from 'next/link';
import Board2 from './Board2';
import io from 'socket.io-client';

const RobotPage: React.FC = () => {
  const [darkMode, setDarkMode]= useState(false);

  const [socket, setSocket] = useState<any>(null); // State to hold the socket

  // Establish a connection to the server
  useEffect(() => {
    const newSocket = io('http://localhost:8080');
    setSocket(newSocket);
    return () => newSocket.close();
  }, []);

  // Function to handle link click and emit a message to the server
  const handleLinkClick = () => {
    if (socket) {
      // Emit a message to the server upon link click
      socket.emit('refreshServer');
    }
  };
  return (
    <div className={darkMode ? "dark" : ""}>
      
    <Head>
      <title>COnnect Four Game</title>
      <meta name="description" content="Generated by create next app" />
      <link rel="icon" href="/favicon.ico" />
    </Head>




    <main className={  'bg-orange-400 px-10 md:px-20 lg:pc-40 dark:bg-gray-950 '} >
    <section className=" min-h-screen">
        <nav className=' py-10 mb-12 flex justify-between'>
          <h1 className=' text-xl  dark:text-white'>Connect Four Game</h1>
          <ul className='flex items-center'>
            <li>
            <BsFillMoonStarsFill onClick={() => setDarkMode(!darkMode)} className=' cursor-pointer text-2xl'/>
            </li>
            <li>
            <Link href="/">
          <div className="flex items-center ml-8"onClick={handleLinkClick}>
            <FaArrowLeft className="mr-2" /> 
          </div>
            </Link>
            </li>
          </ul>
        </nav>




      <section className="flex justify-center items-center ">
        
        <Board2 />
      </section>

    </section>
    </main>
    </div>
  );
};

export default RobotPage;
