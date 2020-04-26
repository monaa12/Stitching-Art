import 'package:flutter/material.dart';
import 'dart:io';
import 'dart:async';
import 'package:image_picker/image_picker.dart';
//import 'package:image_picker_modern/image_picker_modern.dart';

void main() => runApp(MaterialApp(
  home: Home(),
));
class Home extends StatefulWidget {

  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  File imageFile;

  _openGallery()async {
    var image = await ImagePicker.pickImage(source: ImageSource.gallery);
    setState(() => imageFile = image);

  }
  _openCamera()async{
    var image = await ImagePicker.pickImage(source: ImageSource.camera);
    setState(() => imageFile = image);
  }
  void _showOptions(BuildContext context) {

    showModalBottomSheet(
        context: context,
        builder: (context) {
          return Container(
              height: 150,
              child: Column(children: <Widget>[
                ListTile(
                    onTap: (){_openCamera();},
                    leading: Icon(Icons.photo_camera),
                    title: Text("Take a picture from camera")
                ),
                ListTile(
                    leading: Icon(Icons.photo_library),
                    onTap: (){_openGallery();} ,
                    title: Text("Choose from photo library")
                )
              ])
          );
        }
    );
  }
  Future<void> _showChoiceDialog(BuildContext context){
    return showDialog(context: context,builder:(BuildContext context){
      return AlertDialog(
        title: Text("Upload photo using:"),
        content: SingleChildScrollView(
          child: ListBody(
            children: <Widget>[
              GestureDetector(
                child:Text("Gallery"),
                onTap: (){_openGallery();},
              ),
              Padding(padding: EdgeInsets.all(8.0)),
              GestureDetector(
                child:Text("Camera"),
                onTap: (){_openCamera();},
              )
            ],
          ),
        ),
      );
    });
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
         appBar: AppBar(
        // title: Text('Stitching Art',style: TextStyle(fontFamily: 'IndieFlower')),
         centerTitle: true,
         title:Text('Stitching Art',
           style: TextStyle(
           fontFamily: 'IndieFlower',
         fontSize: 30.0,
        ),
        ),
        ),
        body: Center(
        child: Image(
        image:NetworkImage('https://i.pinimg.com/originals/5b/2a/74/5b2a74c90579bd8ab05b7399d4be2ede.jpg'),
        ),
        ),
        floatingActionButton: FloatingActionButton(
         onPressed: (){_showOptions(context);},
        child: Icon(
         Icons.add_a_photo
        ),
        ),
        );
  }
}


