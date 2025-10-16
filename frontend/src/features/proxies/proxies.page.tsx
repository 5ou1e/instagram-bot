import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchWorkingGroup } from "@/shared/api/working-groups";
import ProxiesTable from "@/features/proxies/ui/proxies-table";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/shared/ui/tabs";
import { Card, CardContent } from "@/shared/ui/card";


function ProxiesPage() {

  return (
    <div className="p-6 space-y-6">
        <Card className="w-full">
          <CardContent className="p-0">
            <div className="p-3">
              <ProxiesTable initialPageSize={500} />
            </div>
          </CardContent>
        </Card>
    </div>
  );
}

export const Component = ProxiesPage;