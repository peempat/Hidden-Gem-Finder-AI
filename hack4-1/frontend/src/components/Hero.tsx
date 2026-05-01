import React from 'react'
import { ArrowDown, MapPinned } from 'lucide-react'

const Hero: React.FC = () => {
  return (
    <section className="hero-landing" aria-labelledby="hero-title">
      <div className="hero-overlay" />

      <div className="hero-content">
        <p className="hero-kicker">WELCOME</p>
        <h1 id="hero-title">Gemmy AI</h1>
        <p className="hero-subtitle">Plan a Thailand trip that feels simple, calm, and made for your travel style.</p>

        <a className="hero-cta" href="#planner">
          <MapPinned size={18} />
          Start Planning
          <ArrowDown size={16} />
        </a>
      </div>
    </section>
  )
}

export default Hero
