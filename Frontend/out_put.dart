import 'package:flutter/material.dart';
class output extends StatefulWidget {
  @override
  _outputState createState() => _outputState();
}

class _outputState extends State<output> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title:Text('Stitching art'),
        centerTitle: true ,
        backgroundColor: Colors.red[200],
      ),
      body:Column(
        // mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children : <Widget>[
          Expanded(
            flex:3,
            child: Image(
              image: AssetImage('assets/cfff.jpg'),

            ),
          ),

        ],
      ),

    ) ;
  }
}
