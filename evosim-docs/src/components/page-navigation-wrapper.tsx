"use client";

import { usePathname } from "next/navigation";
import { PageNavigation } from "./page-navigation";
import { getPageNavigation } from "@/lib/navigation";

export function PageNavigationWrapper() {
  const pathname = usePathname();
  const { previous, next } = getPageNavigation(pathname);
  
  return <PageNavigation previous={previous} next={next} />;
}
