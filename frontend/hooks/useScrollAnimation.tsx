"use client";

import { useEffect, useRef, useState, RefObject } from "react";

export function useScrollAnimation<T extends HTMLElement>(): [RefObject<T>, boolean] {
  const ref = useRef<T>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          // Once visible, stop observing
          if (ref.current) {
            observer.unobserve(ref.current);
          }
        }
      },
      {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px",
      }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, []);

  return [ref, isVisible];
}

// Component wrapper for scroll animation
interface AnimateOnScrollProps {
  children: React.ReactNode;
  className?: string;
  delay?: number;
}

export function AnimateOnScroll({ children, className = "", delay = 0 }: AnimateOnScrollProps) {
  const [ref, isVisible] = useScrollAnimation<HTMLDivElement>();

  return (
    <div
      ref={ref}
      className={`animate-on-scroll ${isVisible ? "visible" : ""} ${className}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
}

// Staggered animation for lists
interface StaggeredListProps {
  children: React.ReactNode[];
  className?: string;
  staggerDelay?: number;
}

export function StaggeredList({ children, className = "", staggerDelay = 100 }: StaggeredListProps) {
  const [ref, isVisible] = useScrollAnimation<HTMLDivElement>();

  return (
    <div ref={ref} className={className}>
      {children.map((child, index) => (
        <div
          key={index}
          className={`animate-on-scroll ${isVisible ? "visible" : ""}`}
          style={{ transitionDelay: `${index * staggerDelay}ms` }}
        >
          {child}
        </div>
      ))}
    </div>
  );
}
