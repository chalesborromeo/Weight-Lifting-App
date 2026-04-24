import type { BodyMetric, BodyMetricCreate } from "@/types";
import { request } from "./client";

export const bodyMetricsApi = {
  list: () => request<BodyMetric[]>("/body-metrics/"),
  create: (data: BodyMetricCreate) =>
    request<BodyMetric>("/body-metrics/", { method: "POST", body: data }),
};
