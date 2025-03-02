import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

const schema = defineSchema({
    users: defineTable({
        name: v.string(),
        email: v.string(),
        imageUrl: v.optional(v.string()),
        externalId: v.string(),
    }).index("by_external_id", ["externalId"]),

    chats: defineTable({
        userId: v.id("users"),
        title: v.string(),
    }).index("by_userId", ["userId"]),

    messages: defineTable({
        role: v.union(v.literal("user"), v.literal("assistant")),
        content: v.string(),
        chatId: v.id("chats"),
    }).index("by_chatId", ["chatId"]),
});

export default schema;
