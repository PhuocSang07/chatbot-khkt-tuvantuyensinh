import { MobileSidebar } from "@/components/mobile-sidebar";
import { Sidebar } from "@/components/sidebar";

type Props = {
    children: React.ReactNode;
};

export default function HomeLayout({ children }: Props) {
    return (
        <div className="relative flex h-full bg-neutral-800">
            <Sidebar />
            <div>
                <MobileSidebar />
            </div>
            <div className="h-full flex-1 pl-14">{children}</div>
        </div>
    );
}
