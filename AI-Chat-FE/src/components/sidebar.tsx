"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";

import { cn } from "@/lib/utils";
import { PenSquare, SidebarIcon } from "lucide-react";

import { ChatList } from "../features/chats/components/chat-list";

import { useCreateChat } from "@/features/home/api/use-create-chat";

export const Sidebar = () => {
    const [isCollapsed, setIsCollapsed] = useState(false);
    const router = useRouter();

    const { mutate } = useCreateChat();

    const onNewChat = () => {
        mutate(
            {},
            {
                onSuccess(id) {
                    router.push(`/${id}`);
                },
            },
        );
    };
    return (
        <div className="relative hidden lg:block">
            <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsCollapsed(false)}
                className={cn(
                    "absolute left-4 top-2 hidden",
                    isCollapsed && "block",
                )}
            >
                <SidebarIcon className="size-4" />
            </Button>

            {!isCollapsed && (
                <div className="h-full w-[260px] bg-neutral-900 px-2 py-2">
                    <div className="fixed left-0 top-0 z-10 w-[260px] bg-neutral-900 px-2 pt-2">
                        <div className="flex justify-between">
                            <Button
                                size="icon"
                                variant="ghost"
                                onClick={() => setIsCollapsed(true)}
                            >
                                <SidebarIcon className="size-4" />
                            </Button>
                            <Button
                                size="icon"
                                variant="ghost"
                                onClick={onNewChat}
                            >
                                <PenSquare className="size-4" />
                            </Button>
                        </div>
                    </div>

                    <ScrollArea className="mt-10 pr-2">
                        <ChatList />
                    </ScrollArea>
                </div>
            )}
        </div>
    );
};
