"use client";

import { QUESTIONS } from "@/constants";
import { useLayoutEffect, useRef } from "react";

import { Badge } from "@/components/ui/badge";

import { Loader } from "lucide-react";
import { MessageItem } from "./message-item";

import { useChatId } from "@/features/home/hooks/use-chat-id";

import { useMessagesList } from "@/features/messages/api/use-messages-list";
import { useSubmitMessage } from "../hooks/use-submit-message";

export const MessagesList = () => {
    const chatId = useChatId();
    const { data, isPending, isError } = useMessagesList(chatId);

    const scrollRef = useRef<HTMLDivElement>(null);
    const { sendMessage } = useSubmitMessage();

    useLayoutEffect(() => {
        const idTimeout = setTimeout(() => {
            scrollToBottom();
        }, 10);

        return () => clearTimeout(idTimeout);
    }, [data]);

    const scrollToBottom = () => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: "smooth" });
        }
    };

    if (isPending) {
        return (
            <div className="flex size-full items-center justify-center">
                <Loader className="size-10 animate-spin" />
            </div>
        );
    }

    if (isError) {
        return <div>Message not found</div>;
    }

    if (data.length === 0) {
        return (
            <div className="flex h-full flex-col items-center justify-center gap-6">
                <h1 className="text-4xl font-bold">What can I help with?</h1>

                <div className="flex flex-wrap justify-center gap-3">
                    {QUESTIONS.map((question, index) => (
                        <Badge
                            key={index}
                            variant="outline"
                            className="cursor-pointer bg-neutral-700 text-white hover:bg-neutral-700/60"
                            onClick={async () => {
                                await sendMessage({
                                    chatId,
                                    content: question,
                                });
                            }}
                        >
                            {question}
                        </Badge>
                    ))}
                </div>
            </div>
        );
    }

    return (
        <div className="overflow-auto overscroll-y-contain pr-2">
            {data.map((item) => (
                <MessageItem key={item._id} message={item} />
            ))}
            <div ref={scrollRef} />
        </div>
    );
};
