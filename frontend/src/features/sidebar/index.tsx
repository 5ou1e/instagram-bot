"use client";

import { Sidebar, SidebarContent, SidebarFooter, SidebarHeader, SidebarRail } from "@/shared/ui/sidebar";
import { HomeSection } from "./ui/sections/home-section";
import { WorkingGroupsSection } from "./ui/sections/working-groups-section";
import type { AppSidebarProps } from "./ui/types";

export function AppSidebar(props: AppSidebarProps) {
  return (
    <Sidebar className="border-r">
      <SidebarHeader>
        <div className="px-2 py-1.5 text-sm font-semibold">Панель</div>
      </SidebarHeader>

      <SidebarContent>
        <HomeSection />
        <WorkingGroupsSection {...props} />
      </SidebarContent>

      <SidebarFooter>
        <div className="px-2 py-2 text-xs text-muted-foreground">© {new Date().getFullYear()} — Instagram-bot</div>
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  );
}
