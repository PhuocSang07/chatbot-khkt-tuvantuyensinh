import { useEffect, useState } from "react";

export const useTypeEffect = (text: string, speed = 100) => {
    const [displayedText, setDisplayedText] = useState("");

    useEffect(() => {
        let index = 0;

        const intervalId = setInterval(() => {
            setDisplayedText((prev) => {
                if (text[index]) {
                    return prev + text[index];
                }
                return prev;
            });
            index++;

            if (index === text.length) {
                clearInterval(intervalId);
            }
        }, speed);

        return () => clearInterval(intervalId);
    }, [text, speed]);

    return displayedText;
};
