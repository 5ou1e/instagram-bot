"use client";

import { Network as ProxiesIcon} from "lucide-react";
import { ROUTES } from "@/shared/routes";
import { Link, useMatch } from "react-router-dom";
import { Sidebar, SidebarContent, SidebarFooter, SidebarHeader, SidebarRail } from "@/shared/ui/sidebar";
import { HomeSection } from "./ui/sections/home-section";
import { WorkingGroupsSection } from "./ui/sections/working-groups-section";
import type { AppSidebarProps } from "./ui/types";
import { SidebarGroup, SidebarGroupLabel, SidebarMenu, SidebarMenuButton, SidebarMenuItem } from "@/shared/ui/sidebar";

export function AppSidebar(props: AppSidebarProps) {
  const proxiesMatch = useMatch({ path: ROUTES.PROXIES, end: true });
  return (
    <Sidebar className="border-r">
      <SidebarHeader>
        <div className="px-2 py-1.5 text-sm font-semibold">Панель</div>
      </SidebarHeader>

      <SidebarContent>
        <HomeSection />
        <WorkingGroupsSection {...props} />
      </SidebarContent>

      <SidebarContent>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton asChild isActive={!!proxiesMatch}>
            <Link to={ROUTES.PROXIES}>
              <ProxiesIcon className="mr-2 h-4 w-4" />
              Прокси
            </Link>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
      </SidebarContent>

      <SidebarFooter>
        <div className="px-2 py-2 text-xs text-muted-foreground">© {new Date().getFullYear()} — Instagram-bot</div>
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  );
}
