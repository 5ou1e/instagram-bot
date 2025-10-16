// app/router.tsx
import { createBrowserRouter } from "react-router-dom";
import { App } from "./app";
import { Providers } from "./providers";
import { ROUTES } from "../shared/routes";

export const router = createBrowserRouter([
  {
    element: (
      <Providers>
        <App />
      </Providers>
    ),
    children: [
      {
        path: ROUTES.WORKING_GROUP,
        lazy: () => import("@/features/working-group/working-group.page"),
      },
      {
        path: ROUTES.PROXIES,
        lazy: () => import("@/features/proxies/proxies.page"), // ← было loader
      },
      {
        path: ROUTES.HOME,
        lazy: () => import("@/features/home/home.page"), // ← было loader
      },
    ],
  },
]);
