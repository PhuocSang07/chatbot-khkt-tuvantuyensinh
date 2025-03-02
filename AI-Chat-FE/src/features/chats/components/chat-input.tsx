"use client";

import Image from "next/image";
import { KeyboardEvent, useEffect, useRef, useState } from "react";

import { Textarea } from "@/components/ui/textarea";

import { useChatId } from "@/features/home/hooks/use-chat-id";

import { useMessagesList } from "@/features/messages/api/use-messages-list";
import { useSubmitMessage } from "@/features/messages/hooks/use-submit-message";

const MAX_HEIGHT = 200;

export const ChatInput = () => {
    const [msg, setMsg] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const chatId = useChatId();
    const { isPending, sendMessage } = useSubmitMessage();
    const { data } = useMessagesList(chatId);

    useEffect(() => {
        const textarea = textareaRef.current;
        if (!textarea) return;

        const adjustHeight = () => {
            textarea.style.height = "auto";
            textarea.style.height = `${Math.min(textarea.scrollHeight, MAX_HEIGHT)}px`;
        };

        textarea.addEventListener("input", adjustHeight);
        adjustHeight();

        return () => {
            textarea.removeEventListener("input", adjustHeight);
        };
    }, []);

    const onKeyDown = async (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter") {
            e.preventDefault();

            setMsg("");

            const bonus = data
                ?.slice(-3)
                .map((msg) => msg.content)
                .join(" ");
            await sendMessage({ chatId, content: msg, bonus });
        }
    };

    return (
        <div className="flex flex-col gap-2">
            {isPending && (
                <div className="mb-3 flex gap-4">
                    <div className="flex size-12 shrink-0 items-center justify-center rounded-full">
                        <Image
                            src="/logo.svg"
                            alt="Bot"
                            width={150}
                            height={150}
                        />
                    </div>
                    <div className="loader"></div>
                </div>
            )}
            <Textarea
                disabled={isPending}
                ref={textareaRef}
                value={msg}
                onChange={(e) => setMsg(e.target.value)}
                placeholder={isPending ? "AI thinking..." : "Message AI chat"}
                className="max-h-[200px] w-full resize-none overflow-y-auto rounded-xl border bg-neutral-700 p-3 text-base shadow-md outline-none transition-all duration-200 ease-in-out focus-visible:outline-none focus-visible:ring-0 focus-visible:ring-offset-0"
                onKeyDown={onKeyDown}
            />
            <p className="ml-auto text-xs text-muted-foreground">
                Ctrl + Enter to new line
            </p>
        </div>
    );
};
