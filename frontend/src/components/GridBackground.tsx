"use client";

import { useEffect, useRef } from "react";

export default function GridBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mouseRef = useRef({ x: -1000, y: -1000 });
  const rafRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    function resize() {
      canvas!.width = window.innerWidth;
      canvas!.height = window.innerHeight;
    }

    function draw() {
      const w = canvas!.width;
      const h = canvas!.height;
      const spacing = 60;
      const radius = 250;
      const mx = mouseRef.current.x;
      const my = mouseRef.current.y;

      ctx!.clearRect(0, 0, w, h);

      // Vertical lines
      for (let x = 0; x <= w; x += spacing) {
        ctx!.beginPath();
        ctx!.moveTo(x, 0);
        ctx!.lineTo(x, h);
        const dist = Math.abs(x - mx);
        const intensity = Math.max(0, 1 - dist / radius);
        ctx!.strokeStyle = `rgba(212, 168, 67, ${0.03 + intensity * 0.15})`;
        ctx!.lineWidth = intensity > 0.1 ? 1 : 0.5;
        ctx!.stroke();
      }

      // Horizontal lines
      for (let y = 0; y <= h; y += spacing) {
        ctx!.beginPath();
        ctx!.moveTo(0, y);
        ctx!.lineTo(w, y);
        const dist = Math.abs(y - my);
        const intensity = Math.max(0, 1 - dist / radius);
        ctx!.strokeStyle = `rgba(212, 168, 67, ${0.03 + intensity * 0.15})`;
        ctx!.lineWidth = intensity > 0.1 ? 1 : 0.5;
        ctx!.stroke();
      }

      // Intersection glow dots
      for (let x = 0; x <= w; x += spacing) {
        for (let y = 0; y <= h; y += spacing) {
          const dx = x - mx;
          const dy = y - my;
          const dist = Math.sqrt(dx * dx + dy * dy);
          const intensity = Math.max(0, 1 - dist / radius);

          if (intensity > 0.05) {
            ctx!.beginPath();
            ctx!.arc(x, y, 1.5 + intensity * 3, 0, Math.PI * 2);
            ctx!.fillStyle = `rgba(212, 168, 67, ${intensity * 0.6})`;
            ctx!.fill();

            if (intensity > 0.3) {
              ctx!.beginPath();
              ctx!.arc(x, y, 4 + intensity * 8, 0, Math.PI * 2);
              ctx!.fillStyle = `rgba(212, 168, 67, ${intensity * 0.08})`;
              ctx!.fill();
            }
          }
        }
      }

      rafRef.current = requestAnimationFrame(draw);
    }

    function onMouseMove(e: MouseEvent) {
      mouseRef.current = { x: e.clientX, y: e.clientY };
    }

    function onMouseLeave() {
      mouseRef.current = { x: -1000, y: -1000 };
    }

    window.addEventListener("resize", resize);
    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseleave", onMouseLeave);
    resize();
    rafRef.current = requestAnimationFrame(draw);

    return () => {
      window.removeEventListener("resize", resize);
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseleave", onMouseLeave);
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
