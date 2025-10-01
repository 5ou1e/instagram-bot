export type WorkingGroupItem = {
  id: string;
  name: string;
  status?: string | null;
};

export type AppSidebarProps = {
  currentGroupId?: string;
  onGroupSelect?: (group: WorkingGroupItem) => void;
};
