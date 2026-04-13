"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export default function HeroSection() {
  return (
    <section className="relative flex items-center justify-center min-h-[85vh] px-4 overflow-hidden">
      {/* Hero gradient overlays */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[600px] bg-accent-gold/[0.04] rounded-full blur-[120px]" />
        <div className="absolute bottom-0 left-0 right-0 h-40 bg-gradient-to-t from-bg-primary to-transparent" />
      </div>

      <div className="relative text-center max-w-4xl mx-auto">
        {/* Overline badge */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="mb-8"
        >
          <span className="inline-flex items-center gap-2 px-4 py-1.5 glass-panel rounded-full text-xs font-medium text-text-secondary">
            <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
            Live Science Intelligence
          </span>
        </motion.div>

        {/* Main headline */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] mb-6"
        >
          <span className="text-gradient-hero">See the full picture.</span>
          <br />
          <span className="text-gradient-gold glow-text">Trust the source.</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.35 }}
          className="text-lg sm:text-xl text-text-secondary max-w-2xl mx-auto mb-10 leading-relaxed"
        >
          AI-powered intelligence tracking live developments in{" "}
          <span className="text-text-primary font-medium">space exploration</span>,{" "}
          <span className="text-text-primary font-medium">quantum physics</span>, and{" "}
          <span className="text-text-primary font-medium">frontier research</span>.
        </motion.p>

        {/* CTA buttons */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <Link href="#feed" className="btn-primary text-base px-8 py-3">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Explore Feed
          </Link>
          <Link href="/trends" className="btn-secondary text-base px-8 py-3">
            View Trends
          </Link>
        </motion.div>

        {/* Stats row */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.7 }}
          className="mt-16 flex items-center justify-center gap-8 sm:gap-12"
        >
          {[
            { value: "9+", label: "Sources" },
            { value: "4", label: "Categories" },
            { value: "24/7", label: "Monitoring" },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <p className="text-2xl font-bold font-mono text-gradient-gold">{stat.value}</p>
              <p className="text-xs text-text-muted mt-1 uppercase tracking-wider">{stat.label}</p>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
