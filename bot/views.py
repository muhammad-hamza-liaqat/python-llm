import os
import fitz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from .utils import save_to_vectorstore, get_vectorstore


class UploadDocumentView(APIView):

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        upload_dir = os.path.join(settings.BASE_DIR, "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.name)
        with open(file_path, "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        doc = fitz.open(file_path)
        texts = []
        for page in doc:
            text = page.get_text()
            if text.strip():
                texts.append(text)
        doc.close()

        if not texts:
            return Response({"error": "No extractable text found"}, status=status.HTTP_400_BAD_REQUEST)

        save_to_vectorstore(texts, [{"title": file.name, "file_path": file_path} for _ in texts])

        return Response({"message": f"File '{file.name}' uploaded and indexed successfully"})


class AskQuestionView(APIView):

    def post(self, request, *args, **kwargs):
        question = request.data.get("question")
        if not question:
            return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)

        vectorstore = get_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        docs = retriever.invoke(question)
        # print("🔍 Retrieved Docs:", [d.page_content[:200] for d in docs])

        if not docs:
            return Response({"answer": "I don't know."})

        llm = ChatOpenAI(
            temperature=0,
            model="gpt-4o-mini",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )

        template = """
        You are a helpful assistant. Answer the question based only on the provided documents.
        If you don't know the answer from the documents, say "I don't know."

        Context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        chain = prompt | llm
        answer = chain.invoke({"context": "\n\n".join([d.page_content for d in docs]), "question": question})

        return Response({"answer": answer.content})
