from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Quiz, Sitting
from .serializers import QuestionSerializer, QuizDetailSerializer, QuizSerializer, SittingSerializer


class QuizListView(ListAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()


class QuizDetailView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizDetailSerializer
    queryset = Quiz.objects.all()


class SittingApiView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Quiz.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        sitting = Sitting.objects.user_sitting(request.user, instance)

        if sitting:
            serializer = SittingSerializer(sitting)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_226_IM_USED)


class QuestionApiView(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Sitting.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        question = instance.get_first_question()

        if question:
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        else:
            instance.mark_quiz_complete()
            return Response({"status": "end"}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        user_answer = request.data.get('answer')
        instance = self.get_object()
        question = instance.get_first_question()

        correct = question.answer.lower() == user_answer.lower()

        # Save user answer
        instance.add_user_answer(question, user_answer)

        # remove question from current list
        instance.remove_first_question()

        if correct:
            print('Answer is correct')
            # Add points

            # Return that answer is correct
        else:
            # Add question to incorrect question

            # return that answer is incorrect with correct answer
            pass

        print(instance, request.data, question)

        return Response({})
