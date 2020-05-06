import 'package:path/path.dart';
import 'package:dio/dio.dart';

void uploadFile(filePath) async {
  // Get base file name
  String fileName = basename(filePath.path);
  print("File base name: $fileName");

  try {
    FormData photo =
    new FormData.from({"photo": new UploadFileInfo(filePath, fileName)});
    Response response = await Dio().post("http://10.0.2.2:5000/", data: photo);
    print("File upload response: $response");

  } catch (e) {
    print("Exception Caught: $e");
  }
}
void uploadStitches(number) async{
try {
  Response res = await Dio().post(
      "http://10.0.2.2:5000/params", data: {"width": number, "height": 40});
  print("value: $number");
}
catch(e){
  print("Exception Caught: $e");
}
}
void uploadLabel(object) async{
  try {
    Response resp = await Dio().post(
        "http://10.0.2.2:5000/automatic_crop", data: {"label": object});
    print("the object is: $object");
  }
  catch(e){
  print("Exception Caught: $e");
  }
}
