"use client";

import { Button } from "@/components/ui/button";
import { SidebarIcon, SquarePen } from "lucide-react";

import { useCreateChat } from "../api/use-create-chat";

export const NewChatButton = () => {
    const { mutate } = useCreateChat();

    return (
        <div className="flex justify-between">
            <Button size="icon">
                <SidebarIcon className="size-4" />
            </Button>
            <Button size="icon" onClick={() => void mutate({})}>
                <SquarePen className="size-4" />
            </Button>
        </div>
    );
};
