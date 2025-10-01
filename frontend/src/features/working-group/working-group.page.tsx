// pages/working_groups/WorkingGroupPage.tsx
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchWorkingGroup } from "@/shared/api/working-groups";
import AccountWorkersTable from "@/features/working-group/ui/account-workers-table";
import { WorkingGroupSettingsTab } from "@/features/working-group/working-group-settings-tab";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/shared/ui/tabs";
import { Card, CardContent } from "@/shared/ui/card";

function Stat({ value, label }: { value: number | string; label: string }) {
  return (
    <div className="flex flex-col items-center">
      <span className="text-xl font-semibold leading-none">{value}</span>
      <span className="text-xs text-muted-foreground mt-1">{label}</span>
    </div>
  );
}

function WorkingGroupPage() {
  const { wgId } = useParams<{ wgId: string }>();

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["working_group", wgId],
    queryFn: () => fetchWorkingGroup(wgId!),
    enabled: !!wgId,
    staleTime: 10_000,
  });

  if (isLoading) return <div>Загрузка…</div>;
  if (isError) return <div className="text-destructive">{String(error)}</div>;
  if (!data) return <div>Группа не найдена</div>;


  const group = data.result as any;

  return (
    <div className="p-6 space-y-6">


      <Tabs defaultValue="accounts" className="w-full">
        <TabsList>
          <TabsTrigger value="accounts">Аккаунты</TabsTrigger>
          <TabsTrigger value="settings">Настройки</TabsTrigger>
        </TabsList>

        <TabsContent value="accounts" className="w-full">
          <Card className="w-full">
            <CardContent className="p-0">
              <div className="p-3">
                <AccountWorkersTable wgId={wgId!} initialPageSize={50} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings" className="w-full">
            <CardContent className="p-0">
              <div className="p-3">
                <WorkingGroupSettingsTab wgId={wgId!} initialPageSize={10} />
              </div>
            </CardContent>
        </TabsContent>
      </Tabs>
    </div>
  );
}

export const Component = WorkingGroupPage;