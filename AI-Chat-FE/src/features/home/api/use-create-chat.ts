import { ConvexError } from "convex/values";
import { api } from "../../../../convex/_generated/api";

import { useConvexMutation } from "@convex-dev/react-query";
import { useMutation } from "@tanstack/react-query";

import { toast } from "sonner";

export const useCreateChat = () => {
    const mutation = useMutation({
        mutationFn: useConvexMutation(api.chats.create),
        onError(error) {
            const errorMessage =
                error instanceof ConvexError
                    ? error.data
                    : "Unexpected error occurred";

            toast.error(errorMessage);
        },
    });

    return mutation;
};
