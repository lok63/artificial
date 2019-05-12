from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

# Create your views here.

@api_view(["GET","POST"])
def store_dataset(request):
    """
    Accept a POST request that will contain the Dataset for the ML model
    """
    if request.method == 'GET':
        return JsonResponse({"Sucess": "Well done it works"})

    elif request.method == "POST":
        print("#######################")

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            csv_file = (request.FILES["file"])   
            #Return error messages when user upload wrong files
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a csv file")
                return render(request, template_form, args)
            else:
                print("#### Updating Bank Table")
                update_BankModel(csv_file)

                return redirect("/artificial_demo/list_dataset")

        else: #When form is not valid render the upload form again
            return render(request, template_form, args)


        response = {"Sucess": "You said " + incoming_data["test"] }
        return JsonResponse(response)
    
    raise APIException("There was a problem!")

class Store_Data(APIView):

    def post(self, request):

        incoming_data = request.data
        print("#######################")
        print(request.FILES)
        print(incoming_data)
        response = {"Sucess": "You said " + incoming_data["test"] }
        return Response(response)

    def get(self,request):
        return Response(request.data)

class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)


# class DataUpload(APIView):
#     serializer_class = InventoryFile_Serializer
#     parser_classes = [ MultiPartParser,FormParser ]

#     def post(self,request):
#         try:
#             serializer = InventoryFile_Serializer(data=request.data)
#             print(serializer.initial_data)

#             if serializer.is_valid():
#                 print(serializer.data)
#                 return Response("Done")
#             else:
#                 print(serializer.errors)
#                 return Response("Not Done")

#         except Exception as e:
#             return Response(str(e)) 