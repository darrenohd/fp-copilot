class PromptManager:
    def __init__(self):
        self.prompt_templates = {
            'default': """You are an assistant for question-answering tasks...""",
            'academic': """You are a scholarly assistant...""",
            'technical': """You are a technical documentation expert..."""
        }
    
    def get_prompt(self, style='default', **kwargs):
        template = self.prompt_templates[style]
        return template.format(**kwargs) 