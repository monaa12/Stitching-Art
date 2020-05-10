//import 'dart:html';
import 'package:flutter/material.dart';
import 'package:path/path.dart';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';
import 'Gridded_image.dart';

//  final GlobalKey<ScaffoldState> _scaffoldstate =new GlobalKey<ScaffoldState>();
/*void uploadFile(filePath) async {
  // Get base file name
  String fileName = basename(filePath.path);
  print("File base name: $fileName");

  try {
    FormData photo =
    new FormData.from({"photo": new UploadFileInfo(filePath, fileName)});
    Response response = await Dio().post("http://10.0.2.2:5000/", data: photo);
    print("File upload response: $response");
    //   _showBarMsg(response.data['message']);
  } catch (e) {
    print("Exception Caught: $e");
  }
}

 */
class APIs extends StatefulWidget {
  @override
  _APIsState createState() => _APIsState();
}

class _APIsState extends State<APIs> {
  @override

  Widget build(BuildContext context) {
    return Container();
  }
}



Future <void> uploadFile(filePath) async{
  // Get base file name
  String fileName = basename(filePath.path);
  print("File base name: $fileName");
  try{
    FormData photo = new FormData.fromMap({"photo" : await MultipartFile.fromFile(filePath.path,filename: fileName)});
    Response response = await Dio().post("http://10.0.2.2:5000/", data: photo);
    print("File upload response: $response");
  }
  catch(e)
  {
    print("Exception Caught: $e");
  }
}

void uploadStitches(number) async{
  try {
    // FormData formData = new FormData.from({
    //   "width": number
    // });
    Response res = await Dio().post(
        "http://10.0.2.2:5000/params", data: {"width": number, "height": 8});
    print("value: $number");

    //Response res2 = await Dio().get("http://10.0.2.2:5000/params");
    //print(res2.data);
  }
  catch(e){
    print("Exception Caught: $e");
  }
}
Future <void> uploadLabel(object) async{
  try {
    Response resp = await Dio().post(
        "http://10.0.2.2:5000/automatic_crop", data: {"label": object});
    print("the object is: $object");
  }
  catch(e){
    print("Exception Caught: $e");
  }
}
void uploadLabelImage(object,filePath) async{
  String fileName = basename(filePath.path);
  print("File base name: $fileName");
  try{
    FormData photoLabel = new FormData.fromMap({"label": object,"photo" : await MultipartFile.fromFile(filePath.path,filename: fileName)});
    Response response = await Dio().post("http://10.0.2.2:5000/", data: photoLabel);
    print("File upload response: $response");
    print("the object is: $object");
  }
  catch(e)
  {
    print("Exception Caught: $e");
  }

}
/*Future <void> downloadImage() async{
 // String savePath="./grided.png";
  final imageUrl="http://10.0.2.2:5000/gridded";
  Dio dio=Dio();
  try{
    var directory=await getApplicationDocumentsDirectory();
    await dio.download(imageUrl, "${directory.path}/grided.png", onReceiveProgress: (rec,total){
      print("Rec: $rec , Total: $total");
    });
  }
  catch(e){
    print(e);
  }
  //Response image= await Dio().download("http://10.0.2.2:5000/gridded", savePath);


  //File f;
  //f=File("${dir.path}/grided.png");
}

 */


//void _showBarMsg(String msg) {
// scaffoldstate.currentState.showSnackBar(new SnackBar(content: new Text(msg)));
//}