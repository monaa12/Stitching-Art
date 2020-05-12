import 'dart:typed_data';
import 'package:gallery_saver/gallery_saver.dart';
import 'package:flutter/material.dart';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'API.dart';
import 'pie_chart.dart';

class Gridded extends StatefulWidget {
  @override
  _GriddedState createState() => _GriddedState();
}

class _GriddedState extends State<Gridded> {

  bool downloading=true;
  String downloadingStr="Processing";
  double download=0.0;
  File f;
  var imageUrl="http://127.0.0.1:5000/gridded";

  Future<void> downloadFile(imageUrl) async
  {
    try{
      Dio dio=Dio();
      var dir=await getApplicationDocumentsDirectory();
      String fileName=imageUrl.substring(imageUrl.lastIndexOf("/")+1);
      f=File("${dir.path}/$fileName");
      print(dir.path);
      print(f.path);
      Response response=await dio.download(imageUrl, "${dir.path}/$fileName" ,onReceiveProgress: (rec,total){

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
            Center(
              child: Image.file(f,height: 650, width: 650,),
          ),
        ),

      ),

      floatingActionButton:  FloatingActionButton(
        onPressed: () {
          Navigator.pushNamed(context, '/pie_chart');
        },
        child: Icon(
            Icons.navigate_next
        ),
        backgroundColor: Colors.red,
      ),
    );
  }
}
