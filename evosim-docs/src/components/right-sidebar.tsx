"use client";

import { TableOfContents } from "./table-of-contents";
import { cn } from "@/lib/utils";

interface RightSidebarProps {
  className?: string;
}

export function RightSidebar({ className }: RightSidebarProps) {
  return (
    <aside
      className={cn(
        "hidden lg:block w-64 shrink-0 sticky top-20 h-fit",
        "border-l border-border pl-6",
        className
      )}
    >
      <div className="space-y-6">
        <TableOfContents />
      </div>
    </aside>
  );
}
