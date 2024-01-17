import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const Board = () => {
    const [board, setBoard] = useState(Array.from({ length: 6 }, () => Array(7).fill('bg-gray-400')));
    const [currentPlayer, setCurrentPlayer] = useState(1);
    const [winner, setWinner] = useState(null); // New state to track the winner
    const socket = io('http://localhost:8080'); // Change the URL/port to match your server


    useEffect(() => {
        socket.on('etat', (status) => {
            switch (status) {
                case 'win1':
                    console.log('Player 1 wins!');
                    setWinner(1); // Set the winner to Player 1
                    break;
                case 'win2':
                    console.log('Player 2 wins!');
                    setWinner(2); // Set the winner to Player 2
                    break;
                case 'draw':
                    console.log('DRAW');
                    setWinner('draw'); // Set the winner to draw
                    break;
            }
        });
    }, []);

    useEffect(() => {
        const handlePlayer1Move = (position) => {
            const { col } = position;
            const updatedBoard = [...board];
            for (let row = board.length - 1; row >= 0; row--) {
                if (updatedBoard[row][col] === 'bg-gray-400') {
                    updatedBoard[row][col] = 'bg-red-500'; // Player 2 color is blue
                    break;
                }
            }
            setBoard(updatedBoard);
            setCurrentPlayer(1); // Switch to Player 1
             
        };

        socket.on('player1Move', handlePlayer1Move);

        return () => {
            // Clean up the event listener on unmount
            socket.off('player1Move', handlePlayer1Move);
        };
    }, [board]);
    





    useEffect(() => {
        const handlePlayer2Move = (position) => {
            const { col } = position;
            const updatedBoard = [...board];
            for (let row = board.length - 1; row >= 0; row--) {
                if (updatedBoard[row][col] === 'bg-gray-400') {
                    updatedBoard[row][col] = 'bg-blue-500'; // Player 2 color is blue
                    break;
                }
            }
            setBoard(updatedBoard);
            setCurrentPlayer(1); // Switch to Player 1
            
        };

        socket.on('player2Move', handlePlayer2Move);
        

        return () => {
            // Clean up the event listener on unmount
            socket.off('player2Move', handlePlayer2Move);
        };
    }, [board]);
    

    return (
        <section className="flex justify-center items-center">
            {winner === null && (
                <p>{`Current Player: ${currentPlayer}`}</p>
            )}
            {winner !== null && (
                <p>{winner === 'draw' ? 'It\'s a draw!' : `Player ${winner} wins!`}</p>
            )}
            <table className="border-collapse">
                {board.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                        {row.map((cell, colIndex) => (
                            <td
                                key={`${rowIndex}-${colIndex}`}
                                className={`w-24 h-24 rounded-full ${cell}`}
                            >
                                <button type="button"></button>
                            </td>
                        ))}
                    </tr>
                ))}
            </table>
        </section>
    );
};

export default Board;
