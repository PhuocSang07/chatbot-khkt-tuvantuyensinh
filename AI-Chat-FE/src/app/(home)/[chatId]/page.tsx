import { ScrollArea } from "@/components/ui/scroll-area";
import { UserButton } from "@/components/user-button";

import { ChatInput } from "@/features/chats/components/chat-input";
import { MessagesList } from "@/features/messages/components/messages-list";

export default function ChatPage() {
    return (
        <div className="flex h-full flex-col overscroll-none py-3 pr-14">
            <div className="ml-auto mt-3">
                <UserButton />
            </div>
            <ScrollArea className="my-2 h-full flex-1">
                <MessagesList />
            </ScrollArea>
            <ChatInput />
        </div>
    );
}
