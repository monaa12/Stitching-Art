//import 'dart:js';
import 'package:flutter/material.dart';
import 'package:flutterapp/pages/out_put.dart';

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
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children : <Widget>[
      Expanded(
        flex:3,
        child: Image(
        image: AssetImage('assets/cfff.jpg'),

        ),
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
