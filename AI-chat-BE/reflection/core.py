class Reflection():
    def __init__(self, llm):
        self.llm = llm

    def _concat_and_format_texts(self, data):
        concatenatedTexts = []
        for entry in data:
            role = entry.get('role', '')
            all_texts = ' '.join(part['text'] for part in entry['parts'])
            concatenatedTexts.append(f"{role}: {all_texts} \n")
        return ''.join(concatenatedTexts)


    def __call__(self, chatHistory, lastItemsConsidereds=15):
        
        # if len(chatHistory) >= lastItemsConsidereds:
        #     chatHistory = chatHistory[len(chatHistory) - lastItemsConsidereds:]

        # historyString = self._concat_and_format_texts(chatHistory)
        historyString = chatHistory
        higherLevelSummariesPrompt = """Đưa ra lịch sử trò chuyện và câu hỏi mới nhất của người dùng có thể tham khảo ngữ cảnh trong lịch sử trò chuyện, hãy tạo một đoạn văn bản ngắn để tóm tắt nội dung cuộc trò chuyện để mô hình hiểu được ngữ cảnh. KHÔNG trả lời câu hỏi, chỉ sửa lại câu hỏi nếu cần và nếu không thì trả lại như cũ. 
        """

        # print(higherLevelSummariesPrompt)
        messages=[(
                    "system",
                    higherLevelSummariesPrompt
                ),
                ("human", historyString)
            ]
        
        completion = self.llm.invoke(messages)
    
        return completion.content