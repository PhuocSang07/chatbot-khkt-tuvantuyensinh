"use client";

import ReactMarkdown from "react-markdown";
import SyntaxHighlighter from "react-syntax-highlighter";
import { vs2015 } from "react-syntax-highlighter/dist/esm/styles/hljs";
import remarkGfm from "remark-gfm";

import { Check, Copy } from "lucide-react";

import { useCopyToClipboard } from "@/hooks/use-copy-to-clipboard";

interface Props {
    content: string;
}

export const Markdown = ({ content }: Props) => {
    const { copyToClipboard, isCopied } = useCopyToClipboard();

    return (
        <>
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                className="markdown"
                components={{
                    code({ node, className, children, ...props }) {
                        const match = /language-(\w+)/.exec(className || "");
                        return match ? (
                            <div className="py-6">
                                <div className="flex w-full justify-end rounded-t-md bg-white/5 p-2">
                                    <button
                                        onClick={() =>
                                            copyToClipboard(
                                                String(children).replace(
                                                    /\n$/,
                                                    "",
                                                ),
                                            )
                                        }
                                        className="flex items-center gap-1 text-sm text-neutral-300"
                                    >
                                        {isCopied ? (
                                            <>
                                                <Check className="size-4" />
                                                Copied!
                                            </>
                                        ) : (
                                            <>
                                                <Copy className="size-4" />
                                                Copy code
                                            </>
                                        )}
                                    </button>
                                </div>
                                <SyntaxHighlighter
                                    language={match[1]}
                                    style={vs2015}
                                >
                                    {String(children).replace(/\n$/, "")}
                                </SyntaxHighlighter>
                            </div>
                        ) : (
                            <code className={className} {...props}>
                                {children}
                            </code>
                        );
                    },
                }}
            >
                {content}
            </ReactMarkdown>

            {/* <div ref={scrollRef} /> */}
        </>
    );
};
