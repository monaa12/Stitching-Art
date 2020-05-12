import 'dart:typed_data';
import 'package:gallery_saver/gallery_saver.dart';
import 'package:flutter/material.dart';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'API.dart';
import 'pie_chart.dart';

class DMCGridded extends StatefulWidget {
  @override
  _DMCGriddedState createState() => _DMCGriddedState();
}

class _DMCGriddedState extends State<DMCGridded> {

  bool downloading=true;
  String downloadingStr="Processing";
  double download=0.0;
  File f;
  var imageUrl="http://127.0.0.1:5000/gridded_DMC";
  Widget getImageWidget() {
    if (f != null) {
      return Image.network("http://192.168.1.102:5000/gridded");
    } else {
      //return Image.network("http://10.0.2.2:5000/pie_chart");
      print("no");
    }
  }
  Future<void> downloadFile(imageUrl) async
  {
    try{
      Dio dio=Dio();
      var dir=await getApplicationDocumentsDirectory();
      String fileName=imageUrl.substring(imageUrl.lastIndexOf("/")+1);
      f=File("${dir.path}/$fileName");
      print(dir.path);
      print(f.path);
      Response response=await dio.download(imageUrl, "${dir.path}/$fileName" /*"${dir.path}/gridedddd.png"*/,onReceiveProgress: (rec,total){
        // GallerySaver.saveImage(f.path).then((bool success){
        //   setState(() {
        //    print('Image is saved');
        //  });
        //   });

        setState(() {
          downloading=true;
          download=(rec/total)*100;
          print(fileName);
          downloadingStr="Downloading Image : "+(download).toStringAsFixed(0);
        });
        setState(() {
          downloading=false;
          downloadingStr="Completed";
        });
      });
      // var filePath = await ImagePickerSaver.saveFile(
      //      fileData: response.bodyBytes);
      //await ImageGallerySaver.saveImage(imageUrl, albumName: "Abc");
      //final result = await ImageGallerySaver.saveImage(Uint8List.fromList(response.data));
      //print(result);
      // await f.writeAsBytes(response.bodyBytes, flush: true);
    }catch(e)
    {
      print(e);
    }
  }

  @override
  void initState() {
    super.initState();
    downloadFile(imageUrl);

  }

  Widget build(BuildContext context) {
    return Scaffold(

      appBar: AppBar(
        title:Text('Stitching Art',
          style: TextStyle(
            fontSize: 35.0,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true ,
        backgroundColor: Colors.red[700],
      ),
      body:
      Center(
        child: downloading?Container(
          height: 250,
          width: 250,
          child: Card(
            color: Colors.red[700],
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                CircularProgressIndicator(backgroundColor: Colors.white,),
                SizedBox(height: 20,),
                Text(downloadingStr,style: TextStyle(color: Colors.white),)
              ],
            ),
          ),
        ):
        Container(
          child:
          //Column(
          Center(
            child:
              Image.file(f,height: 650, width: 650,),
          ),
        ),

      ),
      //  Center(
      //      child:getImageWidget(),
      //  ),
      /* Column(
         // child: Center(
            //child: Image.file(f,height: 600, width: 600,fit: BoxFit.cover),
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
          getImageWidget(),
              //Image.file(f, height: 600, width: 600, fit: BoxFit.cover),

    ],
          ), */

      //   ),
      //da bta3 Center widget ),
      floatingActionButton:  FloatingActionButton(
        onPressed: () {
          // Navigator.push(context, MaterialPageRoute(builder: (context) => Chart()));
          Navigator.pushNamed(context, '/dmc_pie_chart');
        },
        child: Icon(
            Icons.navigate_next
        ),
        backgroundColor: Colors.red,
      ),
    );
  }
}
