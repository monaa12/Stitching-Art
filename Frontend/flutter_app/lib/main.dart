//import 'dart:js';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutterapp/pages/out_put.dart';
import 'package:image_cropper/image_cropper.dart';
import 'package:image_picker/image_picker.dart';

void main() => runApp(MaterialApp(

    home:Home(),
  routes: {
    //  '/':(context)  =>Home(),
    '/output':(context)  =>output(),
  },
  ));
class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();

}

class _HomeState extends State<Home> {

  File _selectedFile;
  void _showOptions(BuildContext context) {

    showModalBottomSheet(
        context: context,
        builder: (context) {
          return Container(
              height: 150,
              child: Column(children: <Widget>[
                ListTile(
                    onTap: (){getImage(ImageSource.camera);},
                    leading: Icon(Icons.photo_camera),
                    title: Text("Take a picture from camera")
                ),
                ListTile(
                    leading: Icon(Icons.photo_library),
                    onTap: (){getImage(ImageSource.gallery);} ,
                    title: Text("Choose from photo library")
                )
              ])
          );
        }
    );
  }
  Widget getImageWidget() {
    if (_selectedFile != null) {
      return Image.file(
        _selectedFile,
        width: 250,
        height: 250,
        fit: BoxFit.cover,
      );
    } else {
      return Image.asset(
        "assets/cfff.jpg",
        width: 250,
        height: 250,
        fit: BoxFit.cover,
      );}
  }
  getImage(ImageSource source) async {
    this.setState((){
      //_inProcess = true;
    });
    File image = await ImagePicker.pickImage(source: source);
    if(image != null){
      File cropped = await ImageCropper.cropImage(
          sourcePath: image.path,
          aspectRatio: CropAspectRatio(
              ratioX: 1, ratioY: 1),
          compressQuality: 100,
          maxWidth: 700,
          maxHeight: 700,
          compressFormat: ImageCompressFormat.jpg,
          androidUiSettings: AndroidUiSettings(
            toolbarColor: Colors.red[200],
            toolbarTitle: "RPS Cropper",
            statusBarColor: Colors.red[200],
            backgroundColor: Colors.white,
          )
      );

      this.setState((){
        _selectedFile = cropped;
        //_inProcess = false;
      });
    } else {
      this.setState((){
        //_inProcess = false;
      });
    }
  }

  final TextEditingController controller= new TextEditingController ();
  final TextEditingController controller2= new TextEditingController ();
  String result="";
  String result2="";
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title:Text('Stitching art'),
        centerTitle: true ,
        backgroundColor: Colors.red[200],
      ),

      body:Column(
        //haiodaaaaaa
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children : <Widget>[
          getImageWidget(),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              
              MaterialButton(
                  color: Colors.deepOrange,
                  child: Icon(
                      Icons.add_a_photo
                  ),
                //  child: Text(

                  //  "Device",
                   // style: TextStyle(color: Colors.white),
                  //),
                  onPressed: () {
                    _showOptions(context);
                    //getImage(ImageSource.gallery);
                  }
               )
            ],
          ),

    Expanded(
      flex:1,
      child: Container(

        padding: EdgeInsets.all(10.0),
        color: Colors.red[200],
        child: Text('Select Dimensions:'),
      ),
    ),
    Expanded(
      flex:3,
      child: Row(
        children: <Widget>[
          Expanded(
            flex:1,
            child: Container(

              padding: EdgeInsets.all(10.0),
              color: Colors.red[200],
              child: Text('width:'),
            ),
          ),
          Expanded(
            flex:1,
            child: Container(

              padding: EdgeInsets.all(10.0),
              //color: Colors.red[200],
              child:          new TextField(
                decoration: new InputDecoration(
                    hintText: "width"
                ),
                onSubmitted: (String str){
                  setState(() {
                    result = str;
                  });
                  controller.text="";
                },
                controller: controller,
              )
              ,
            ),
          ),
          //Text('width'),
          //Text('length'),
          Expanded(
            flex:1,
            child: Container(

              padding: EdgeInsets.all(10.0),
              color: Colors.red[200],
              child: Text('length:'),
            ),
          ),
          Expanded(
            flex:1,
            child: Container(

              padding: EdgeInsets.all(10.0),
              //color: Colors.red[200],
              child:          new TextField(
                decoration: new InputDecoration(
                    hintText: "length"
                ),
                onSubmitted: (String str){
                  setState(() {
                    result2 = str;
                  });
                  controller2.text="";
                },
                controller: controller2,
              )
              ,
            ),
          ),
        ],
      ),
    ),

    ],
      ),
      /*
      Center(
        child: Image(
          image: AssetImage('assets/cfff.jpg'),

        )
      ),*/
      floatingActionButton: FloatingActionButton(
        onPressed: (){
          Navigator.pushNamed(context, '/output');
        },
        child: Text('Done'),
        backgroundColor: Colors.red[200],
      ),

    ) ;
  }
}
