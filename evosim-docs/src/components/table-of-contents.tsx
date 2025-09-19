"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

interface Heading {
  id: string;
  text: string;
  level: number;
}

interface TableOfContentsProps {
  className?: string;
}

export function TableOfContents({ className }: TableOfContentsProps) {
  const [headings, setHeadings] = useState<Heading[]>([]);
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    const headingElements = document.querySelectorAll("h1, h2, h3");
    
    const headingList: Heading[] = Array.from(headingElements).map((heading) => {
      const id = heading.id || heading.textContent?.toLowerCase().replace(/\s+/g, "-").replace(/[^\w\-]+/g, "") || "";
      
      // Set the id if it doesn't exist
      if (!heading.id) {
        heading.id = id;
      }
      
      return {
        id,
        text: heading.textContent || "",
        level: parseInt(heading.tagName.charAt(1))
      };
    });

    setHeadings(headingList);

    // Set up intersection observer for active heading
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        });
      },
      {
        rootMargin: "-20% 0% -35% 0%",
        threshold: 0.1,
      }
    );

    headingElements.forEach((heading) => observer.observe(heading));

    return () => {
      headingElements.forEach((heading) => observer.unobserve(heading));
    };
  }, []);

  const scrollToHeading = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  if (headings.length === 0) {
    return null;
  }

  return (
    <div className={cn("space-y-2", className)}>
      <h4 className="font-medium text-sm text-muted-foreground">On This Page</h4>
      <nav className="space-y-1">
        {headings.map((heading) => (
          <button
            key={heading.id}
            onClick={() => scrollToHeading(heading.id)}
            className={cn(
              "block w-full text-left text-sm transition-colors hover:text-foreground py-1 px-2 rounded-sm",
              heading.level === 1 && "font-medium",
              heading.level === 2 && "ml-0",
              heading.level === 3 && "ml-3",
              heading.level === 4 && "ml-6",
              heading.level === 5 && "ml-9",
              heading.level === 6 && "ml-12",
              activeId === heading.id
                ? "text-foreground font-medium bg-muted"
                : "text-muted-foreground hover:bg-muted/50"
            )}
          >
            {heading.text}
          </button>
        ))}
      </nav>
    </div>
  );
}
