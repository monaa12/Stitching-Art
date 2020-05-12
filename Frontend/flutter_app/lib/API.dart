//needed packages for sending requests
import 'package:path/path.dart';
import 'package:dio/dio.dart';

//function to upload image to server
Future <void> uploadFile(filePath) async{
  // Get base file name
  String fileName = basename(filePath.path);
  print("File base name: $fileName");
  try{
    FormData photo = new FormData.fromMap({"photo" : await MultipartFile.fromFile(filePath.path,filename: fileName)});
    Response response = await Dio().post("http://127.0.0.1:5000/", data: photo);
    print("File upload response: $response");
  }
  catch(e)
  {
    print("Exception Caught: $e");
  }
}
//function to upload number of stitches to server
Future <void> uploadStitches(numStitches,numColors) async{
try {

  Dio dio = new Dio();
  List<Response> response = await Future.wait([dio.post("http://127.0.0.1:5000/params", data: {"width": numStitches, "height": numColors}),
    dio.get("http://127.0.0.1:5000/params")]);
}
catch(e){
  print("Exception Caught: $e");
}
}
//function to upload label if object detection option is selected to server
Future <void> uploadLabel(object) async{
  try {
    Response resp = await Dio().post("http://127.0.0.1:5000/automatic_crop", data: {"label": object});
  }
  catch(e){
  print("Exception Caught: $e");
  }
}
