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
      const spacing = 50;
      const radius = 280;
      const mx = mouseRef.current.x;
      const my = mouseRef.current.y;

      ctx!.clearRect(0, 0, w, h);

      // Cursor halo glow
      if (mx > -500 && my > -500) {
        const halo = ctx!.createRadialGradient(mx, my, 0, mx, my, radius * 1.2);
        halo.addColorStop(0, "rgba(212, 168, 67, 0.04)");
        halo.addColorStop(0.5, "rgba(74, 144, 217, 0.02)");
        halo.addColorStop(1, "transparent");
        ctx!.fillStyle = halo;
        ctx!.fillRect(0, 0, w, h);
      }

      // Vertical lines
      for (let x = 0; x <= w; x += spacing) {
        const dist = Math.abs(x - mx);
        const intensity = Math.max(0, 1 - dist / radius);

        ctx!.beginPath();
        ctx!.moveTo(x, 0);
        ctx!.lineTo(x, h);
        ctx!.strokeStyle = intensity > 0.05
          ? `rgba(212, 168, 67, ${0.04 + intensity * 0.18})`
          : "rgba(255, 255, 255, 0.025)";
        ctx!.lineWidth = intensity > 0.1 ? 0.8 : 0.4;
        ctx!.stroke();
      }

      // Horizontal lines
      for (let y = 0; y <= h; y += spacing) {
        const dist = Math.abs(y - my);
        const intensity = Math.max(0, 1 - dist / radius);

        ctx!.beginPath();
        ctx!.moveTo(0, y);
        ctx!.lineTo(w, y);
        ctx!.strokeStyle = intensity > 0.05
          ? `rgba(212, 168, 67, ${0.04 + intensity * 0.18})`
          : "rgba(255, 255, 255, 0.025)";
        ctx!.lineWidth = intensity > 0.1 ? 0.8 : 0.4;
        ctx!.stroke();
      }

      // Intersection glow nodes
      for (let x = 0; x <= w; x += spacing) {
        for (let y = 0; y <= h; y += spacing) {
          const dx = x - mx;
          const dy = y - my;
          const dist = Math.sqrt(dx * dx + dy * dy);
          const intensity = Math.max(0, 1 - dist / radius);

          if (intensity > 0.02) {
            // Inner bright dot
            ctx!.beginPath();
            ctx!.arc(x, y, 1 + intensity * 3, 0, Math.PI * 2);
            ctx!.fillStyle = `rgba(212, 168, 67, ${intensity * 0.7})`;
            ctx!.fill();

            // Outer glow ring
            if (intensity > 0.2) {
              ctx!.beginPath();
              ctx!.arc(x, y, 3 + intensity * 10, 0, Math.PI * 2);
              ctx!.fillStyle = `rgba(212, 168, 67, ${intensity * 0.06})`;
              ctx!.fill();
            }

            // Bright core at close range
            if (intensity > 0.6) {
              ctx!.beginPath();
              ctx!.arc(x, y, 2, 0, Math.PI * 2);
              ctx!.fillStyle = `rgba(240, 199, 94, ${intensity * 0.8})`;
              ctx!.fill();
            }
          } else {
            // Subtle base dots even without mouse
            ctx!.beginPath();
            ctx!.arc(x, y, 0.5, 0, Math.PI * 2);
            ctx!.fillStyle = "rgba(255, 255, 255, 0.03)";
            ctx!.fill();
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
      className="fixed inset-0 z-[1] pointer-events-none"
      aria-hidden="true"
    />
  );
}
