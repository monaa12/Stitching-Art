import 'package:flutter/material.dart';
import 'package:flutterapp/API.dart';
//import 'package:flutter/material.dart';
//import 'API.dart';
import 'package:flutterapp/Gridded_image.dart';
import 'package:flutterapp/main.dart';

class output extends StatefulWidget {
  @override
  _outputState createState() => _outputState();
}

class _outputState extends State<output> {
  final TextEditingController textCont= new TextEditingController ();
  final TextEditingController controller= new TextEditingController ();
  final TextEditingController controller2= new TextEditingController ();
  String result="";
  String result2="";
  String res="";
 Future <List<double>>dim;
  @override
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

      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children : <Widget>[
          Padding(padding: EdgeInsets.all(10.0)),
          Expanded(
            flex:1,
            child: Container(

              alignment:Alignment.centerLeft,
              padding: EdgeInsets.all(10.0),
              color: Colors.white70,
              child: Text('Make your own design:',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 25.0,
                 // color : Colors.red[600],
                ),
              ),
            ),
          ),
          Expanded(
            flex:1,
            child: Column(
              children: <Widget>[
                Expanded(
                  flex:1,
                  child: Container(
                    alignment:Alignment.centerLeft,
                    //height: 50,
                    //width: 400,
                    padding: EdgeInsets.all(10.0),
                    color: Colors.white70,
                    child: Text('Number of Stitches of Width:',
                      style: TextStyle(
                        fontSize:20.0,
                        fontWeight: FontWeight.normal,
                        color : Colors.red[600],

                      ),
                    ),
                  ),
                ),
                ////henaaaa ya haiodaaa
              Expanded(
                flex:1,
                child: Container(

                  padding: EdgeInsets.all(10.0),
                  //color: Colors.red[200],
                  child:          new TextField(
                    decoration: new InputDecoration(
                        hintText: "stitches"
                    ),
                    onSubmitted: (String str){
                      setState(() {
                        res = str;
                        //uploadFile(res);
                      });
                      textCont.text="";
                    },
                    controller: textCont,

                  ),
                ),
              )
                ],
                ),
          ),
        Expanded(
          flex:1,
          child: Column(
            children: <Widget>[
            Expanded(
            flex:1,
            child: Container(
              alignment:Alignment.centerLeft,
              padding: EdgeInsets.all(10.0),
              color: Colors.white70,
              child: Text('Number of image colors:',
                style: TextStyle(
                  fontSize:20.0,
                  fontWeight: FontWeight.normal,
                  color : Colors.red[600],

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
                    hintText: "colors"
                ),
                onSubmitted: (String str){
                  setState(() {
                    result = str;
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
          MaterialButton(
               color:Colors.red[600],

              child: Text(
                "Show expected output dimensions"
                //Icons.add_a_photo
              ),
              //backgroundColor: Colors.red,
              onPressed: () {
              dim= uploadStitches(res,result);
               // _showOptions(context);
              }),
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

                dim= uploadStitches(res,result);
              }
          ),

          Expanded(
            flex:1,
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
                    child: Text(
                      dim.toString() ,
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
                    child:new Text(
                      dim.toString(),
                    ),
                  ),
                ),

              ],
            ),
          ),

          //////////////////haiodaaa
          Expanded (
            flex:2,
            child: Container(

            ),
          ),
        ],

      ),


      floatingActionButton:  FloatingActionButton(
        onPressed: () {
          //Navigator.push(context, MaterialPageRoute(builder: (context) => Gridded()));
          Navigator.pushNamed(context, '/gridded');
          //uploadStitches(res,result);
          /// hanb3t hena el number of colors
          //uploadStitches(result);
        },
        child: Icon(
            Icons.done
        ),
        backgroundColor: Colors.red,
      ),
    ) ;
  }
}