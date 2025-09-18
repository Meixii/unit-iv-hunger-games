"use client";

import * as React from "react"
import { GalleryVerticalEnd } from "lucide-react"
import { usePathname } from "next/navigation"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  SidebarRail,
} from "@/components/ui/sidebar"

// EvoSim Documentation Navigation
const data = {
  navMain: [
    {
      title: "Overview",
      url: "/",
      items: [
        {
          title: "Introduction",
          url: "/",
        },
        {
          title: "Project Objectives",
          url: "/objectives",
        },
        {
          title: "Project Scope",
          url: "/scope",
        },
        {
          title: "Project Limitations",
          url: "/limitations",
        },
      ],
    },
    {
      title: "Core Concepts",
      url: "/concepts",
      items: [
        {
          title: "Terminologies",
          url: "/terminologies",
        },
        {
          title: "MLP & Evolutionary Algorithm",
          url: "/mlp-evolution",
        },
        {
          title: "Fitness Function",
          url: "/fitness-function",
        },
      ],
    },
    {
      title: "Game Mechanics",
      url: "/mechanics",
      items: [
        {
          title: "Core Mechanics",
          url: "/core-mechanics",
        },
        {
          title: "Parameters & Variables",
          url: "/parameters",
        },
        {
          title: "Map & Objectives",
          url: "/map-objectives",
        },
        {
          title: "Events & Disasters",
          url: "/events-disasters",
        },
      ],
    },
    {
      title: "Technical Details",
      url: "/technical",
      items: [
        {
          title: "Quantitative Mechanics",
          url: "/quantitative-mechanics",
        },
        {
          title: "Code Implementation",
          url: "/code-implementation",
        },
        {
          title: "Formulas & Computations",
          url: "/formulas",
        },
        {
          title: "Data Structure",
          url: "/data-structure",
        },
      ],
    },
    {
      title: "Development",
      url: "/development",
      items: [
        {
          title: "Task List",
          url: "/development-tasks",
        },
        {
          title: "Implementation Phases",
          url: "/phases",
        },
      ],
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const pathname = usePathname();

  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="#">
                <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
                  <GalleryVerticalEnd className="size-4" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-medium">EvoSim Docs</span>
                  <span className="">v1.0.0</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            {data.navMain.map((item) => (
              <SidebarMenuItem key={item.title}>
                <SidebarMenuButton asChild isActive={pathname === item.url}>
                  <a href={item.url} className="font-medium">
                    {item.title}
                  </a>
                </SidebarMenuButton>
                {item.items?.length ? (
                  <SidebarMenuSub>
                    {item.items.map((subItem) => (
                      <SidebarMenuSubItem key={subItem.title}>
                        <SidebarMenuSubButton asChild isActive={pathname === subItem.url}>
                          <a href={subItem.url}>{subItem.title}</a>
                        </SidebarMenuSubButton>
                      </SidebarMenuSubItem>
                    ))}
                  </SidebarMenuSub>
                ) : null}
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  )
}
