// Import images at the top of your file
import Image from 'next/image';
import Head from 'next/head';
import { Inter } from 'next/font/google';
import { useEffect, useState } from 'react';
import { BsFillMoonStarsFill } from 'react-icons/bs';
import computerImage from '../public/computer.png';
import humainImage from '../public/humain.png';
import Link from 'next/link';
import io from 'socket.io-client';

const inter = Inter({ subsets: ['latin'] });

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const [socket, setSocket] = useState<any>(null);

  useEffect(() => {
    const newSocket = io('http://localhost:8080');
    setSocket(newSocket);
    return () => newSocket.close();
  }, []);
  const startComputerVsMonteCarlo = () => {
    if (socket) {
    socket.emit('startComputerVsMonteCarlo');
  }
  };

  return (
    <div className={darkMode ? 'dark' : ''}>
      <Head>
        <title>Connect Four Game</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="bg-orange-400 px-10 md:px-20 lg:pc-40 dark:bg-gray-950">
        <section className="min-h-screen">
          <nav className="py-10 mb-12 flex justify-between">
            <h1 className="text-xl dark:text-white">Connect Four Game</h1>
            <ul className="flex items-center">
              <li>
                <BsFillMoonStarsFill
                  onClick={() => setDarkMode(!darkMode)}
                  className="cursor-pointer text-2xl"
                />
              </li>
            </ul>
          </nav>

          <div className="text-center">
            <p className="text-5xl dark:text-white text-center">CHOOSE YOUR ENEMY</p>

            <div className="flex justify-center mt-10 text-3xl text-center">
              <div className="flex flex-col items-center">
                <Link href="/HumainPage">
                  <div className="flex items-center mb-10 cursor-pointer">
                    <div className="mx-auto bg-gradient-to-b from-orange-600 rounded-full w-30 h-30 relative overflow-hidden">
                      <Image src={humainImage} width={200} height={200} alt="Humain Image" />
                    </div>
                    <p className="mr-2 ml-20">Humain</p>
                  </div>
                </Link>
                <Link href="/RobotPage">
                  <div className="flex items-center cursor-pointer" onClick={startComputerVsMonteCarlo}>
                    <div className="mx-auto bg-gradient-to-b from-blue-500 rounded-full w-30 h-30 relative overflow-hidden " >
                      <Image src={computerImage} width={200} height={200} alt="Computer Image" />
                    </div>
                    <p className="mr-2 ml-20">Robot</p>
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
