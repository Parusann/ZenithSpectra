"use client";

import { useEffect, useRef } from "react";

interface Orb {
  x: number;
  y: number;
  radius: number;
  vx: number;
  vy: number;
  color: string;
  opacity: number;
  pulseSpeed: number;
  pulsePhase: number;
}

export default function AmbientOrbs() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rafRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    function resize() {
      canvas!.width = window.innerWidth;
      canvas!.height = window.innerHeight;
    }

    resize();

    const orbs: Orb[] = [
      // Gold orbs
      { x: 0.7, y: 0.2, radius: 300, vx: 0.15, vy: 0.08, color: "212, 168, 67", opacity: 0.04, pulseSpeed: 0.0008, pulsePhase: 0 },
      { x: 0.2, y: 0.7, radius: 250, vx: -0.1, vy: 0.12, color: "212, 168, 67", opacity: 0.03, pulseSpeed: 0.001, pulsePhase: 2 },
      // Blue orbs
      { x: 0.3, y: 0.3, radius: 350, vx: 0.08, vy: -0.1, color: "74, 144, 217", opacity: 0.05, pulseSpeed: 0.0006, pulsePhase: 1 },
      { x: 0.8, y: 0.8, radius: 280, vx: -0.12, vy: -0.06, color: "56, 189, 248", opacity: 0.03, pulseSpeed: 0.0012, pulsePhase: 3 },
      // Deep purple accent
      { x: 0.5, y: 0.1, radius: 200, vx: 0.05, vy: 0.15, color: "139, 92, 246", opacity: 0.025, pulseSpeed: 0.0009, pulsePhase: 1.5 },
    ].map(o => ({
      ...o,
      x: o.x * window.innerWidth,
      y: o.y * window.innerHeight,
    }));

    let time = 0;

    function draw() {
      const w = canvas!.width;
      const h = canvas!.height;
      ctx!.clearRect(0, 0, w, h);
      time++;

      for (const orb of orbs) {
        // Drift movement
        orb.x += orb.vx;
        orb.y += orb.vy;

        // Soft bounce off edges
        if (orb.x < -orb.radius) orb.x = w + orb.radius;
        if (orb.x > w + orb.radius) orb.x = -orb.radius;
        if (orb.y < -orb.radius) orb.y = h + orb.radius;
        if (orb.y > h + orb.radius) orb.y = -orb.radius;

        // Pulse opacity
        const pulse = Math.sin(time * orb.pulseSpeed + orb.pulsePhase) * 0.5 + 0.5;
        const alpha = orb.opacity * (0.6 + pulse * 0.4);

        // Draw radial gradient orb
        const grad = ctx!.createRadialGradient(orb.x, orb.y, 0, orb.x, orb.y, orb.radius);
        grad.addColorStop(0, `rgba(${orb.color}, ${alpha})`);
        grad.addColorStop(0.4, `rgba(${orb.color}, ${alpha * 0.5})`);
        grad.addColorStop(1, `rgba(${orb.color}, 0)`);

        ctx!.fillStyle = grad;
        ctx!.fillRect(orb.x - orb.radius, orb.y - orb.radius, orb.radius * 2, orb.radius * 2);
      }

      rafRef.current = requestAnimationFrame(draw);
    }

    window.addEventListener("resize", resize);
    rafRef.current = requestAnimationFrame(draw);

    return () => {
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(rafRef.current);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 z-0 pointer-events-none"
      aria-hidden="true"
    />
  );
}
