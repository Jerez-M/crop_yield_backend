import numpy as np
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import CropData
from .serializers import CropDataSerializer

# import pickle
import os
from joblib import load

model_path = os.path.join(
    os.path.dirname(__file__), "ml_model", "random_forest_model.pkl"
)

with open(model_path, "rb") as file:
    model = load(file)


class YieldPredictionView(GenericAPIView):
    permission_classes = []
    serializer_class = CropDataSerializer
    queryset = CropData.objects.all()

    def post(self, request):
        year = request.data.get("year")
        country = request.data.get("country")
        item = request.data.get("item")
        rainfall = request.data.get("rainfall")
        temperature = request.data.get("temperature")
        pesticide = request.data.get("pesticide")

        # Perform prediction
        try:
            X = np.array([year, country, item, rainfall, temperature, pesticide])
            X = np.reshape(X, (1, -1))  # Reshape to 2D array
            yield_prediction = model.predict(X)*50
        except Exception as e:
            return Response(
                {
                    "message": "failed to perform prediction, please recheck your input variables",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            # save crop data instance
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                saved_instance = serializer.save()
                saved_instance.crop_yield = yield_prediction
                saved_instance.save()

            # Return the prediction result in the response
            return Response(
                {"crop_yield": yield_prediction.item()}, status=status.HTTP_201_CREATED
            )


class RetrieveCropDataByYearView(GenericAPIView):
    permission_classes = []
    serializer_class = CropDataSerializer
    queryset = CropData.objects.all()

    def get(self, request, year):
        try:
            crop_data = CropData.objects.filter(year=year)
        except CropData.DoesNotExist:
            return Response(
                {
                    "message": f"no crop data found for the year {year}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = self.serializer_class(crop_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class RetrieveCropData(GenericAPIView):
    permission_classes = []
    serializer_class = CropDataSerializer
    queryset = CropData.objects.all()

    def get(self, request, pk):
        try:
            crop_data = CropData.objects.get(pk=pk)
        except CropData.DoesNotExist:
            return Response(
                {
                    "message": f"Crop data not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = self.serializer_class(crop_data)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        
class RetrieveAllCropData(GenericAPIView):
    permission_classes = []
    serializer_class = CropDataSerializer
    queryset = CropData.objects.all()

    def get(self, request):
        crop_data = self.queryset.all()
        serializer = self.serializer_class(crop_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
class createCropData(CreateAPIView):
    permission_classes = []
    serializer_class = CropDataSerializer
    queryset = CropData.objects.all()
