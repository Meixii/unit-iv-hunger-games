export interface NavigationItem {
  title: string;
  url: string;
}

export const navigationOrder: NavigationItem[] = [
  { title: "Project Objectives", url: "/objectives" },
  { title: "Project Scope", url: "/scope" },
  { title: "Project Limitations", url: "/limitations" },
  { title: "Terminologies", url: "/terminologies" },
  { title: "MLP & Evolutionary Algorithm", url: "/mlp-evolution" },
  { title: "Fitness Function", url: "/fitness-function" },
  { title: "Core Mechanics", url: "/core-mechanics" },
  { title: "Parameters & Variables", url: "/parameters" },
  { title: "Map & Objectives", url: "/map-objectives" },
  { title: "Events & Disasters", url: "/events-disasters" },
  { title: "Quantitative Mechanics", url: "/quantitative-mechanics" },
  { title: "Code Implementation", url: "/code-implementation" },
  { title: "Formulas & Computations", url: "/formulas" },
  { title: "Data Structure", url: "/data-structure" },
  { title: "Development Task List", url: "/development-tasks" },
  { title: "Implementation Phases", url: "/phases" },
];

export function getPageNavigation(currentUrl: string) {
  // Handle home page specially
  if (currentUrl === "/") {
    return {
      previous: undefined,
      next: navigationOrder[0] // First page after introduction
    };
  }
  
  const currentIndex = navigationOrder.findIndex(item => item.url === currentUrl);
  
  if (currentIndex === -1) {
    return { previous: undefined, next: undefined };
  }
  
  // For the first page in navigation order, previous should be home page
  const previous = currentIndex === 0 
    ? { title: "Introduction", url: "/" }
    : currentIndex > 0 ? navigationOrder[currentIndex - 1] : undefined;
    
  const next = currentIndex < navigationOrder.length - 1 ? navigationOrder[currentIndex + 1] : undefined;
  
  return { previous, next };
}
