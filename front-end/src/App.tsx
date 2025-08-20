import { Outlet } from "react-router";
import { SidebarInset, SidebarProvider } from "./components/ui/sidebar";
import { AppSidebar } from "./components/core/AppSidebarComponent";
import { Home, Link, Upload, type LucideIcon } from "lucide-react";
import {
  QueryCache,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";
import { toast, Toaster } from "sonner";

const items: { href: string; icon: LucideIcon; title: string }[] = [
  { href: "/", icon: Home, title: "Home" },
  { href: "/upload", icon: Upload, title: "Upload" },
  { href: "/references", icon: Link, title: "Dashboards" },
  // { href: "/inspect", icon: Eye, title: "Inspect" },
  // { href: "/save", icon: Save, title: "Save" },
];
function App() {
  const queryClient = new QueryClient({
    queryCache: new QueryCache({
      onError: (error) => {
        if (error) toast.error(error.message);
      },
    }),
  });

  return (
    <QueryClientProvider client={queryClient}>
      <SidebarProvider>
        <AppSidebar items={items} />
        <SidebarInset>
          <Outlet />
        </SidebarInset>
      </SidebarProvider>
      <Toaster position="top-right" richColors />
    </QueryClientProvider>
  );
}

export default App;
