from rest_framework.views import APIView
from rest_framework import status
from .serializers import PromptSerializer
from .utils import call_deepseek_chat
from .local_huggingface import call_huggingface_chat
from server.responses import success_response, error_response
from .prompts import reword_task_prompt, extract_code


class DeepSeekGenerateView(APIView):

    def post(self, request):
        serializer = PromptSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation failed",
                details=" ".join(f"{field} field is required" for field in serializer.errors.keys()),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        task = serializer.validated_data["prompt"]
        language = serializer.validated_data.get("language", None)

        prompt = reword_task_prompt(task, language)

        try:
            content = call_deepseek_chat(prompt)
            code = extract_code(content)
            return success_response(
                data={"code": code},
                message="Response generated successfully",
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return error_response(
                message="DeepSeek call failed",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HuggingFaceGenerateView(APIView):

    def post(self, request):
        serializer = PromptSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation failed",
                details=" ".join(f"{field} field is required" for field in serializer.errors.keys()),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        task = serializer.validated_data["prompt"]

        prompt = reword_task_prompt(task, language="python")

        try:
            content = call_huggingface_chat(prompt)
            code = extract_code(content)
            return success_response(
                data={"code": code},
                message="Response generated successfully",
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return error_response(
                message="Internal Server Error",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
