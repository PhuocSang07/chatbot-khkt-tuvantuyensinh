"use client";

import Image from "next/image";

import { Markdown } from "@/features/messages/components/markdown";
import { Doc } from "../../../../convex/_generated/dataModel";

type Props = {
    message: Doc<"messages">;
};

export const MessageItem = ({ message }: Props) => {
    return (
        <div className="relative flex">
            {message.role === "user" ? (
                <div className="mb-3 ml-auto max-w-[50%] rounded-3xl bg-neutral-600 px-3 py-2 text-white">
                    {message.content}
                </div>
            ) : (
                <div className="mb-3 flex gap-4">
                    <div className="flex size-14 shrink-0 items-center justify-center rounded-full">
                        <Image
                            src="/logo.svg"
                            alt="Bot"
                            width={200}
                            height={200}
                        />
                    </div>
                    <div>
                        <Markdown content={message.content} />
                    </div>
                </div>
            )}
        </div>
    );
};
