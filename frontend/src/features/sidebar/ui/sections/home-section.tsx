import { Link, useMatch } from "react-router-dom";
import { Home as HomeIcon } from "lucide-react";
import { SidebarGroup, SidebarGroupLabel, SidebarMenu, SidebarMenuButton, SidebarMenuItem } from "@/shared/ui/sidebar";
import { ROUTES } from "@/shared/routes";

export function HomeSection() {
  const homeMatch = useMatch({ path: ROUTES.HOME, end: true });
  return (
    <SidebarGroup>
      <SidebarGroupLabel>Навигация</SidebarGroupLabel>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton asChild isActive={!!homeMatch}>
            <Link to={ROUTES.HOME}>
              <HomeIcon className="mr-2 h-4 w-4" />
              Главная
            </Link>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarGroup>
  );
}
