"use client";

import { useRef, useCallback } from "react";

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  tilt?: boolean;
  padding?: "sm" | "md" | "lg";
  onClick?: () => void;
}

const paddingMap = { sm: "p-3", md: "p-5", lg: "p-6" };

export default function GlassCard({
  children,
  className = "",
  hover = true,
  tilt = true,
  padding = "md",
  onClick,
}: GlassCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const rafRef = useRef<number | null>(null);
  const currentRotateX = useRef(0);
  const currentRotateY = useRef(0);
  const targetRotateX = useRef(0);
  const targetRotateY = useRef(0);
  const isHovering = useRef(false);

  const animateTilt = useCallback(() => {
    currentRotateX.current += (targetRotateX.current - currentRotateX.current) * 0.12;
    currentRotateY.current += (targetRotateY.current - currentRotateY.current) * 0.12;

    if (cardRef.current) {
      cardRef.current.style.transform = `perspective(800px) rotateX(${currentRotateX.current}deg) rotateY(${currentRotateY.current}deg) translateY(-2px)`;
    }

    if (
      isHovering.current ||
      Math.abs(currentRotateX.current) > 0.01 ||
      Math.abs(currentRotateY.current) > 0.01
    ) {
      rafRef.current = requestAnimationFrame(animateTilt);
    } else {
      currentRotateX.current = 0;
      currentRotateY.current = 0;
      if (cardRef.current) {
        cardRef.current.style.transform = "";
        cardRef.current.classList.remove("tilt-ready");
      }
      rafRef.current = null;
    }
  }, []);

  const onMouseEnter = useCallback(() => {
    if (!tilt) return;
    isHovering.current = true;
    cardRef.current?.classList.add("tilt-ready");
    if (!rafRef.current) rafRef.current = requestAnimationFrame(animateTilt);
  }, [tilt, animateTilt]);

  const onMouseMove = useCallback(
    (e: React.MouseEvent) => {
      if (!tilt || !cardRef.current) return;
      const rect = cardRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      cardRef.current.style.setProperty("--mouse-x", `${x}px`);
      cardRef.current.style.setProperty("--mouse-y", `${y}px`);

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      targetRotateX.current = ((y - centerY) / centerY) * -6;
      targetRotateY.current = ((x - centerX) / centerX) * 6;
    },
    [tilt],
  );

  const onMouseLeave = useCallback(() => {
    if (!tilt) return;
    isHovering.current = false;
    targetRotateX.current = 0;
    targetRotateY.current = 0;
    if (cardRef.current) {
      cardRef.current.style.setProperty("--mouse-x", "50%");
      cardRef.current.style.setProperty("--mouse-y", "50%");
    }
    if (!rafRef.current) rafRef.current = requestAnimationFrame(animateTilt);
  }, [tilt, animateTilt]);

  return (
    <div
      ref={cardRef}
      className={`glass-card ${hover ? "glass-card-hover" : ""} ${paddingMap[padding]} ${className}`}
      style={{ transformStyle: "preserve-3d" }}
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      onMouseMove={onMouseMove}
      onMouseLeave={onMouseLeave}
    >
      {children}
    </div>
  );
}
