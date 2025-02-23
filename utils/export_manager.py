class ExportManager:
    @staticmethod
    def export_chat_history(messages, format='markdown'):
        if format == 'markdown':
            return ExportManager._to_markdown(messages)
        elif format == 'pdf':
            return ExportManager._to_pdf(messages)
        elif format == 'txt':
            return ExportManager._to_txt(messages) 