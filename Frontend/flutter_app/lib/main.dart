import 'dart:io';
import 'package:flutter/material.dart';
//for images
import 'package:image_cropper/image_cropper.dart';
import 'package:image_picker/image_picker.dart';
//needed .dart files
import 'dmc_gridded.dart';
import'num_stitches.dart';
import 'pie_chart.dart';
import 'Gridded_image.dart';
import 'API.dart';
import 'dmc_pie_chart.dart';

void main() => runApp(MaterialApp(
  //home:Home(),
  initialRoute:'/',
  routes: {'/':(context)=>Home(),
    '/params':(context)=>StitchesColors(),
    '/automatic_crop':(context)=>Home(),
    '/gridded':(context)=>Gridded(),
    '/pie_chart':(context)=>Chart(),
    '/dmc_pie_chart': (context)=> DMCChart(),
    '/gridded_DMC' : (context)=>DMCGridded(),
  },
));
class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();

}
class _HomeState extends State<Home> {
  File _selectedFile;
  //function to upload images with camera or gallery
  getImage(ImageSource source) async{
    var image = await ImagePicker.pickImage(source:source);
    setState(() => _selectedFile = image);
  }
  //function showing options to use camera or gallery
  void _showOptions(BuildContext context) {
    showModalBottomSheet(
        context: context,
        builder: (context) {
          return Container(
              height: 150,
              child: Column(children: <Widget>[
                ListTile(
                    onTap: (){getImage(ImageSource.camera);
                    Navigator.of(context).pop();
                    },
                    leading: Icon(Icons.photo_camera),
                    title: Text("Take a photo using camera")
                ),
                ListTile(
                    leading: Icon(Icons.photo_library),
                    onTap: (){getImage(ImageSource.gallery);
                    Navigator.of(context).pop();
                    } ,
                    title: Text("Choose from photo library")
                )
              ])
          );
        }
    );
  }
  //function showing options to use cropper or object detection
  Future<void> _showChoiceDialog(BuildContext context){
    return showDialog(context: context,builder:(BuildContext context){
      return AlertDialog(
        title: Text("Crop your image using:",
          style: TextStyle(
            color: Colors.red[600],
            fontWeight: FontWeight.bold,
          ),
        ),
        content: SingleChildScrollView(
          child: ListBody(
            children: <Widget>[
              Row(
                children: <Widget>[
                  Expanded(
                    flex: 2,
                    child: Text('Your object',
                      style: TextStyle(
                        fontSize: 17.0,
                      ),
                    ),
                  ),
                  Expanded(
                    flex: 3,
                    child: new TextField(
                      decoration: new InputDecoration(
                          hintText: "Type here"
                      ),
                      onSubmitted: (String obj){
                        setState(() {
                          object = obj;
                        });
                        objectController.text="";
                      },
                      controller: objectController,
                    ),
                  )
                ],
              ),
              Padding(padding: EdgeInsets.all(8.0)),
              GestureDetector(
                child:Text("Cropper",
                  style: TextStyle(
                    fontSize: 17,
                  ),
                ),
                onTap: (){cropImage(_selectedFile);
                  Navigator.of(context).pop();},
              )
            ],
          ),
        ),
        actions: <Widget>[
          new FlatButton(
            child: new Text('SAVE',
              style: TextStyle(
                color: Colors.red[600],
                fontWeight: FontWeight.bold,
                fontSize: 17.0,
              ),
            ),
            onPressed: () {
              Navigator.of(context).pop();
            },
          )
        ],
      );
    });
  }
  Widget getImageWidget() {
    if (_selectedFile != null) {
      return Image.file(
        _selectedFile,
        width: 400,
        height: 400,
        fit: BoxFit.cover,
      );
    } else {
      return Image.asset(
        "assets/download.jpg",
        width: 400,
        height: 400,
        fit: BoxFit.cover,
      );}
  }
  cropImage(File img) async {
    this.setState((){
      // _inProcess = true;
    });
    if(img != null){
      File cropped = await ImageCropper.cropImage(
          sourcePath: img.path,
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
  //for text fields
  final TextEditingController controller= new TextEditingController ();
  final TextEditingController controller2= new TextEditingController ();
  final TextEditingController objectController= new TextEditingController ();
  String result="";
  String result2="";
  String object="";
  @override
  Widget build(BuildContext context) {
    return Scaffold(
     // key: scaffoldstate,
      appBar: AppBar(
        title:Text('Stitching Art',
          style: TextStyle(
            fontSize: 35.0,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true ,
        backgroundColor: Colors.redAccent[700],
      ),
      //backgroundColor: Colors.red[600],
      body:
      Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children : <Widget>[
          getImageWidget(),

          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              Align(
                alignment: Alignment.bottomLeft,
                child: FloatingActionButton(
                    backgroundColor: Colors.red,
                    child: Icon(
                        Icons.crop
                    ),
                    heroTag: null,
                    onPressed: () {
                      _showChoiceDialog(context);

                    }
                ),
              ),

              Align(
                alignment: Alignment.bottomRight,
                child: FloatingActionButton(
                    backgroundColor: Colors.red,
                    child: Icon(
                        Icons.add_a_photo
                    ),
                    heroTag: null,
                    onPressed: () {
                      _showOptions(context);
                    }),
              ),

            ],
          ),
          Padding(padding: EdgeInsets.all(10.0)),
          /*
          Expanded(
            flex:1,
            child: Container(
              padding: EdgeInsets.all(10.0),
              color: Colors.red[600],
              child: Text('Select Dimensions:',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 25.0,
                ),
              ),
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
                    color: Colors.red[600],
                    child: Text('width:',
                      style: TextStyle(
                        fontSize:20.0,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
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
                    color: Colors.red[600],
                    child: Text('length:',
                      style: TextStyle(
                        fontSize:20.0,
                        fontWeight: FontWeight.bold,
                      ) ,
                    ),
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
                    ),
                  ),
                ),

              ],
            ),
          ),
*/
        ],
      ),

      floatingActionButton: FloatingActionButton(
        onPressed: () {
         // Navigator.push(context, MaterialPageRoute(builder: (context) => output()));
          //uploadText(result);
          if (object != "") {
            Navigator.pushNamed(context, '/automatic_crop');
            uploadLabel(object);
          }
          Navigator.pushNamed(context, '/params');
          uploadFile(_selectedFile);
        },
        child: Icon(
            Icons.done
        ),
        backgroundColor: Colors.red,
      ),

    ) ;
  }
}