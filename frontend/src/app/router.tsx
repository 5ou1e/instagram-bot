import { ROUTES } from "../shared/routes";
import { createBrowserRouter, redirect } from "react-router-dom";
import { App } from "./app";
import { Providers } from "./providers";

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
        path: ROUTES.HOME,
        loader: () => import("@/features/home/home.page"),
      },
    ],
  },
]);