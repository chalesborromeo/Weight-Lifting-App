import type { ReactNode } from "react";

type Props = {
  title: string;
  action?: ReactNode;
};

export function SectionHeader({ title, action }: Props) {
  return (
    <div className="flex items-center justify-between">
      <h2 className="text-lg font-semibold text-foreground">{title}</h2>
      {action}
    </div>
  );
}
