import { useState } from "react";

import { axiosClient } from "@/lib/axios";
import { useCreateMessage } from "../api/use-create-message";

import { toast } from "sonner";

type TMessage = {
    chatId: string;
    content: string;
    bonus?: string;
};

export const useSubmitMessage = () => {
    const [isPending, setIsPending] = useState(false);

    const { mutateAsync } = useCreateMessage();

    const sendMessage = async ({ chatId, content, bonus = "" }: TMessage) => {
        try {
            setIsPending(true);
            // send user message
            await mutateAsync({
                chatId: chatId as any,
                content,
                role: "user",
            });

            const res = await axiosClient.post<{ response: string }>("/", {
                message: bonus + " hỏi: " + content,
            });

            console.log("🚀 ~ sendMessage ~ res:", res.data.response);

            const msg = res.data.response;

            // send bot message
            await mutateAsync({
                role: "assistant",
                chatId: chatId as any,
                content: msg,
            });
        } catch (error) {
            toast.error("Fail to send message");
        } finally {
            setIsPending(false);
        }
    };

    return { sendMessage, isPending };
};
