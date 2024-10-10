"use client";

import { Canvas, useFrame, useLoader } from "@react-three/fiber";
import { TextureLoader, SphereGeometry } from "three";
import { OrthographicCamera, Stars, useSphere } from "@react-three/drei";
import { useEffect, useRef, useState } from "react";

function Earth() {
  const texture = useLoader(TextureLoader, "/1.jpg");
  const earthRef = useRef();

  useFrame(() => {
    if (earthRef.current) {
      earthRef.current.rotation.y += 0.003;
    }
  });

  return (
    <mesh ref={earthRef} position={[350, 150, 0]}>
      <sphereGeometry args={[15, 32, 16]} />
      <meshStandardMaterial map={texture} />
    </mesh>
  );
}

function Asteroids({ position, size }) {
  const texture = useLoader(TextureLoader, "/as.jpg");
  const asteroidRef = useRef();

  const radius = size || 15;
  const widthSegments = 4;
  const heightSegments = 4;

  const rotationSpeed = {
    x: Math.random() * 0.03,
    y: Math.random() * 0.01,
    z: Math.random() * 0.02,
  };

  useEffect(() => {
    if (asteroidRef.current) {
      const geometry = new SphereGeometry(
        radius,
        widthSegments,
        heightSegments
      );
      asteroidRef.current.geometry = geometry;
    }
  }, [radius, widthSegments, heightSegments]);

  useFrame(() => {
    if (asteroidRef.current) {
      asteroidRef.current.rotation.x += rotationSpeed.x;
      asteroidRef.current.rotation.y += rotationSpeed.y;
      asteroidRef.current.rotation.z += rotationSpeed.z;
    }
  });

  return (
    <mesh ref={asteroidRef} position={position}>
      <meshStandardMaterial map={texture} />
    </mesh>
  );
}

export default function Universe() {
  const [inputValue, setInputValue] = useState("");
  const [asteroids, setAsteroids] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:5550/asteroid", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ count: inputValue }),
      });

      const data = await response.json();
      console.log("Response:", data);

      if (Array.isArray(data) && data[0] && Array.isArray(data[0])) {
        setAsteroids(data[0]);
      } else {
        console.error("Format de données inattendu :", data);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      <form
        onSubmit={handleSubmit}
        style={{ position: "absolute", top: "20px", left: "20px", zIndex: 1 }}
      >
        <input
          type="text"
          name="count"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Nombre d'astéroides"
          style={{ padding: "5px", fontSize: "16px", color: "black" }}
        />
        <button type="submit" style={{ padding: "5px 10px", fontSize: "16px" }}>
          OK
        </button>
      </form>

      <Canvas>
        <OrthographicCamera makeDefault position={[350, 150, 100]} zoom={2} />

        <Stars
          radius={800}
          depth={30}
          count={500000}
          factor={4}
          saturation={0}
          fade={true}
        />

        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} intensity={1} />

        <Earth />

        {asteroids.map((asteroid) => (
          <Asteroids
            key={asteroid.asteroid_id}
            position={[
              asteroid.position.x * 0.0007,
              asteroid.position.y * 0.0003,
              asteroid.position.z * 0.0001,
            ]}
            size={asteroid.size * 0.01}
          />
        ))}
      </Canvas>
    </div>
  );
}
