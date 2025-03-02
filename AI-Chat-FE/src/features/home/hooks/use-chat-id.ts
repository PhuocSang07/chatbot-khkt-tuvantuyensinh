import { useParams } from "next/navigation";

export const useChatId = () => {
    const { chatId } = useParams<{ chatId: string }>();

    return chatId;
};
