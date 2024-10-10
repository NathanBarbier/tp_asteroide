'use client';

import { Canvas, useFrame, useLoader } from '@react-three/fiber';
import { TextureLoader } from 'three';
import { OrthographicCamera, Stars } from '@react-three/drei';
import { useRef, useState } from 'react';

function Earth() {
  const texture = useLoader(TextureLoader, '/1.jpg');
  const earthRef = useRef();

  useFrame(() => {
    if (earthRef.current) {
      earthRef.current.rotation.y += 0.001;
    }
  });

  return (
    <mesh ref={earthRef} position={[0, 0, 0]}>
      <sphereGeometry args={[15, 32, 16]} />
      <meshStandardMaterial map={texture} />
    </mesh>
  );
}

function Asteroids() {
  return (
    <mesh position={[-100, 10, 0]}>
      <sphereGeometry args={[5, 32, 16]} />
      <meshStandardMaterial color="lightblue" />
    </mesh>
  );
}

export default function Universe() {
  const [inputValue, setInputValue] = useState('');

  // Fonction pour gérer la soumission du formulaire
  const handleSubmit = async (e) => {
    e.preventDefault(); // Empêche le rechargement de la page

    try {
      const response = await fetch('http://localhost:5550/asteroid', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: inputValue }),
      });

      const data = await response.json();
      console.log('Response:', data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div style={{ height: '100vh', width: '100vw' }}>
      <form onSubmit={handleSubmit} style={{ position: 'absolute', top: '20px', left: '20px', zIndex: 1 }}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Nombre d'astéroides"
          style={{ padding: '5px', fontSize: '16px', color: 'black' }}
        />
        <button type="submit" style={{ padding: '5px 10px', fontSize: '16px' }}>OK</button>
      </form>

      <Canvas>
        <OrthographicCamera makeDefault position={[0, 0, 100]} zoom={2} />

        <Stars 
          radius={500}  
          depth={30}    
          count={500000}  
          factor={4}    
          saturation={0}  
          fade={true}    
        />

        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} intensity={1} />

        <Asteroids />
        <Earth />
      </Canvas>
    </div>
  );
}
