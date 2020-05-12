import 'package:flutter/material.dart';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'API.dart';
import 'main.dart';

class DMCChart extends StatefulWidget {
  @override
  _DMCChartState createState() => _DMCChartState();
}

class _DMCChartState extends State<DMCChart> {
  bool downloading=true;
  String downloadingStr="No data";
  double download=0.0;
  File f;
  var imageUrl="http://127.0.0.1:5000/dmc_pie_chart";
  Widget getImageWidget() {
    if (f != null) {
      return Image.file(
        f,
       // width: 500,
       // height: 500,
       // fit: BoxFit.cover,
      );
    } else {
      return Image.network(
        "assets/loading.jpg",
      //  width: 500,
      //  height: 500,
       // fit: BoxFit.cover,
      );
    }
  }
  Future<void> downloadDMCPieChart(imageUrl) async
  {
    try{
      Dio dio=Dio();
      var dir=await getApplicationDocumentsDirectory();
      String fileName=imageUrl.substring(imageUrl.lastIndexOf("/")+1);
      f=File("${dir.path}/$fileName");
      await dio.download(imageUrl, "${dir.path}/$fileName" /*"${dir.path}/gridedddd.png"*/,onReceiveProgress: (rec,total){
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
    downloadDMCPieChart(imageUrl);
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
     // Center(
     //   child:getImageWidget(),
      //),
      /*Column(
        // child: Center(
        //child: Image.file(f,height: 600, width: 600,fit: BoxFit.cover),
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: <Widget>[
          getImageWidget(),
          //Image.file(f, height: 600, width: 600, fit: BoxFit.cover),

        ],
      ),
      */
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
        ):Container(
          child:
          Center(
            child:Image.file(f,height: 650, width: 650,),
          ),
        ),
      ),


      floatingActionButton:  FloatingActionButton(
        onPressed: () {
          //Navigator.push(context, MaterialPageRoute(builder: (context) => Chart()));
          Navigator.pushNamed(context, '/');
        },
        child: Icon(
            Icons.done
        ),
        backgroundColor: Colors.red,
      ),
    );
  }
}
