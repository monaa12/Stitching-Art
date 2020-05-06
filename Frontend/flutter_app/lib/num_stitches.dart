import 'package:flutter/material.dart';
import 'API.dart';
class output extends StatefulWidget {
  @override
  _outputState createState() => _outputState();
}

class _outputState extends State<output> {
  final TextEditingController textCont= new TextEditingController ();
  String res="";
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

      body:Column(
        // mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children : <Widget>[

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

              )
              ,
            ),
          )
        ],
      ),
      floatingActionButton:  FloatingActionButton(
        onPressed: () {
          uploadStitches(res);
        },
        child: Icon(
            Icons.done
        ),
        backgroundColor: Colors.red,
      ),
    ) ;
  }
}