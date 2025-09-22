from rest_framework.views import APIView
from rest_framework import status
from .serializers import PromptSerializer
from .utils import call_deepseek_chat
from server.responses import success_response, error_response


class DeepSeekGenerateView(APIView):
    def post(self, request):
        serializer = PromptSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation failed",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        prompt = serializer.validated_data["prompt"]

        try:
            content = call_deepseek_chat(prompt)
            return success_response(
                details={"response": content},
                message="Response generated successfully",
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return error_response(
                message="DeepSeek call failed",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
