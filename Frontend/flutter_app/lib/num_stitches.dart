//needed packages
import 'package:flutter/material.dart';
//needed .dart files
import 'package:flutterapp/API.dart';

class StitchesColors extends StatefulWidget {
  @override
  _StitchesColorsState createState() => _StitchesColorsState();
}

class _StitchesColorsState extends State<StitchesColors> {

  final TextEditingController StitchesController= new TextEditingController ();
  final TextEditingController Colorscontroller= new TextEditingController ();
  String colors="";
  String stitches="";
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
                Expanded(
                  flex:1,
                  child: Container(

                    padding: EdgeInsets.all(10.0),
                    child:          new TextField(
                      decoration: new InputDecoration(
                          hintText: "stitches"
                      ),
                      onSubmitted: (String str){
                        setState(() {
                          stitches = str;
                        });
                        StitchesController.text=stitches;
                      },
                      controller: StitchesController,
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
                    child:          new TextField(
                      decoration: new InputDecoration(
                          hintText: "colors"
                      ),
                      onSubmitted: (String str){
                        setState(() {
                          colors = str;
                        });
                        Colorscontroller.text=colors;
                      },
                      controller: Colorscontroller,
                    ),

                  ),
                ),
              ],
            ),
          ),
          Expanded (
            flex:2,
            child: Container(
            ),
          ),
        ],
      ),
      floatingActionButton:  FloatingActionButton(
        onPressed: () {
          Navigator.pushNamed(context, '/gridded');
          uploadStitches(stitches,colors);
        },
        child: Icon(
            Icons.done
        ),
        backgroundColor: Colors.red,
      ),
    ) ;
  }
}