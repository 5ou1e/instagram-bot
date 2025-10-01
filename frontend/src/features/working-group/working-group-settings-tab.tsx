"use client"

import * as React from "react"
import { Button } from "@/shared/ui/button"
import { Switch } from "@/shared/ui/switch"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/shared/ui/dialog"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/shared/ui/card"
import { GripVertical, Settings } from "lucide-react"

// ВАЖНО: импортируем как неймспейс — у diceui так в примерах
import * as Sortable from "@/shared/ui/sortable"

type Task = {
  id: string
  name: string
  enabled: boolean
  description?: string
}

const initialTasks: Task[] = [
  { id: "1", name: "Лайкинг", enabled: true, description: "Ставим лайки по хэштегам" },
  { id: "2", name: "Подписки", enabled: false, description: "Подписки на новых пользователей" },
  { id: "3", name: "Комментарии", enabled: true, description: "Оставляем комментарии по шаблону" },
  { id: "4", name: "Рассылки", enabled: false, description: "Директ-рассылки по базе" },
]

export function WorkingGroupSettingsTab() {
  const [tasks, setTasks] = React.useState<Task[]>(initialTasks)
  const [selectedTask, setSelectedTask] = React.useState<Task | null>(null)

  // diceui ожидает value = массив элементов и onValueChange = сеттер массива
  return (
    <div className="p-6 space-y-4">
      <Sortable.Root
        value={tasks}
        onValueChange={setTasks}
        getItemValue={(item: Task) => item.id}
        // orientation="vertical" // можно явно указать
      >
        <Sortable.Content className="flex flex-col gap-2.5">
          {tasks.map((task) => (
            <Sortable.Item key={task.id} value={task.id} asChild>
              <Card
                className={`flex items-center justify-between transition ${
                  task.enabled ? "" : "bg-muted opacity-70"
                }`}
              >
                <CardHeader className="flex flex-row items-center gap-3 p-4">
                  {/* Ручка перетаскивания: обязательно используем ItemHandle */}
                  <Sortable.ItemHandle asChild>
                    <button
                      type="button"
                      aria-label="Перетащить"
                      className="inline-flex items-center justify-center rounded p-1 text-muted-foreground cursor-grab data-[dragging]:cursor-grabbing"
                    >
                      <GripVertical className="h-4 w-4" />
                    </button>
                  </Sortable.ItemHandle>

                  <div>
                    <CardTitle className="text-sm">{task.name}</CardTitle>
                    <CardDescription>{task.description}</CardDescription>
                  </div>
                </CardHeader>

                <CardContent className="flex items-center gap-4">
                  <Switch
                    checked={task.enabled}
                    onCheckedChange={(v) =>
                      setTasks((prev) =>
                        prev.map((t) => (t.id === task.id ? { ...t, enabled: v } : t)),
                      )
                    }
                  />
                  <Button size="sm" variant="outline" onClick={() => setSelectedTask(task)}>
                    <Settings className="h-4 w-4 mr-1" /> Настройки
                  </Button>
                </CardContent>
              </Card>
            </Sortable.Item>
          ))}
        </Sortable.Content>

        {/* Drag-overlay (можно сделать динамический по доке) */}
        <Sortable.Overlay>
          <div className="size-full rounded-md bg-primary/10" />
        </Sortable.Overlay>
      </Sortable.Root>

      <Dialog open={!!selectedTask} onOpenChange={() => setSelectedTask(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Настройки: {selectedTask?.name}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <p>Здесь будет форма настроек задачи.</p>
            <Button onClick={() => setSelectedTask(null)}>Сохранить</Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
