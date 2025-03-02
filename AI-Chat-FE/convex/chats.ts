import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { getCurrentUserOrThrow } from "./users";

export const get = query({
    args: { id: v.id("chats") },
    handler: async (ctx, args) => {
        return await ctx.db.get(args.id);
    },
});

export const create = mutation({
    args: {},
    handler: async (ctx) => {
        const user = await getCurrentUserOrThrow(ctx);

        const chatId = await ctx.db.insert("chats", {
            userId: user._id,
            title: "New chat",
        });

        return chatId;
    },
});

export const list = query({
    args: {},
    handler: async (ctx) => {
        const user = await getCurrentUserOrThrow(ctx);

        return ctx.db
            .query("chats")
            .withIndex("by_userId", (q) => q.eq("userId", user._id))
            .order("desc")
            .collect();
    },
});

export const rename = mutation({
    args: { id: v.id("chats"), title: v.string() },
    handler: async (ctx, args) => {
        await ctx.db.patch(args.id, {
            title: args.title,
        });
    },
});

export const remove = mutation({
    args: { id: v.id("chats") },
    handler: async (ctx, args) => {
        await ctx.db.delete(args.id);
    },
});
