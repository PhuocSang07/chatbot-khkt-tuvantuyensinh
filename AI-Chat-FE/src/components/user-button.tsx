import { UserButton as UserBtn } from "@clerk/nextjs";

export const UserButton = () => {
    return <UserBtn appearance={{ elements: { avatarBox: "size-10" } }} />;
};
