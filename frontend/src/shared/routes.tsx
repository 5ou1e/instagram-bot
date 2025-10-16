import { generatePath } from "react-router-dom";

export const ROUTES = {
  HOME: "/",
  WORKING_GROUP: "/working-groups/:wgId",
  PROXIES: "/proxies"
} as const;

export const linkToWorkingGroup = (wgId: string) =>
  generatePath(ROUTES.WORKING_GROUP, { wgId });

export type PathParams = {
  [ROUTES.WORKING_GROUP]: { wgId: string };
};

// типобезопасные params (react-router v6.21+)
declare module "react-router-dom" {
  interface Register {
    params: PathParams;
  }
}
