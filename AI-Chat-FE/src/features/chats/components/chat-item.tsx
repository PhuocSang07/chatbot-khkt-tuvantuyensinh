"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { KeyboardEvent, useState } from "react";

import { Doc } from "../../../../convex/_generated/dataModel";

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import { MoreHorizontal, Pencil, Trash2 } from "lucide-react";

import { cn } from "@/lib/utils";
import { toast } from "sonner";

import { useChatId } from "@/features/home/hooks/use-chat-id";
import { useConfirm } from "@/hooks/use-confirm";

import { useRemoveChat } from "@/features/home/api/use-remove-chat";
import { useRenameChat } from "@/features/home/api/use-rename-chat";

type Props = {
    chat: Doc<"chats">;
};

export const ChatItem = ({ chat }: Props) => {
    const [editing, setEditing] = useState(false);
    const [title, setTitle] = useState(chat.title);

    const chatId = useChatId();
    const isActive = chat._id === chatId;

    const rename = useRenameChat();
    const remove = useRemoveChat();

    const { confirm, ConfirmDialog } = useConfirm();
    const router = useRouter();

    const onSubmit = () => {
        if (title.trim().length === 0) return;

        rename.mutate(
            {
                id: chat._id,
                title,
            },
            {
                onSettled() {
                    setEditing(false);
                },
            },
        );
    };

    const onKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key !== "Enter") return;
        e.preventDefault();
        onSubmit();
    };

    const onDelete = async () => {
        const ok = await confirm();

        if (ok) {
            remove.mutate(
                { id: chat._id },
                {
                    onSuccess() {
                        toast.success("Deleted chat");
                        router.replace("/");
                    },
                },
            );
        }
    };

    return (
        <div
            className={cn(
                "mt-1 flex items-center justify-between rounded-md px-3 hover:bg-neutral-700",
                isActive && "bg-neutral-700",
            )}
        >
            <ConfirmDialog />
            {editing ? (
                <input
                    placeholder="Chat title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    onKeyDown={onKeyDown}
                    className="mr-2 w-full bg-neutral-800"
                    disabled={rename.isPending}
                    onBlur={onSubmit}
                    autoFocus
                />
            ) : (
                <Link href={`/${chat._id}`} className="mr-2 flex-1 truncate">
                    {chat.title}
                </Link>
            )}

            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <button
                        className="-mr-2 rounded-md p-2 hover:bg-neutral-700"
                        disabled={remove.isPending}
                    >
                        <MoreHorizontal className="size-4" />
                    </button>
                </DropdownMenuTrigger>
                <DropdownMenuContent side="right" align="start">
                    <DropdownMenuItem onClick={() => setEditing(true)}>
                        <Pencil className="size-4" />
                        Rename
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={onDelete}>
                        <Trash2 className="text-rose-600 hover:text-rose-600" />
                        <span className="text-rose-600 hover:text-rose-600">
                            Delete
                        </span>
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
    );
};
