import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
import { Loader2 } from "lucide-react";
const loaderVariants = cva("animate-spin text-primary", {
  variants: {
    size: {
      small: "size-6",
      medium: "size-8",
      large: "size-12",
    },
  },
  defaultVariants: {
    size: "medium",
  },
});

interface SpinnerContentProps extends VariantProps<typeof loaderVariants> {
  className?: string;
}

export function Spinner({ size, className }: SpinnerContentProps) {
  return <Loader2 className={cn(loaderVariants({ size }), className)} />;
}
