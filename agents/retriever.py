class DocumentRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.5},
        )

    def get_relevant_context(self, query):
        docs = self.retriever.invoke(query)
        context = []
        sources = []
        
        for doc in docs:
            context.append(doc.page_content)
            sources.append({
                'file': doc.metadata.get('source', 'Unknown'),
                'page': doc.metadata.get('page', 'Unknown')
            })
            
        return {
            'context': "\n".join(context),
            'sources': sources
        } 